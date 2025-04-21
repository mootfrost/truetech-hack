from langchain.schema import SystemMessage, HumanMessage
from app.agents.IntentAgent import IntentAgent
from app.agents.BaseAgent import BaseAgent, AgentContext
from app.deps import chat_model
from app.agents.EmotionAgent import EmotionAgent
from app.agents.RagAgent import RagAgent


class ActionSuggestionAgent(BaseAgent):
    @staticmethod
    async def hint(intent: str, emotion: str, decide: str) -> str:
        messages = [
            SystemMessage(
                content="Ты учитель - даёшь точные краткие советы которые всегда работают"
            ),
            HumanMessage(
                content=f"""Проанализировав текст ответь на вопросы: что ответить человеку, каким тоном, 
                                 и какое действие выполнить опираясь на целль - {intent} и эмоции - Х+{emotion} и используя готовое решение {decide}. Не говори ничего лишнего, только чистый ответ на вопрос пользователя, который сразу покажется ему. Например, не пиши, например, "Чтобы ответить на вопрос" или "Ответ", сразу отыечай на вопрос"""
            ),
        ]
        response = await chat_model.apredict_messages(messages)
        return response.content

    async def run(self, query: str, context: AgentContext | None) -> str:
        intent = IntentAgent()
        end_intent = await intent.run(query, context)
        emot = EmotionAgent()
        end_emot = await emot.run(query, context)
        answer = RagAgent()
        end_answer = await answer.run(query, context)

        # end_hint = await self.hint(end_intent, end_emot, end_answer)

        # print(f'[end_hint]: {end_hint}')

        return end_intent, end_emot, end_answer
