# check_jsonl.py
import json
with open('keyword_matches.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        print(json.loads(line))