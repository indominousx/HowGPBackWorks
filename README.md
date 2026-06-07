# Enterprise Document Intelligence Chatbot

An AI-powered Enterprise Document Intelligence Platform that allows users to upload PDF documents, store them in a vector database, and interact with them using natural language.

The system uses Retrieval-Augmented Generation (RAG) to provide accurate, document-grounded responses while maintaining complete chat isolation across multiple conversations.

---

# Features

## Document Upload & Processing

* Upload one or multiple PDF documents
* Automatic PDF parsing using PyMuPDF
* Intelligent text chunking using RecursiveCharacterTextSplitter
* Metadata enrichment for document tracking
* Storage of document information per conversation

---

## AI-Powered Question Answering

* Natural language querying over uploaded documents
* Retrieval-Augmented Generation (RAG)
* Context-aware document search
* Semantic similarity search using vector embeddings
* Hallucination-resistant prompt engineering

---

## Multi-Chat Architecture

* Create multiple independent conversations
* ChatGPT-style sidebar conversation history
* Automatic chat title generation
* Persistent conversation storage
* Chat-specific document retrieval

---

## Persistent Storage

### PostgreSQL

Stores:

* Chats
* Messages
* Uploaded document metadata

### Qdrant

Stores:

* Vector embeddings
* Chunk metadata
* Semantic search index

---

## Document Isolation

Each uploaded document chunk is stored with metadata:

```json
{
  "chat_id": "abc123",
  "file_name": "Guide.pdf"
}
```

During retrieval, only chunks belonging to the current chat are searched.

This ensures:

* No cross-chat leakage
* Better retrieval quality
* Scalable multi-conversation support

---

# System Architecture

┌─────────────────────┐
│ Streamlit Frontend │
└──────────┬──────────┘
│
▼
┌─────────────────────┐
│ PostgreSQL Database │
│                     │
│ Chats               │
│ Messages            │
│ Documents           │
└──────────┬──────────┘
│
▼
┌─────────────────────┐
│ RAG Pipeline        │
└──────────┬──────────┘
│
▼
┌─────────────────────┐
│ Qdrant Vector DB    │
│                     │
│ Embeddings          │
│ Metadata            │
└──────────┬──────────┘
│
▼
┌─────────────────────┐
│ Qwen 2.5 LLM        │
└─────────────────────┘

---

# Technology Stack

## Frontend

* Streamlit

## LLM

* Qwen 2.5 Instruct
* HuggingFace Inference API

## Embeddings

* sentence-transformers/all-MiniLM-L6-v2

## Vector Database

* Qdrant

## Relational Database

* PostgreSQL

## Frameworks

* LangChain
* LangChain Qdrant
* LangChain HuggingFace

## PDF Processing

* PyMuPDF

---

# Project Structure

```text
EnterpriseDocumentChatBot/

│
├── app.py
│
├── documentloader.py
│
├── genembeddings.py
│
├── rag_chain.py
│
├── db.py
│
├── chat_repository.py
│
├── init_db.py
│
├── docker-compose.yml
│
├── .env
│
├── uploads/
│
└── README.md
```

---

# Database Design

## Chats Table

Stores conversation information.

| Column     | Type      |
| ---------- | --------- |
| chat_id    | TEXT      |
| title      | TEXT      |
| created_at | TIMESTAMP |

---

## Messages Table

Stores complete conversation history.

| Column     | Type      |
| ---------- | --------- |
| id         | SERIAL    |
| chat_id    | TEXT      |
| role       | TEXT      |
| content    | TEXT      |
| created_at | TIMESTAMP |

---

## Documents Table

Stores uploaded document information.

| Column      | Type      |
| ----------- | --------- |
| id          | SERIAL    |
| chat_id     | TEXT      |
| file_name   | TEXT      |
| uploaded_at | TIMESTAMP |

---

# RAG Workflow

## Step 1

User uploads PDF documents.

---

## Step 2

Documents are loaded using PyMuPDF.

---

## Step 3

Documents are chunked into smaller sections.

Example:

```text
Document
   ↓
Chunk 1
Chunk 2
Chunk 3
```

---

## Step 4

Each chunk is converted into vector embeddings.

```text
Text
   ↓
Embedding Model
   ↓
Vector
```

---

## Step 5

Vectors are stored in Qdrant with metadata.

```json
{
  "chat_id": "abc123",
  "file_name": "Guide.pdf"
}
```

---

## Step 6

User asks a question.

Example:

```text
What are the project phases?
```

---

## Step 7

Retriever searches only the current chat's vectors.

```python
Filter(
    metadata.chat_id == current_chat_id
)
```

---

## Step 8

Relevant chunks are sent to the LLM.

---

## Step 9

The LLM generates an answer grounded in retrieved context.

---

# Scalability Considerations

The system is designed to support:

* Thousands of conversations
* Millions of document chunks
* Multiple documents per conversation
* Enterprise-scale semantic search

Future enhancements may include:

* User authentication
* Multi-user support
* Role-based access control
* Hybrid Search (BM25 + Dense Retrieval)
* Re-ranking models
* Conversation memory
* Source citations
* Cloud deployment

---

# Setup Instructions

## Start Infrastructure

```bash
docker-compose up -d
```

---

## Initialize Database

```bash
python init_db.py
```

---

## Run Application

```bash
streamlit run app.py
```

---

## Open Application

```text
http://localhost:8501
```

---

# Key Learning Outcomes

This project demonstrates practical experience with:

* Retrieval-Augmented Generation (RAG)
* Vector Databases
* Semantic Search
* LangChain
* Prompt Engineering
* PostgreSQL
* Qdrant
* Streamlit
* Enterprise AI System Design
* Docker-based Development

---

