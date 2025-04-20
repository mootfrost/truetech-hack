import requests
from app.config import config

headers = {
    'Authorization': 'Bearer ' + config.openai_token
}
body = {
    'model': 'mws-gpt-alpha',
    "messages": [
        {"role":"use", "content": "Привет, как дела?"}
    ],
    "temperature": 0.6
}

resp = requests.post('https://api.gpt.mws.ru/v1/chat/completions', headers=headers, json=body)
print(resp.json())