from fastapi import APIRouter
from app.config import config
import requests
import re


def classify_with_model(text):
    prompt = {
        "model": 'mws-gpt-alpha',
        "messages": [{"role": """Ты — AI-анализатор эмоций в сообщениях пользователя. 
Твоя задача — определить эмоцию, тональность и необходимость эскалации к оператору.
    
Формат ответа: JSON с полями:
{
  "emotion": <эмоция>,
  "sentiment": <позитивно/негативно/нейтрально>,
  "escalate": true/false,
  "emotion_force": от 0 до 100
  
}

emotion_force - cbkf 'vjwbb

Эмоции: злость, раздражение, разочарование, грусть, страх, радость, удивление, благодарность, нейтрально.
""",
        "content": f"Определи эмоции клиента: '{text}' верни json"}],
        "temperature": 0.5
    }
    return prompt


headers = {
    'Authorization': 'Bearer ' + config.mws_token
}


router = APIRouter(prefix='/emo')
@router.get('/request')
async def remo(text: str):
    resp = requests.post('https://api.gpt.mws.ru/v1/chat/completions', headers=headers, json=classify_with_model(text))
    print(resp.json()["choices"][0]["message"]["content"])
    return {'message': 'em agent'}




__all__ = ['router']