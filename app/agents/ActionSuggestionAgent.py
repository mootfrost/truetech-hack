from langchain.schema import SystemMessage, HumanMessage
from app.agents.IntentAgent import IntentAgent
from app.agents.BaseAgent import BaseAgent
from app.ai_models import chat_model
from app.agents.EmotionAgent import EmotionAgent
from app.agents.RagAgent import RagAgent



class ActionSuggestionAgent(BaseAgent):

    @staticmethod
    async def hint(intent: str, emotion: str, decide:str) -> str:
        messages = [
            SystemMessage(content='Ты учитель - даёшь точные краткие советы которые всегда работают'),
            HumanMessage(content=f'''Проанализировав текст ответь на вопросы: что ответить человеку, каким тоном, 
                                 и какое действие выполнить опираясь на целль - {intent} и эмоции - Х+{emotion} и используя готовое решение {decide}'''),
        ]
        response = await chat_model.apredict_messages(messages)
        return response.content

    async def run(self, query: str, context : str ="") -> str:

        intent = IntentAgent()
        end_intent = await intent.get_intent(query)

        emot = EmotionAgent()
        end_emot = await emot.detert_emotion(query)

        answer = RagAgent()
        end_answer = await answer.run(query, context)

        end_hint = await self.hint(end_intent, end_emot, end_answer)

        print(f'[end_hint]: {end_hint}')

        return end_hint





