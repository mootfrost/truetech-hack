from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class AgentContext:
    message_history: str
    user_data: str

class BaseAgent(ABC):
    @abstractmethod
    async def run(self, query: str, context: AgentContext | None) -> str:
        pass



