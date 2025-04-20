from fastapi import APIRouter
import requests
from app.config import config
import re


router = APIRouter(prefix='/qa')


def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)      # удаление пунктуации
    text = text.strip()
    return text


def classify_with_model(text):
    payload = {
        "model": 'mws-gpt-alpha',
        "messages": [{"role": "user", "content": f"Определи намерения клиента: '{text}'"}],
        "temperature": 0
    }
    return  payload

headers = {
    'Authorization': 'Bearer ' + config.mws_token
}



resp = requests.post('https://api.gpt.mws.ru/v1/chat/completions', headers=headers, json=classify_with_model("pass"))
q = resp.json()
print(q)

@router.get('/')
async def status():
    return {'message': 'kb agent'}


__all__ = ['router']