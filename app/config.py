from pydantic import BaseSettings


class Config(BaseSettings):
    mws_token: str


config = Config(_env_file='.env')

__all__ = ['config']