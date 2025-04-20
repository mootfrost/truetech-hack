import uvicorn

from app.config import config
from app import app, log_config

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080, log_config=log_config)