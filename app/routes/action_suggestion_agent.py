from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import User
from app.agents import ActionSuggestionAgent
from app.deps import get_session

router = APIRouter(prefix='/suggest')
agent = ActionSuggestionAgent()


@router.get('/query-agent')
async def request(text: str, id: int | None = None, phone: str | None = None, session: AsyncSession = Depends(get_session)):
    context = None
    if id is not None:
        result = await session.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()
        if user:
            context = {'user': user.to_human_readable()}
    elif phone is not None:
        result = await session.execute(select(User).where(User.phone == phone))
        user = result.scalar_one_or_none()
        if user:
            context = {'user': user.to_human_readable()}
    print(context['user'])

    result = await agent.run(query=text, context=context)
    return {'message': result}
