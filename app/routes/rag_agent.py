from fastapi import APIRouter, UploadFile, File, Form
from app.agents import RagAgent


router = APIRouter(prefix="/rag")
agent = RagAgent()


@router.post("/upload")
async def upload_doc(file: UploadFile = File(...)):
    result = await agent.docs_from_file(file)
    return {"message": result}


@router.post("/query-agent")
async def query_agent(query: str = Form(...)):
    answer = await agent.run(query)
    return {"answer": answer}
