from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.config import config
import uvicorn
import httpx

app = FastAPI()


class EmbeddingRequest(BaseModel):
    model: str
    input: str


class EmbeddingResponse(BaseModel):
    embedding: list


@app.post("/embed", response_model=EmbeddingResponse)
async def get_embedding(request: EmbeddingRequest):
    headers = {
        "Authorization": f"Bearer {config.openai_token}",
        "Content-Type": "application/json",
    }
    payload = {"model": request.model, "input": request.input}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{config.openai_endpoint}/embeddings", headers=headers, json=payload
        )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    data = response.json()
    embedding = data.get("embedding")
    if embedding is None:
        raise HTTPException(
            status_code=500, detail="Не удалось получить эмбеддинг из ответа API"
        )

    return EmbeddingResponse(embedding=embedding)


@app.get("/.well-known/ready")
async def ready():
    return {"status": "ready"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3001)
