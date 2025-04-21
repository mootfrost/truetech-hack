from langchain_openai.chat_models import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import config
from app.db import async_session


embedding_model = OpenAIEmbeddings(
    openai_api_key=config.openai_token,
    openai_api_base=config.openai_endpoint,
    model=config.embedding_model,
)

chat_model = ChatOpenAI(
    openai_api_key=config.openai_token,
    openai_api_base=config.openai_endpoint,
    model_name=config.chat_model,
    temperature=0,
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
