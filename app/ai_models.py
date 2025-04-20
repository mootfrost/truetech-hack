from langchain_openai.chat_models import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings

from app.config import config


embedding_model = OpenAIEmbeddings(
    openai_api_key=config.openai_token,
    openai_api_base=config.openai_endpoint,
    model=config.embedding_model,
)

chat_model = ChatOpenAI(
    openai_api_key=config.openai_token,
    openai_api_base=config.openai_endpoint,
    model_name=config.chat_model,
    temperature=0
)