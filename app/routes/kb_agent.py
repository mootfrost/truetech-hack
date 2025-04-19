from fastapi import APIRouter


router = APIRouter(prefix='/rag')


@router.get('/')
async def status():
    return {'message': 'kb agent'}


__all__ = ['router']