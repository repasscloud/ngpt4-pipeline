import os
import json
import requests

OLLAMA_API_URL = "http://localhost:11434/generate"

def request_variations(sentence, model="llama3.2:3b", count=10):
    """
    Sends a request to the Ollama API to generate variations of the input sentence.
    """
    variations = []
    for _ in range(count):
        payload = {
            "model": model,
            "prompt": f"Generate a similar statement to: {sentence}"
        }
        response = requests.post(OLLAMA_API_URL, json=payload)
        if response.status_code == 200:
            data = response.json()
            variation = data.get("completion", "").strip()
            if variation:
                variations.append(variation)
    return variations

def process_input_file(input_file):
    """
    Reads the input JSON, processes each intent, and generates output files.
    """
    with open(input_file, "r") as f:
        data = json.load(f)
    
    for intent, sentences in data.items():
        output_file = f"{intent}.json"
        all_variations = {}
        
        for sentence in sentences:
            print(f"Generating variations for: {sentence}")
            variations = request_variations(sentence)
            all_variations[sentence] = variations
        
        with open(output_file, "w") as outfile:
            json.dump(all_variations, outfile, indent=4)
        print(f"Saved variations to {output_file}")

if __name__ == "__main__":
    input_file = "input.json"  # Input JSON file in $PWD
    if os.path.exists(input_file):
        process_input_file(input_file)
    else:
        print(f"Input file {input_file} not found. Please provide one in the current directory.")
