import weaviate
from langchain_weaviate.vectorstores import WeaviateVectorStore
from langchain.chains import RetrievalQA
import tempfile
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
import os
from app.agents.BaseAgent import BaseAgent
from langchain.prompts import PromptTemplate
from tiktoken import get_encoding


from app.deps import embedding_model, chat_model
from app.config import config


class RagAgent(BaseAgent):
    def __init__(self):
        self.client = weaviate.connect_to_local(port=config.weaviate.http_port,
                                                grpc_port=config.weaviate.grpc_port,
                                                host=config.weaviate.host)

        self.vectorstore = WeaviateVectorStore(
            client=self.client,
            index_name='Document',
            text_key='content',
            embedding=embedding_model
        )

        self.prompt = PromptTemplate(
            template='Предоставь чистый ответ, не пиши ничего лишноего, только ответ на вопрос'
                     'Контекст: {context}\n'
                     'Вопрос: {question}',
            input_variables=["context", "question"]
        )

    async def run(self, query: str, context: dict = None) -> str:
        retriever = self.vectorstore.as_retriever()
        chain = RetrievalQA.from_chain_type(
            llm=chat_model,
            retriever=retriever,
            chain_type='stuff',
            chain_type_kwargs={
                'prompt': self.prompt
            }
        )
        return chain.run(query)

    @staticmethod
    def batch_documents(docs, batch_size):
        for i in range(0, len(docs), batch_size):
            yield docs[i:i + batch_size]

    def num_tokens(self, text, model_name="cl100k_base"):
        encoding = get_encoding(model_name)
        return len(encoding.encode(text))

    def batch_by_token_limit(self, docs, token_limit=8192):
        batch = []
        total_tokens = 0
        for doc in docs:
            tokens = self.num_tokens(doc.page_content)
            if total_tokens + tokens > token_limit and batch:
                yield batch
                batch = []
                total_tokens = 0
            batch.append(doc)
            total_tokens += tokens
        if batch:
            yield batch

    async def docs_from_file(self, file):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        loader = TextLoader(tmp_path, encoding='utf-8')
        documents = loader.load()
        os.remove(tmp_path)

        splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=500, separators=['},', '}\n'])
        docs = splitter.split_documents(documents)
        print(len(docs))
        for batch in self.batch_by_token_limit(docs, token_limit=8192):
            await self.vectorstore.aadd_documents(batch)
        return {'chunks': len(docs), 'status': 'ok'}
