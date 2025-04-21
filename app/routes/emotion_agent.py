from fastapi import APIRouter
from app.agents import EmotionAgent

router = APIRouter(prefix="/emotion")



@router.get("/query-agent")
async def request(text: str):
    agent = EmotionAgent()
    result = await agent.run(query=text)
    return {"message": result}
