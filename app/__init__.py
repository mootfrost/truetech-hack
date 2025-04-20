from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.routes import kb_agent_router
import uvicorn


log_config = uvicorn.config.LOGGING_CONFIG
log_config['formatters']['access']['fmt'] = '%(asctime)s - %(levelname)s - %(message)s'
log_config['formatters']['default']['fmt'] = '%(asctime)s - %(levelname)s - %(message)s'
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(kb_agent_router)



__all__ = ['app', 'log_config']