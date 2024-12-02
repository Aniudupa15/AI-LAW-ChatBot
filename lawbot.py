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
TOGETHER_AI_API = os.getenv("TOGETHER_AI_API")
if not TOGETHER_AI_API:
    raise RuntimeError("TOGETHER_AI_API key is missing. Set it in the environment variables.")

# Lazy loading of embeddings and FAISS index
try:
    embeddings = HuggingFaceEmbeddings(
        model_name="nomic-ai/nomic-embed-text-v1",
        model_kwargs={"trust_remote_code": True, "revision": "289f532e14dbbbd5a04753fa58739e9ba766f3c7"},
    )
    index_path = Path("models/index.faiss")
    if not index_path.exists():
        raise FileNotFoundError("FAISS index not found. Please ensure the file exists in the 'models' directory.")
    db = FAISS.load_local("models", embeddings)
    db_retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 4})
except Exception as e:
    raise RuntimeError(f"Error initializing embeddings or FAISS index: {str(e)}")

# Prompt Template
prompt_template = """<s>[INST]This is a chat template and as a legal chatbot specializing in Indian Penal Code queries, your objective is to provide accurate and concise information.
CONTEXT: {context}
CHAT HISTORY: {chat_history}
QUESTION: {question}
ANSWER:
</s>[INST]"""
prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question", "chat_history"])

# LLM Setup (Ensure Together.ai key is valid)
try:
    llm = Together(
        model="mistralai/Mistral-7B-Instruct-v0.2",
        temperature=0.5,
        max_tokens=1024,
        together_api_key=TOGETHER_AI_API,
    )
except Exception as e:
    raise RuntimeError(f"Error initializing LLM: {str(e)}")

# Memory for Conversational Context
memory = ConversationBufferWindowMemory(k=2, memory_key="chat_history", return_messages=True)

# Conversational Chain
try:
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        memory=memory,
        retriever=db_retriever,
        combine_docs_chain_kwargs={"prompt": prompt},
    )
except Exception as e:
    raise RuntimeError(f"Error creating conversational chain: {str(e)}")

# Input Schema
class ChatRequest(BaseModel):
    question: str
    chat_history: str

@router.post("/chat/")
async def chat(request: ChatRequest):
    try:
        inputs = {"question": request.question, "chat_history": request.chat_history}
        result = qa_chain(inputs)
        return {"answer": result.get("answer", "No answer provided.")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@router.get("/")
async def root():
    return {"message": "LawGPT API is running."}
