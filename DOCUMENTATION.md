# **AI Engineer Test Submission**

## **Table of Contents**
1. [Introduction](#introduction)
2. [Synthetic Data Generation](#synthetic-data-generation)
    - [Synthetic PDF Data](#synthetic-pdf-data)
    - [Synthetic SQL Database](#synthetic-sql-database)
3. [RAG System Implementation](#rag-system-implementation)
    - [Retrieval Strategy](#retrieval-strategy)
    - [System Architecture](#system-architecture)
    - [Challenges & Trade-offs](#challenges--trade-offs)
4. [Benchmarking & Testing](#benchmarking--testing)
    - [Evaluation Metrics](#evaluation-metrics)
    - [Comparison of Baseline vs. RAG](#comparison-of-baseline-vs-rag)
5. [Fine-Tuning Data Formatting](#fine-tuning-data-formatting)
6. [Deployment & Deliverables](#deployment--deliverables)
7. [Submission Details](#submission-details)

---

## **Introduction**
This submission is part of the AI Engineer Test to demonstrate expertise in:
- Generating **synthetic data** (PDF and CSV format).
- Implementing a **RAG-based chatbot** using open models (Llama 8B) and the **Groq API**.
- Evaluating chatbot performance through **benchmarking and structured testing**.
- Formatting data for **fine-tuning instruction-based LLMs**.

A hosted **RAG chatbot interface** and a **GitHub repository** for the retrieval pipeline are included.

---

## **Synthetic Data Generation**
### **Synthetic PDF Data**
- **Generated a 50+ page structured document** mimicking a **technical manual** for a fictional product (**AI Assistant X-3000**).
- Document includes:
  - **Product Features**
  - **Installation Guide**
  - **Troubleshooting Procedures**
  - **Security & Privacy**
  - **Smart Home Integrations**
  - **FAQs and User Interactions**
- **Why?** This structured, realistic document helps in training LLMs and simulating enterprise documentation retrieval.

- Way to generate synthetic data:
  - **Use of GPT-3** to generate text based on prompts, tables, mermaid code for flowchart, and python code for graphs.
  - **Use of Dall-E** to generate images based on prompts.
  - **Manual curation** to ensure coherence and relevance.
  - **Structured formatting** for easy retrieval.

### **Synthetic SQL Database**
- **Database contains 1,000+ rows**, representing **user interaction logs**.
- **Fields:** `interaction_id`, `user_id`, `device_type`, `command_category`, `command_text`, `ai_response`, `response_time_ms`, `user_satisfaction`, `status`, `error_code`.
- **Purpose:**
  - Enables **structured retrieval for RAG** when answering **quantitative questions** (e.g., error rates, usage frequency).
  - Simulates a **real-world analytics database**.

- Way to generate synthetic data:
    - **Use of Faker** to generate random data for each field.

---

## **RAG System Implementation**
### **Retrieval Strategy**
- **Embedding Model:** OpenAIEmbeddings `text-embedding-3-large` (better performance).
- **Vector Store:** FAISS for **fast similarity search**.
- **Chunking Strategy:**
  - **Text split into 1000-character chunks with 200-character overlap** for optimal retrieval.
  - **SQL queries triggered for numerical/statistical questions**.

### **System Architecture**
1. **User Query → FAISS Search → Retrieve Top 5 Relevant Chunks**
2. **If structured data needed, execute SQL query**
3. **Final Context Passed to LLM** (Llama 8B via Groq API)
4. **Generate Response → Return to User**

### **Challenges & Trade-offs**
- **Why FAISS?**
  - **Fast** local vector search
  - No **external dependencies**
- **Optimal Chunking Trade-off:**
  - **Too small = Loss of context**
  - **Too large = Retrieval inefficiency**

---

## **Benchmarking & Testing**
### **Evaluation Metrics**
To compare **Baseline LLM vs. RAG**:
- **Answer Accuracy** (Correctness of response)
- **Context Relevance** (Does retrieval improve response?)
- **Completeness** (Is the response comprehensive?)
- **Conciseness & Fluency** (Well-structured response)

### **Comparison of Baseline vs. RAG**
| **Metric** | **Baseline (No RAG)** | **RAG System** |
|------------|----------------|------------|
| **Accuracy** | 3.6/5.0 | **4.8/5.0** |
| **Relevance** | 2.6/5.0 | **4.8/5.0** |
| **Completeness** | 3.4/5.0 | **4.6/5.0** |
| **Conciseness** | 4.4/5.0 | **5.0/5.0** |
| **Final Score** | **3.5/5.0** | **4.75/5.0** |

- **Key Findings:**
  - **RAG improves accuracy and factual retrieval**.
  - **SQL integration enhances data-driven responses**.

---

## **Fine-Tuning Data Formatting**
### **Why JSONL Format?**
- **Instruction-based fine-tuning** for models like **LLaMA, Gemma, Mistral, and Phi**.
- Allows structured **question-answer** learning.

### **JSONL Example:**
```json
[
    {
        "instruction": "Deskripsikan produk AI Assistant X-3000.", 
        "response": "Berikut adalah jawaban untuk pertanyaan \"Deskripsikan produk AI Assistant X-3000\":\n\nAI Assistant X-3000 adalah robot asisten pintar generasi terbaru yang dirancang untuk membantu pengguna dalam berbagai tugas sehari-hari di rumah, kantor, dan lingkungan industri. Dengan kemampuan kecerdasan buatan (AI) tingkat lanjut, robot ini dapat memahami perintah suara, mengenali wajah, serta beradaptasi dengan kebiasaan pengguna untuk memberikan layanan yang lebih personal dan efisien. Dilengkapi dengan sensor canggih, pemrosesan bahasa alami (NLP), dan konektivitas Internet of Things (IoT), AI Assistant X-3000 mampu berinteraksi dengan berbagai perangkat pintar dalam ekosistem rumah dan kantor. Teknologi utama yang digunakan dalam AI Assistant X-3000 mencakup prosesor AI berkecepatan tinggi, kamera multi-spektrum dengan kemampuan pengenalan wajah dan objek, serta sensor LiDAR dan ultrasonik untuk navigasi mandiri yang presisi."
    }, 
    {
        "instruction": "Apa saja fitur yang dimiliki oleh AI Assistant X-3000?", 
        "response": "Berikut adalah jawaban untuk pertanyaan tentang fitur yang dimiliki oleh AI Assistant X-3000:\n\nAI Assistant X-3000 hadir dengan berbagai fitur canggih yang dirancang untuk meningkatkan efisiensi dan kenyamanan pengguna. Beberapa fitur utama yang dimiliki oleh AI Assistant X-3000 adalah:\n\n1. Interaksi Suara dan Visual: AI Assistant X-3000 dapat memproses perintah suara dan memberikan respons secara visual maupun auditori.\n2. Navigasi Otomatis dan Penghindaran Hambatan: AI Assistant X-3000 dapat bergerak secara mandiri serta menghindari rintangan dengan akurasi tinggi.\n3. Kontrol Smart Home: AI Assistant X-3000 dapat mengatur lampu, suhu ruangan, dan keamanan rumah sesuai dengan jadwal.\n4. Pengingat Otomatis: AI Assistant X-3000 dapat memberikan pengingat otomatis untuk pengguna.\n5. Manajemen Jadwal: AI Assistant X-3000 dapat membantu pengguna dalam manajemen jadwal.\n6. Integrasi dengan Kalender Digital: AI Assistant X-3000 dapat diintegrasikan dengan kalender digital.\n7. Navigasi Bebas: AI Assistant X-3000 dapat beroperasi secara otonom untuk navigasi bebas.\n8. Pemantauan Inventaris: AI Assistant X-3000 dapat membantu pengguna dalam pemantauan inventaris.\n9. Laporan Analitik Otomatis: AI Assistant X-3000 dapat memberikan laporan analitik otomatis.\n\nDengan demikian, AI Assistant X-3000 dapat membantu pengguna dalam berbagai tugas sehari-hari dan meningkatkan efisiensi dan kenyamanan pengguna."
    }, 
]
```

- Extracted **10 Q&A pairs** from the synthetic PDF.

---

## **Deployment & Deliverables**
- **📍 Hosted Chatbot:** *https://rag-llm-app-desk-aagspmk7srfw7joxukqvlt.streamlit.app/*
- **📂 GitHub Repository:** *https://github.com/MKMaarif/RAG-LLM_Helpdesk_synthetic-data.git*
- **📄 Synthetic Data Files:**
  - `M. Khoirul Ma'arif_synthetic_data.pdf`
  - `M. Khoirul Ma'arif_synthetic_data.sql`
  - `M. Khoirul Ma'arif.json` (fine-tuning format)
  - This documentation (`DOCUMENTATION.md`)

---