from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
import httpx

from app.agents import RagAgent
from app.config import config


router = APIRouter(prefix='/rag')


@router.post('/upload')
async def upload_doc(file: UploadFile = File(...)):
    rag_agent = RagAgent()
    result = await rag_agent.docs_from_file(file)
    return {"message": result}


@router.post('/query-agent')
async def query_agent(query: str = Form(...)):
    rag_agent = RagAgent()
    answer = await rag_agent.run(query)
    return {'answer': answer}
