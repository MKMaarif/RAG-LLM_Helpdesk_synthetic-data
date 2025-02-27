from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_openai import OpenAIEmbeddings
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from uuid import uuid4
import sqlite3
import pandas as pd
import os

PDF_PATH = "files/M. Khoirul Ma'arif_synthetic_data_backup.pdf"
CSV_PATH = "files/M. Khoirul Ma'arif_synthetic_data.csv"

# VECTOR DATABASE
# load pdf
def load_pdf():
    doc_loader = PyPDFLoader(PDF_PATH)
    documents = doc_loader.load()
    for i in range(len(documents)):
        documents[i].page_content = ' '.join(documents[i].page_content.split())
    return documents

# Split documents into pages
def split_documents(documents: list[Document]):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False
    )
    return splitter.split_documents(documents)

# Custom function to calculate chunk ids
def calculate_chunk_ids(chunks):
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0
            
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        chunk.metadata["chunk_id"] = chunk_id

    return chunks

# Initialize FAISS index
def initialize_faiss_index():
    if os.path.exists("database/faiss_index"):
        os.remove("database/faiss_index")

    # Load documents
    documents = load_pdf()
    chunks = split_documents(documents)
    chunks = calculate_chunk_ids(chunks)

    # Initialize FAISS index
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    index = faiss.IndexFlatL2(len(embeddings.embed_query("hello world")))

    # Create FAISS vector store
    vector_store = FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )
    uuids = [str(uuid4()) for _ in range(len(chunks))]

    # Add documents to FAISS index
    vector_store.add_documents(documents=chunks, uuids=uuids)
    
    return vector_store

# SQL DATABASE
def initialize_sql_db(SQL_DB_PATH):
    # read csv
    df = pd.read_csv(CSV_PATH)

    # Create SQLite database
    conn = sqlite3.connect(SQL_DB_PATH)
    df.to_sql("synthetic_data", conn, if_exists="replace", index=False)
    conn.close()

    return