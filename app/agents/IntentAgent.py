import logging

from langchain.schema import SystemMessage, HumanMessage
from app.routes.user_base import users
from app.agents.BaseAgent import BaseAgent
from app.deps import chat_model, get_session
from app.models import User
import logging
import re

logger = logging.getLogger('uvicorn.error')


class IntentAgent(BaseAgent):

    @staticmethod
    def preprocess(text: str) -> str:
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        return text.strip()

    @staticmethod
    async def get_intent(text: str) -> str:
        messages = [
            SystemMessage(content='Ты четко определяешь только intent запроса на русском и делаешь это не более чем за 5 слов. Никогда не пиши ничего кроме intent. Intet - это предмет того, что хочет пользователь или с чем возникла проблема'),
            HumanMessage(content=f'определи интент: {text}.'),
        ]
        response = await chat_model.apredict_messages(messages)
        return response.content

    @staticmethod
    async def extract_entities(intent: str, text: str) -> str:
        messages = [
            SystemMessage(content='''Ты — модель для извлечения сущностей из пользовательских сообщений на основе заданного интента.
            Формат ответа: только JSON с ключами и значениями сущностей.'''),
            HumanMessage(content=f'Твоя задача: получить сущности, нужные для работы с {intent} из текста {text}')
        ]
        response = await chat_model.apredict_messages(messages)
        return response.content

    @staticmethod
    async def analyze_user(user: str) -> str:
        messages = [
            SystemMessage(content='ты ищешь зацепки о финансовом положении пользователя и его лояльности'),
            HumanMessage(content=f'Проанализируй информацию и определи кейсы {user}. Напиши только самый правдоподобный'),
        ]
        response = await chat_model.apredict_messages(messages)
        return response.content

    @staticmethod
    async def summ_ask(intent:str, entitiesstr:str, user_info: str | None) -> str:
        message = [
            SystemMessage(content='Проанализировав все свойствыа ты даешь краткую точную информацию зачем пользователь написал в поддержку на основании данных про него исключительно итоговую оценку'),
            HumanMessage(content=f'Проанализируй {intent}, {entitiesstr}, {user_info} '),]

        response = await chat_model.apredict_messages(message)
        return response.content

    async def run(self, query: str, context: dict = None) -> str:
        preprocessed = self.preprocess(query)
        user_info = None
        if context:
            user_info = await self.analyze_user(context['user'])
            preprocessed += ' То, что мы знаем о пользователе, это может помочь:' + user_info
            logger.debug(f'[User Info]: {user_info}')

        intent = await self.get_intent(preprocessed)
        entities = await self.extract_entities(intent, preprocessed)

        logger.debug(f'[Intent]: {intent}')
        logger.debug(f'[Entities]: {entities}')

        # final_answer = await self.summ_ask(intent, entities, user_info)
        # print(final_answer)
        return intent
