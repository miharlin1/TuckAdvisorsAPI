#init_db.py
#Initialize the database and load the initial analysis from input.json

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from parser import parse_gpt_output
import database as db

def main():
    print("Initializing database...")
    
    # Create database and schema
    db.init_database()
    
    # Load GPT output from input.json
    input_file = Path(__file__).parent / "src" / "data" / "input.json"
    
    if not input_file.exists():
        print(f"Error: {input_file} not found")
        return
    
    print(f"Loading GPT output from {input_file}...")
    markdown_content = parse_gpt_output(str(input_file))
    
    # Insert into database
    analysis_id = db.insert_analysis(markdown_content)
    
    print("\nDatabase ready! Start the API with:")
    print("  python3 src/api.py")

if __name__ == "__main__":
    main()

