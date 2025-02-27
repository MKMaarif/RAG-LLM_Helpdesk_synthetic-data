import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import sqlite3
import pandas as pd
from langchain_openai import OpenAIEmbeddings
import faiss
from langchain.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from llama_index.llms.groq import Groq

import db_config as db

# Set up Streamlit UI
st.set_page_config(page_title="AI Assistant X-3000 Helpdesk")
st.title("🤖 AI Assistant X-3000 Helpdesk")

# Database path
SQL_DB_PATH = "database/csv_database.db"
FAISS_INDEX_PATH = "database/faiss_index"

# load model embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# Initialize session state variables
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize FAISS index
try:
    st.session_state.vector_store = FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
except FileNotFoundError:
    st.session_state.vector_store = db.initialize_faiss_index()

# Initialize sql database
if not os.path.exists(SQL_DB_PATH):
    db.initialize_sql_db(SQL_DB_PATH)

# Initialize LLM
groq_api_key = os.getenv("GROQ_API_KEY")
llm = llm = Groq(model="llama-3.1-8b-instant", api_key=groq_api_key)

# Prompt Template
PROMPT_TEMPLATE ="""
    Jawab pertanyaan berdasarkan konteks dari PDF berikut: 

    {context}

    ---

    **Pertanyaan:**
    {question}

    ---
    Hanya lanjutkan ke bagian di bawah ini jika benar-benar tidak ada informasi spesifik dalam konteks.
    Jika pertanyaan yang diberikan terkait data riwayat penggunaan dan tidak ada informasi spesifik dalam konteks, jawablah dengan **SQL query** yang sesuai dengan contoh tabel berikut:

    **Nama Tabel:** `synthetic_data`

    **Contoh Data dalam Tabel (Format JSON, hanya contoh, tidak digunakan langsung dalam query):**
    ```json
    [
        {{"interaction_id":1,"user_id":447,"timestamp":"2024-03-12 17:56:48","device_type":"Smart Speaker","command_category":"Information","command_text":"Apa rekomendasi restoran di sekitar sini?","ai_response":"Akses ditolak","response_time_ms":310,"ai_confidence_score":67.97,"user_satisfaction":4,"status":"Error","error_code":"ERR403"}},
        {{"interaction_id":2,"user_id":469,"timestamp":"2024-12-01 06:40:13","device_type":"Smartphone","command_category":"Productivity","command_text":"Bagikan agenda meeting dengan anggota tim","ai_response":"Tugas telah disimpan","response_time_ms":315,"ai_confidence_score":70.04,"user_satisfaction":5,"status":"Success","error_code":null}}
    ]
    ```
    Hanya jawab query SQL dalam bentuk string, tanpa memberi jawaban yang lain.

    ---
    Hanya jawab query SQL, jika tidak ada data yang sesuai dalam konteks.
"""

PROMPT_DB = """
    Jawab pertanyaan berdasarkan hasil query SQL yang diberikan di bawah ini:
    {sql_query_result}

    ---
    Jawab pertanyaan berikut:
    {question}

    Jawab tanpa menyebutkan penggunaan query SQL, tetapi parafrase pertanyaan untuk memberi jawaban yang natural.
"""

def query_retrieval(question: str):
    # Search vector store
    results = st.session_state.vector_store.similarity_search(question, k=5)
    if not results:
        return "Maaf, saya tidak menemukan informasi yang relevan dalam dokumen."

    context_text = '\n\n---\n\n'.join(doc.page_content for doc in results)

    # Prepare prompt with clear formatting
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=question)

    # Generate response using LLM
    response = llm.complete(prompt)
    response = str(response)

    # Validate if response contains an SQL query
    if "synthetic_data" in response:  
        # Take SQL query from response
        response = response.split("```sql")[1].strip()
        response = response.split("```")[0].strip()

        try:
            # Connect to SQLite database
            conn = sqlite3.connect(SQL_DB_PATH)

            # Execute SQL query safely
            sql_query_result = pd.read_sql_query(response, conn)
            conn.close()

            # If DataFrame is empty, return error message
            if sql_query_result.empty:
                return "Tidak ada hasil yang ditemukan."

            # Convert DataFrame to JSON format string
            query_result_str = sql_query_result.to_json(orient="records")

            # Prepare second-stage prompt (SQL result → natural language)
            prompt_db = ChatPromptTemplate.from_template(PROMPT_DB)
            final_prompt = prompt_db.format(sql_query_result=query_result_str, question=question)

            # Generate final response
            response = llm.complete(final_prompt)

            return response
        
        except sqlite3.Error as e:
            return f"Terjadi kesalahan SQL: {e}"
    
    return response

# Chatbot UI
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Tanyakan sesuatu kepada AI Assistant X-3000 Helpdesk!", max_chars=1000):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Mengolah jawaban..."):
        response = query_retrieval(prompt)

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})