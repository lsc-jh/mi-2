import requests
import json

# Task 1
with open('hello.txt', 'w') as f:
    f.write('Hello World!\n')

# Task 2
with open('hello.txt', 'a') as f:
    f.write("Hello again!\n")

# Task 3
LSC_AI_URL = 'https://lsc-ai.kou-gen.net/prompt-legacy/mi-1/v1/generate'
body = {
    "scene": "test_sceneaskadfsbhjklnadfsbdfghjklsabdefghijkrsbfghijkadfgshjbabghjkbdfghjks"
}
result = requests.post(LSC_AI_URL, json=body)

with open('result.json', 'w') as f:
    raw_json = result.json()
    f.write(json.dumps(raw_json))

with open('result.json', 'r') as f:
    raw_json = json.load(f)
    with open('prompt.txt', 'w') as pf:
        pf.write(raw_json['prompt'])

