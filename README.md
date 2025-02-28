
# 🤖 AI Assistant X-3000 Helpdesk Chatbot

This is a **Retrieval-Augmented Generation (RAG) chatbot** built with **Streamlit, FAISS, and SQLite**, powered by **LLaMA-3.1-8B-instant** from Groq API. The chatbot retrieves relevant information from a synthetic **PDF document** and **structured CSV dataset**, generating responses based on the **best available context**.
---

## 🔗 Deployment Link
[https://rag-llm-app-desk-aagspmk7srfw7joxukqvlt.streamlit.app]

---

## 📌 Features
✅ **Retrieval-Augmented Generation (RAG)**: Combines structured and unstructured data retrieval.  
✅ **Vector Database (FAISS)**: Retrieves text from a **50+ page PDF** using embeddings.  
✅ **SQL Querying**: Fetches structured **historical data** from a **CSV-based SQLite database**.  
✅ **LLM Integration**: Uses **LLaMA-3.1-8B-instant via Groq API** to generate responses.  
✅ **Interactive UI**: Built with **Streamlit** for a user-friendly chatbot interface.  

---

## 🚀 **Installation Guide**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/MKMaarif/RAG-LLM_Helpdesk_synthetic-data.git
cd MKMaarif/RAG-LLM_Helpdesk_synthetic-data
```

### **2️⃣ Set Up Python Environment**
Ensure you have Python **3.10+** installed. Then, create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### **3️⃣ Install Dependencies**
Install all required Python packages:

```bash
pip install -r requirements.txt
```

Alternatively, manually install dependencies:

```bash
pip install streamlit langchain openai faiss-cpu sentence-transformers pandas sqlite3 pymupdf
```

### **4️⃣ Set Up Environment Variables**
Create a `.env` file in the root directory and add your **Groq API Key**:

```env
GROQ_API_KEY=your_groq_api_key
```

### **4️⃣ Set Up Secrets Variables for Streamlit**
Create a `secrets.toml` file in the `.streamlit` directory and add your **Groq API Key**:

```toml
GROQ_API_KEY=your_groq_api_key
```

---

## 🛠 **How to Run the Chatbot**

Run the **Streamlit app**:
```bash
streamlit run app.py
```

The chatbot will be accessible at:
```
http://localhost:8501
```

---

## 📜 **Project Structure**
```bash
.
├── app.py               # Streamlit chatbot application
├── db_config.py         # FAISS & SQL database initialization
├── database/
│   ├── faiss_index      # FAISS vector database (auto-generated)
│   ├── csv_database.db  # SQLite database (auto-generated)
├── notebook/
│   ├── display_graph.ipynb   # Display graph for synthetic pdf document
│   ├── generate_table.ipynb  # Create synthetic CSV dataset
│   ├── llm_with_rag.ipynb    # Notebook for LLM understanding
│   ├── rag_system.ipynb      # Building RAG database
├── files/
│   ├── synthetic_data.pdf  # PDF document
│   ├── synthetic_data.csv  # CSV dataset
├── .env                 # API Key (ignored in git)
├── requirements.txt      # Dependencies
└── README.md            # Documentation
```

---

## 🎯 **How It Works**
1. **User asks a question** in the chat.
2. **FAISS vector search** finds relevant text chunks from the **PDF document**.
3. If needed, the **chatbot queries SQL** for structured data.
4. The **LLM (LLaMA-3.1-8B) processes** the retrieved context to generate a response.
5. The **response is displayed** in the Streamlit chatbot UI.

---

## 📌 **Example Queries**
Try asking:
- "Apa fitur utama AI Assistant X-3000?"
- "Bagaimana cara troubleshooting jika AI tidak merespons perintah suara?"
- "Kategori perintah apa yang sering digunakan pengguna?"
- "Berapa persentase error yang dialami pengguna sebelumnya?"
- "Berapa rata-rata kepuasan pengguna AI Assistant X-3000 sebelumnya?"
- "Jelaskan cara menghubungkan AI Assistant X-3000 ke Wi-Fi."
- "Apa teknologi yang digunakan untuk pengenalan wajah AI Assistant X-3000?"
- "Apa langkah pemeliharaan rutin AI Assistant X-3000?"
- "Jelaskan perbedaan AI Assistant X-3000 dengan model sebelumnya."
- "Apa manfaat AI Assistant X-3000 dalam smart home?"

---

## ⚡ **Troubleshooting**
### **Common Issues & Fixes**
| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError: No module named 'streamlit'` | Run `pip install -r requirements.txt` |
| `FileNotFoundError: database/faiss_index not found` | Run `python db_config.py` first |
| `sqlite3.OperationalError: no such table: synthetic_data` | Ensure `csv_database.db` exists and is populated |
| `OpenAI API Key Error` | Ensure `.env` file is correctly set with `GROQ_API_KEY` |

---

## 🌍 **Deployment**
To deploy on **Hugging Face Spaces or Vercel**, follow these steps:
1. **Deploy FAISS + SQLite as a backend service** (FastAPI recommended).
2. **Deploy Streamlit UI separately** using Hugging Face Spaces.

---

## 🎉 **Contributing**
Feel free to **fork this project** and submit **pull requests** to improve the chatbot!

👨‍💻 Developed by **MKMaarif**  
📧 Contact: **[mk.maarif29@gmail.com]**  
🔗 GitHub: **[github.com/MKMaarif]**

---

## 📜 **License**
This project is licensed under the **MIT License**.
```
