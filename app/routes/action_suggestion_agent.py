from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Client, Dialog
from app.agents import ActionSuggestionAgent, AgentContext
from app.deps import get_session
from pydantic import BaseModel

import json
import logging

logger = logging.getLogger("uvicorn.error")

router = APIRouter(prefix="/suggest")


class QueryAgentRequest(BaseModel):
    question: str
    client_id: int | None = None
    dialog_id: int | None = None


@router.post("/query-agent")
async def request(req: QueryAgentRequest, session: AsyncSession = Depends(get_session)):
    context = None
    if req.dialog_id:
        convo = await session.get(Dialog, req.dialog_id)
        print(convo.client_id)
        if not convo:
            raise HTTPException(status_code=404, detail='Dialog not found')
        client = await session.get(Client, convo.client_id)
        context = AgentContext('\n'.join(convo.messages), str(client.to_human_readable()))
    elif req.client_id:
        client = await session.get(Client, req.client_id)
        context = AgentContext('', str(client.to_human_readable()))

    agent = ActionSuggestionAgent()
    intent, emote, result, qa_analys = await agent.run(query=req.question, context=context)
    try:
        parse = json.loads(emote)
    except:
        parse = {'emotion_force': 50, 'emotion': ''}
        logger.error("FAILED TO PARSE EMOTION", emote)

    return {
        'intent': intent,
        'emotion_force': parse.get('emotion_force') or 50,
        'emotion': parse.get('emotion') or 'спокоен',
        'answer': result,
        'qa': qa_analys
    }
