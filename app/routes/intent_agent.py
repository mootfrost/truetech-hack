from fastapi import APIRouter
from app.agents import IntentAgent

router = APIRouter(prefix="/intent")


@router.get("/query-agent")
async def request(text: str):
    agent = IntentAgent()
    result = await agent.run(query=text)
    return {"message": result}
