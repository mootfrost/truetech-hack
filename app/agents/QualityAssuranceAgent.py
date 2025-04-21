from langchain.schema import SystemMessage, HumanMessage
from app.agents.BaseAgent import BaseAgent
from app.deps import chat_model
import logging
import re

logger = logging.getLogger("uvicorn.error")


class QualityAssuranceAgent(BaseAgent):

    @staticmethod
    def preprocess(text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^\w\s]", "", text)
        return text.strip()

    @staticmethod
    async def text_grade(text: str) -> str:
        messages = [
            SystemMessage(
                content="Ты корректор скурпулёзно  ищущий ошибки в тексте выводя только ошибки без вариантов решения"
            ),
            HumanMessage(content=f".объясни ошибки в тексте: {text}."),
        ]
        response = await chat_model.apredict_messages(messages)
        return response.content

    @staticmethod
    async def psyhology_grade(text:str, last_rext:str="где мой заказ") -> str:
        messages = [
            SystemMessage(
                content="Ты ищешь психологичесую некорректностью ответа выводя только ошибки без вариантов решения"
            ),
            HumanMessage(content=f"объясни ошибки в: {text} ответа на вопрос: {last_rext} выводя только ошибки без вариантов решения"),
        ]
        response = await chat_model.apredict_messages(messages)
        return response.content

    @staticmethod
    async def chose_main_problem(text_problem:str, psyhology_problem:str) -> str:
        messages = [
            SystemMessage(
                content="Ты вычленияешь и суммируешь основные ошибки из всех всего 3 основные ошибки"
            ),
            HumanMessage(content=f"разбери ошибки связанные с текстом {text_problem} и ошибки с психологией {psyhology_problem}"),
        ]
        response = await chat_model.apredict_messages(messages)
        return response.content

    @staticmethod
    async def make_last_answer(main_problem, text):
        messages = [
            SystemMessage(
                content="Дыть итоговую оценку тексу, основываясь на главных ошибках"
            ),
            HumanMessage(content=f"используя ошибки {main_problem} из текста {text} измени на подходящий вариант"),
        ]
        response = await chat_model.apredict_messages(messages)
        return response.content


    async def run(self, query: str, context: dict = None) -> str:
        user_info = None
        mistake_finder = await self.text_grade(query)
        etn_finder = await self.psyhology_grade(query)
        sum_m = await self.chose_main_problem(mistake_finder, etn_finder)
        last_ans = await self.make_last_answer(sum_m, query)
        print(last_ans)
        return last_ans

