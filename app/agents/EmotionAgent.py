from langchain.schema import SystemMessage, HumanMessage
from app.agents.BaseAgent import BaseAgent
from app.deps import chat_model
from app.agents.examples import good_example, bad_example
import logging

logger = logging.getLogger('uvicorn.error')


class EmotionAgent(BaseAgent):

    @staticmethod
    async def detert_emotion(text:str) -> str:
        determination = [SystemMessage(content="""Ты — AI-анализатор эмоций в сообщениях пользователя. 
Твоя задача — определить эмоцию, тональность и необходимость эскалации к оператору. Всегда возаращай чистый машиночитаемый JSON без лишей обвязки
Формат ответа: JSON с полями:
{
  "emotion": <эмоция>,
  "sentiment": <позитивно/негативно/нейтрально>,
  "escalate": true/false,
  "emotion_force": от 0 до 100
  
}"""+

f"""emotion_force для позитивных эмоций градируется как: {good_example}
для негативных: {bad_example}
Эмоции: злость, раздражение, разочарование, грусть, страх, радость, удивление, благодарность, нейтрально."""),
                         HumanMessage(content=f'определи эмоцию: {text}. ВСЕГДА ВОЗАРАЩАЙ ЧИСТЫЙ МАШИНОЧИТАЕМЫЙ JSON БЕЗ ЛИШЕЙ ОБВЯЗКИ')
        ]

        response = await chat_model.apredict_messages(determination)
        return response.content

    async def run(self, query: str, context: dict = None) -> str:
        emotion_evol = await self.detert_emotion(query)
        logger.debug(f'[emotion_evol]: {emotion_evol}')
        return emotion_evol
