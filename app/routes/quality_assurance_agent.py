from fastapi import APIRouter
from app.agents import QualityAssuranceAgent

router = APIRouter(prefix="/quality")



@router.get("/query-agent")
async def request(text: str):
    agent = QualityAssuranceAgent()
    result = await agent.run(query=text)
    return {"message": result}
