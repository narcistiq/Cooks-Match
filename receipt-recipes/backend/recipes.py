import google.generativeai as genai
import os
import csv
import json
from google.generativeai.types import GenerateContentResponse
from dotenv import load_dotenv
from pymongo import MongoClient
from pathlib import Path

load_dotenv()

client = MongoClient("mongodb://localhost:27017")

db = client["Recipes"]
collection = db["Recipes"]
csv_path = Path(r"../../Receipes from around the world.csv") 
open_kwargs = {         
    "mode": "r",
    "encoding": "utf-8",
    "newline": "",
}
rows = None
with csv_path.open(encoding="cp1252") as f:      # Windows‑1252 (aka Latin‑1)
    reader = csv.DictReader(f)
    rows = list(reader)
    
collection.delete_many({})
collection.insert_many(rows)
# for i, doc in enumerate(client["Recipes"]["Recipes"].find(), start=1):
#     print(doc)
#     if i == 10:
#         break    
     
recipes = list(collection.find({}, {"_id": 0}))
#print(recipes[:10])

class GeminiClient:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-3-pro-preview")
        self.context = ""

    def setup(self, actualingredients: list):
        ingredients_text = ", ".join(actualingredients)

        self.context = (
            "You have these ingredients:\n"
            f"{ingredients_text}\n"
        )

    def ask(self) -> dict:
        question = (
        "Please choose at least 3 recipes that contain these items. "
        "Make the necessary substitutions as needed. "
        "Return ONLY valid JSON in the following format:\n\n"
        "{ \"recipes\": [ { \"name\": \"\", \"servings\": \"\", "
        "\"ingredients\": [], \"instructions\": [], "
        "\"prep_time\": \"\", \"cook_time\": \"\", \"substitutions\": \"\" } ] }"
        )

        prompt = f"{self.context}\nQuestion: {question}"

        response = self.model.generate_content(
            prompt,
            generation_config={
                "response_mime_type": "application/json",
            },
        )

        return json.loads(response.text)



