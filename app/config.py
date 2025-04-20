from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


class WeaviateConfig(BaseModel):
    host: str
    http_port: int
    grpc_port: int = 50051


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_nested_max_split=1,
                                      env_nested_delimiter='_')

    db_string: str

    openai_token: str
    openai_endpoint: str
    weaviate: WeaviateConfig
    embedding_model: str
    chat_model: str



config = Config(_env_file='.env')

__all__ = ['config']