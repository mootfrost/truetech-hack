import weaviate
from langchain_weaviate.vectorstores import WeaviateVectorStore
from langchain.chains import RetrievalQA
import tempfile
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
import os

from app.ai_models import embedding_model, chat_model
from app.config import config


class RagAgent:
    def __init__(self):
        self.client = weaviate.connect_to_local(port=3002)

        self.vectorstore = WeaviateVectorStore(
            client=self.client,
            index_name="Document",
            text_key="content",
            embedding=embedding_model
        )

    async def run(self, query: str, context: str = "") -> str:
        retriever = self.vectorstore.as_retriever()
        chain = RetrievalQA.from_chain_type(llm=chat_model, retriever=retriever)
        return chain.run(query)

    @staticmethod
    def batch_documents(docs, batch_size):
        for i in range(0, len(docs), batch_size):
            yield docs[i:i + batch_size]

    async def docs_from_file(self, file):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        loader = TextLoader(tmp_path, encoding="utf-8")
        documents = loader.load()
        os.remove(tmp_path)

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = splitter.split_documents(documents)
        batch_size = 128
        for batch in self.batch_documents(docs, batch_size):
            await self.vectorstore.aadd_documents(batch)
        return {'chunks': len(docs), 'status': 'ok'}
