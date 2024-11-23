import os
from pathlib import Path
import streamlit as st
from langchain_community.vectorstores import FAISS  # Updated import for FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain_together import Together
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationalRetrievalChain

# Streamlit Page Configuration
st.set_page_config(page_title="LawGPT")

# Header Image
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.image("https://github.com/harshitv804/LawGPT/assets/100853494/ecff5d3c-f105-4ba2-a93a-500282f0bf00")

# CSS Styling
st.markdown(
    """
    <style>
    div.stButton > button:first-child {
        background-color: #ffd0d0;
    }
    div.stButton > button:active {
        background-color: #ff6262;
    }
    #MainMenu, footer {visibility: hidden;}
    button[title="View fullscreen"] {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Reset Conversation Function
def reset_conversation():
    st.session_state.messages = []
    st.session_state.memory.clear()

# Initialize Session States
if "messages" not in st.session_state:
    st.session_state.messages = []

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferWindowMemory(k=2, memory_key="chat_history", return_messages=True)

# Load Embeddings and FAISS Index
try:
    embeddings = HuggingFaceEmbeddings(
        model_name="nomic-ai/nomic-embed-text-v1",
        model_kwargs={"trust_remote_code": True, "revision": "289f532e14dbbbd5a04753fa58739e9ba766f3c7"},
    )

    index_path = Path("ipc_vector_db/index.faiss")
    if not index_path.exists():
        st.error("FAISS index not found. Please generate it first and place it in 'ipc_vector_db'.")
        st.stop()

    db = FAISS.load_local("ipc_vector_db", embeddings, allow_dangerous_deserialization=True)
    db_retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 4})
except Exception as e:
    st.error(f"Error loading FAISS index or embeddings: {str(e)}")
    st.stop()

# Define Prompt
prompt_template = """<s>[INST]This is a chat template and as a legal chatbot specializing in Indian Penal Code queries, your objective is to provide accurate and concise information.
CONTEXT: {context}
CHAT HISTORY: {chat_history}
QUESTION: {question}
ANSWER:
</s>[INST]"""
prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question", "chat_history"])

# LLM Setup
TOGETHER_AI_API = os.getenv("TOGETHER_AI_API", "your_default_key_here")
if TOGETHER_AI_API == "your_default_key_here":
    TOGETHER_AI_API = st.text_input("Enter your Together.ai API key:", type="password")
    if not TOGETHER_AI_API:
        st.warning("Please set the `TOGETHER_AI_API` environment variable.")
        st.stop()

llm = Together(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    temperature=0.5,
    max_tokens=1024,
    together_api_key=TOGETHER_AI_API,
)

# Conversational Chain
try:
    qa = ConversationalRetrievalChain.from_llm(
        llm=llm,
        memory=st.session_state.memory,
        retriever=db_retriever,
        combine_docs_chain_kwargs={"prompt": prompt},
    )
except Exception as e:
    st.error(f"Error setting up the conversational chain: {str(e)}")
    st.stop()

# Display Previous Messages
for message in st.session_state.messages:
    with st.chat_message(message.get("role")):
        st.write(message.get("content"))

# Chat Input
input_prompt = st.chat_input("Ask a question")
if input_prompt:
    with st.chat_message("user"):
        st.write(input_prompt)
    st.session_state.messages.append({"role": "user", "content": input_prompt})

    with st.chat_message("assistant"):
        with st.spinner("Thinking 💡..."):
            try:
                result = qa.invoke(input=input_prompt)
                full_response = "⚠️ **_Note: Information provided may be inaccurate._** \n\n\n"
                full_response += result["answer"]
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": result["answer"]})
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Reset Button
st.button("Reset All Chat 🗑️", on_click=reset_conversation)
