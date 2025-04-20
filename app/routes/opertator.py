from fastapi import APIRouter


router = APIRouter(prefix='/op')



@router.get('/recommend')
async def get_recommendations(question: str):
    pass




