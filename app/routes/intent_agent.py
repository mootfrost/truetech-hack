from fastapi import APIRouter
from app.config import config
from app.routes.user_base import users
import requests
import re
# import spacy



def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)      # удаление пунктуации
    text = text.strip()
    return text


def verify_intent(text):
    payload = {
        "model": 'mws-gpt-alpha',
  "messages": [
    {
      "role": "system",
      "content": f"Ты четко определяешь только intent запроса сначала на русском а потом на английском и делаешь это не более чем за 4 слова для каждого "
    },
      {"role": "user", "content": f"определи интент: '{text}'"},
  ],
        "temperature": 0
    }
    return payload


def create_script_ML(intent, text):
    script_ML = {
        "model" : "mws-gpt-alpha",
        "messages": [
    {
      "role": "system",
      "content": f"ты аналитик по услугам"
    },
      {"role": "user", "content": f"Проанализируй информацию и определи основные кейсы {users[id]}"}
  ],
        "temperature": 0.2
    }
    return script_ML


def detert_user(id):
    user_info = {
        "model" : "mws-gpt-alpha",
        "messages": [
    {
      "role": "system",
      "content": f"ты ищешь зацепки о финансовом положении пользователя и его лояльности"
    },
      {"role": "user", "content": f"Проанализируй информацию и определи кейсы {users[id]}"}
  ],
        "temperature": 0
    }
    return user_info


headers = {'Authorization': 'Bearer ' + config.mws_token}
router = APIRouter(prefix='/inte')


@router.get('/request')
async def request(text: str, id):

    resp = requests.post('https://api.gpt.mws.ru/v1/chat/completions', headers=headers, json=verify_intent(text))
    user_intent = resp.json()["choices"][0]["message"]["content"]

    response = requests.post('https://api.gpt.mws.ru/v1/chat/completions', headers=headers, json=detert_user(id))
    info_about_user = response.json()["choices"][0]["message"]["content"]


    print(type(user_intent), info_about_user)
    return {'message': info_about_user}


__all__ = ['router']