from fastapi import APIRouter
from app.agents import ActionSuggestionAgent

router = APIRouter(prefix='/acti')
agent = ActionSuggestionAgent()


@router.get('/query-agent')
async def request(text: str, id: str):
    result = await agent.run(query=text, context=id)
    return {'message': result}
