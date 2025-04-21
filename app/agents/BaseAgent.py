from abc import ABC, abstractmethod


class BaseAgent(ABC):
    @abstractmethod
    async def run(self, query: str, context: dict = None) -> str:
        pass
