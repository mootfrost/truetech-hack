from pydantic_settings import BaseSettings


class Config(BaseSettings):
    openai_token: str
    openai_endpoint: str
    weaviate_url: str
    weaviate_api_key: str
    embedding_model: str
    chat_model: str



config = Config(_env_file='.env')

__all__ = ['config']