from fastapi import APIRouter
from app.agents import IntentAgent

router = APIRouter(prefix='/intent')
agent = IntentAgent()


@router.get('/query-agent')
async def request(text: str, id: str):
    result = await agent.run(query=text, context=id)
    return {'message': result}
