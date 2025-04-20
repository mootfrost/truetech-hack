from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import User
from app.agents import ActionSuggestionAgent
from app.deps import get_session
from pydantic import BaseModel

import json
import logging

logger = logging.getLogger('uvicorn.error')

router = APIRouter(prefix='/suggest')
agent = ActionSuggestionAgent()


class QueryAgentRequest(BaseModel):
    question: str
    id: int | None = None
    phone: str | None = None


@router.post('/query-agent')
async def request(req: QueryAgentRequest, session: AsyncSession = Depends(get_session)):
    context = None
    if req.id is not None:
        result = await session.execute(select(User).where(User.id == req.id))
        user = result.scalar_one_or_none()
        if user:
            context = {'user': user.to_human_readable()}
    elif req.phone is not None:
        result = await session.execute(select(User).where(User.phone == req.phone))
        user = result.scalar_one_or_none()
        if user:
            context = {'user': user.to_human_readable()}

    intent, emote, result = await agent.run(query=req.question, context=context)
    try:
        force = json.loads(emote)['emotion_force']
    except:
        force = 50
        logger.error('FAILED TO PARSE EMOTION', emote)
    return {
        'intent': intent,
        'emotion': force,
        'suggestion': result,
    }
