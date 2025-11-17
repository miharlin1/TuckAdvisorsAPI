import json
from pathlib import Path

#Args: json_path: Path to the JSON file
#Returns: String containing the GPT output markdown
def parse_gpt_output(json_path):
    p = Path(json_path)
    if not p.exists():
        raise FileNotFoundError(f"{json_path} not found")
    
    raw = p.read_text(encoding="utf-8")
    data = json.loads(raw)
    
    if "gptOutput" not in data or not isinstance(data["gptOutput"], str):
        raise ValueError("input JSON must contain a 'gptOutput' string field")
    
    return data["gptOutput"]
