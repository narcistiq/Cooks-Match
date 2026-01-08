import ast
from typing import List
from dotenv import dotenv_values
from google import genai

OUTPUT_FILE = "./output.txt"
CLEANED_FILE = "./cleaned_file.txt"

def remove_numbers(contents : List[List[str]]) -> List[str]:
    # Remove integers and floats from list
    new_contents = []

    DELIMITERS = [" ", ".", "-", "#", "(", ")", "/", ":", ',']

    for i, list in enumerate(contents):
        for item in list:
            try:
                # Remove delimiters from item
                for delimiter in DELIMITERS:
                    item = item.replace(delimiter, "")

                float(item)
            except:
                new_contents.append(item)
    
    return new_contents

def llm_clean_up(contents : List[List[str]], API_KEY : str) -> str:
    prompt = "You are part of a program. You will output ONLY food from this receipt. Additionally, output everything in lowercase. Please output as a Python list where each item is a string."
    prompt = prompt + "\n\n" + str(contents)

    client = genai.Client(api_key=API_KEY)
    response = client.models.generate_content(
        contents=prompt,
        model="gemini-3-pro-preview"
    )

    return response.text

if __name__ == "__main__":
    config = dotenv_values(".env")
    API_KEY = config.get("GEMINI_API_KEY")
    file = open(OUTPUT_FILE)
    contents = file.read()
    file.close()

    # Convert to literal data value (list of lists)
    contents = ast.literal_eval(contents)

    # Clean data before sending to LLM
    cleaned = remove_numbers(contents)
    
    # Call LLM to clean up data
    response = llm_clean_up(cleaned, API_KEY)

    with open(CLEANED_FILE, "w") as file:
        file.write(str(response))