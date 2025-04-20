from fastapi import APIRouter
from app.config import config
import requests
import re


def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)      # удаление пунктуации
    text = text.strip()
    return text


def classify_with_model(text):
    payload = {
        "model": 'mws-gpt-alpha',
        "messages": [{"role": "user", "content": f"Определи эмоции клиента: '{text}'"}],
        "temperature": 0
    }
    return  payload

headers = {
    'Authorization': 'Bearer ' + config.mws_token
}


router = APIRouter(prefix='/emo')
@router.get('/remo')
async def remo(text: str):
    resp = requests.post('https://api.gpt.mws.ru/v1/chat/completions', headers=headers, json=classify_with_model(text))
    print(resp.json()["choices"][0]["message"]["content"])
    return {'message': 'em agent'}




__all__ = ['router']