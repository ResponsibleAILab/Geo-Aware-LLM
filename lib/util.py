import json
from typing import List

def save_file(filepath: str, content: str):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

def save_jsonl_file(filepath: str, objects: List[any]):
    with open(filepath, 'w', encoding='utf-8') as f:
        for obj in objects:
            f.write(json.dumps(obj) + '\n')