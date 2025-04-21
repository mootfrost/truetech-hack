from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from sqlalchemy import select
from app.deps import get_session
from app.models import Dialog


router = APIRouter(prefix='/dialog')


class CreateDialogRequest(BaseModel):
    client_id: int | None = None


@router.post('/create')
async def create_dialog(req: CreateDialogRequest, session: AsyncSession = Depends(get_session)):
    dialog = Dialog(
        client_id=req.client_id or 1,
        messages=[]
    )
    session.add(dialog)
    await session.commit()
    await session.refresh(dialog)
    return dialog


class UpdateDialogRequest(BaseModel):
    dialog_id: int
    message: str


@router.post('/update')
async def update_dialog(req: UpdateDialogRequest, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Dialog).where(Dialog.id == req.dialog_id))
    dialog = result.scalar_one_or_none()

    if dialog is None:
        raise HTTPException(status_code=404, detail='Dialog not found')

    dialog.messages.append(req.message)
    await session.commit()
    await session.refresh(dialog)
    return dialog


@router.get('/{id}')
async def get_dialog(id: int, session: AsyncSession = Depends(get_session)):
    res = await session.get(Dialog, id)
    if not res:
        raise HTTPException(status_code=404, detail='Dialog not found')
    return dialog