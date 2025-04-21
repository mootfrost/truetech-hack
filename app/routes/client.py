from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from sqlalchemy import select
from app.deps import get_session
from app.models import Dialog, Client

router = APIRouter(prefix='/client')


@router.get('/')
async def get_client(id: int = Query(None), phone: int = Query(None), session: AsyncSession = Depends(get_session)):
    stmt = select(Client)
    if id:
        stmt = stmt.where(Client.id == id)
    elif phone:
        stmt = stmt.where(Client.phone == phone)
    result = await session.execute(stmt)
    client = result.scalar_one_or_none()
    if not client:
        raise HTTPException(status_code=404, detail='Client not found')
    return client
