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
  "messages": [
    {
      "role": "system",
      "content": "Ты помощник компании МТС. Всегда выполняй свою работу чётко."
    },{"role": "System", "content": f"Определи намерения клиента: '{text}'"}],
        "temperature": 0
    }
    return payload

headers = {
    'Authorization': 'Bearer ' + config.mws_token
}



router = APIRouter(prefix='/rag')
@router.get('/request')
async def request(text: str):
    resp = requests.post('https://api.gpt.mws.ru/v1/chat/completions', headers=headers, json=classify_with_model(text))
    print(resp.json()["choices"][0]["message"]["content"])
    return {'message': 'kb agent'}




__all__ = ['router']