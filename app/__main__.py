import uvicorn
from app import app, log_config
from app.config import config

if __name__ == "__main__":
    uvicorn.run(
        app, host="0.0.0.0", port=config.api_port, log_config=log_config, log_level="debug"
    )
