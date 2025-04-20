from fastapi import APIRouter
from app.agents import EmotionAgent

router = APIRouter(prefix="/emotion")
agent = EmotionAgent()


@router.get("/query-agent")
async def request(text: str):
    result = await agent.run(query=text)
    return {"message": result}
