from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain_together import Together
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationalRetrievalChain
import os

router = APIRouter()

# API Key for Together.ai
TOGETHER_AI_API = os.getenv("TOGETHER_AI_API", "1c27fe0df51a29edee1bec6b4b648b436cc80cf4ccc36f56de17272d9e663cbd")

# Lazy loading of large models (only load embeddings and index when required)
embeddings = HuggingFaceEmbeddings(
    model_name="nomic-ai/nomic-embed-text-v1",
    model_kwargs={"trust_remote_code": True, "revision": "289f532e14dbbbd5a04753fa58739e9ba766f3c7"},
)
index_path = Path("ipc_vector_db/index.faiss")
if not index_path.exists():
    raise FileNotFoundError("FAISS index not found. Please generate it and place it in 'ipc_vector_db'.")
db = FAISS.load_local("ipc_vector_db", embeddings, allow_dangerous_deserialization=True)
db_retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 4})

# Prompt Template
prompt_template = """<s>[INST]This is a chat template and as a legal chatbot specializing in Indian Penal Code queries, your objective is to provide accurate and concise information.
CONTEXT: {context}
CHAT HISTORY: {chat_history}
QUESTION: {question}
ANSWER:
</s>[INST]"""
prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question", "chat_history"])

# LLM Setup (Mistral-7B can be memory-heavy; ensure you're using it wisely)
llm = Together(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    temperature=0.5,
    max_tokens=1024,
    together_api_key=TOGETHER_AI_API,
)

# Memory for Conversational Context
memory = ConversationBufferWindowMemory(k=2, memory_key="chat_history", return_messages=True)

# Conversational Chain
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    memory=memory,
    retriever=db_retriever,
    combine_docs_chain_kwargs={"prompt": prompt},
)

# Input Schema
class ChatRequest(BaseModel):
    question: str
    chat_history: str

@router.post("/chat/")
async def chat(request: ChatRequest):
    try:
        inputs = {"question": request.question, "chat_history": request.chat_history}
        result = qa_chain(inputs)
        return {"answer": result["answer"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@router.get("/")
async def root():
    return {"message": "LawGPT API is running."}
