from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from recipes import GeminiClient
import os, shutil, subprocess, ast

app = FastAPI()

# For some reason the 127.0.0.1 origins don't resolve and we are unable to connect
origins = [
    "http://localhost:5173",   # Vite
    # "http://127.0.0.1:5173",
    "http://localhost:3000",   # CRA
    # "http://127.0.0.1:3000",
]

client = MongoClient("mongodb://localhost:27017/")
db = client["recipes_db"]       # database
collection = db["recipes"]      # collection
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
async def main():
    return

@app.post("/uploads/")
async def upload_receipt(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # backend/
    OCR_DIR = os.path.join(BASE_DIR, "ocr-reader")
    OCR_PATH = os.path.join(OCR_DIR, "ocr-reader.py")
    DATA_CLEANER_PATH = os.path.join(OCR_DIR, "data_cleaner.py")

    try:
        subprocess.run(["python", OCR_PATH], check=True)
        subprocess.run(["python", DATA_CLEANER_PATH], check=True)
    except subprocess.CalledProcessError as e:
            # This happens if the script exits with a non-zero status
            raise HTTPException(status_code=500, detail=f"OCR script failed: {e}")
    except FileNotFoundError as e:
            # This happens if the path to the script is wrong
            raise HTTPException(status_code=500, detail=f"Script not found: {e}")
    except Exception as e:
            # Catch anything else
            raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


    # 3. Read processed output
    CLEANED_FILE_PATH = os.path.join(BASE_DIR, "cleaned_file.txt")
    with open(CLEANED_FILE_PATH, "r") as f:
        contents = f.read().strip()
        
        # Remove markdown code block syntax if present
        if contents.startswith("```python"):
            contents = contents.replace("```python", "").replace("```", "").strip()
        elif contents.startswith("````plaintext\n```python"):
            contents = contents.replace("````plaintext\n```python", "").replace("```\n````", "").strip()
        
        parsed = ast.literal_eval(contents)   # Parse the list from file
        
        # Handle both flat list and nested list formats
        if parsed and isinstance(parsed[0], list):
            # Nested list format: [['tomato', 'onion', 'garlic']]
            ingredients = [item for sublist in parsed for item in sublist]  # flatten
        else:
            # Flat list format: ['diced tomatoes', 'tomato paste', ...]
            ingredients = parsed

    # 4. Call /recipes/generate internally
    try:
        recipes = generate_recipes(ingredients)
        return recipes
    except Exception as e:
        print(f"Error generating recipes: {e}")  # Debug logging
        raise HTTPException(status_code=500, detail=f"Recipe generation failed: {e}")


@app.post("/recipes/generate/")
def generate_recipes(ingredients_text: list[str]):
    try:
        print(f"Generating recipes for ingredients: {ingredients_text}")  # Debug logging
        gemini = GeminiClient()
        gemini.setup(ingredients_text)
        recipes = gemini.ask()
        return recipes
    
    except Exception as e:
        print(f"Gemini API error: {e}")  # Debug logging
        raise HTTPException(status_code=500, detail=f"Gemini API error: {e}")
    
