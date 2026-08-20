# 📄 Chatbot with RAG

This is the **RAG-enabled stage** of the Evolutionary LangGraph Chatbot project.

In this version, the chatbot is extended with **PDF document ingestion and Retrieval-Augmented Generation (RAG)** while retaining the existing conversational and tool-based workflow.

---

# 🚀 What This Version Adds

The chatbot can now:

* Accept PDF documents
* Extract text from uploaded PDFs
* Split documents into smaller chunks
* Generate embeddings using Cohere
* Store embeddings in FAISS
* Retrieve relevant document chunks
* Answer questions using information from the uploaded PDF
* Maintain document retrieval separately for each chat thread
* Continue using other tools such as web search, calculator and stock price retrieval

---

# 🏗️ Architecture

```text
                         USER
                           │
                           ▼
                    ┌─────────────┐
                    │  Streamlit  │
                    │  Frontend   │
                    └──────┬──────┘
                           │
                           │ PDF Upload
                           ▼
                    ┌─────────────┐
                    │ PyPDFLoader │
                    └──────┬──────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │  Text Splitter     │
                 │ chunk_size = 1000  │
                 │ overlap = 200      │
                 └─────────┬──────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │ Cohere Embeddings  │
                 └─────────┬──────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │    FAISS    │
                    └──────┬──────┘
                           │
                           ▼
                     Retriever
                           │
                           ▼
                       RAG Tool
                           │
                           ▼
                    ┌─────────────┐
                    │  LangGraph  │
                    │  Chat Node  │
                    └──────┬──────┘
                           │
                           ▼
                      LLM Response
```

---

# 🔄 LangGraph Workflow

The chatbot uses a graph-based workflow:

```text
START
  │
  ▼
Chat Node
  │
  ├──────────────► Direct Answer
  │
  │
  ▼
Tool Decision
  │
  ▼
Tool Node
  │
  ├── Web Search
  ├── Calculator
  ├── Stock Price
  └── RAG Tool
          │
          ▼
      FAISS Retriever
          │
          ▼
     PDF Context
          │
          ▼
      Chat Node
```

The graph can return to the chat node after tool execution, allowing the LLM to use tool results before producing the final answer.

---

# 📁 Files

## `frontend.py`

Provides the Streamlit interface.

Responsibilities:

* Chat UI
* PDF upload
* Thread management
* Conversation display
* Streaming assistant responses
* Document metadata display

---

## `backend.py`

Contains the LangGraph workflow and conversation persistence.

Responsibilities:

* Define chatbot state
* Create the LangGraph workflow
* Configure the LLM
* Create the ToolNode
* Configure conditional routing
* Configure SQLite checkpointing

---

## `tool.py`

Contains the tools and RAG pipeline.

Responsibilities:

* Web search
* Calculator
* Stock price retrieval
* PDF ingestion
* Text splitting
* Cohere embeddings
* FAISS vector store
* Retriever creation
* RAG tool

---

# 📄 RAG Pipeline

When a PDF is uploaded:

```text
PDF
 │
 ▼
PyPDFLoader
 │
 ▼
Documents
 │
 ▼
RecursiveCharacterTextSplitter
 │
 ▼
Document Chunks
 │
 ▼
Cohere Embeddings
 │
 ▼
FAISS
 │
 ▼
Retriever
 │
 ▼
Stored for Current Thread
```

The implementation uses:

```text
chunk_size = 1000
chunk_overlap = 200
```

and retrieves the top 4 relevant chunks during similarity search.

---

# 🧠 Thread-Specific Retrieval

Each conversation thread can have its own uploaded document.

Conceptually:

```text
Thread A
 └── PDF A
      └── FAISS Retriever A

Thread B
 └── PDF B
      └── FAISS Retriever B

Thread C
 └── PDF C
      └── FAISS Retriever C
```

This prevents document context from one conversation thread from being mixed with another.

---

# 🔧 Available Tools

The current version includes:

### Web Search

Used when the chatbot needs external web information.

### Calculator

Performs arithmetic operations.

Supported operations:

* Addition
* Subtraction
* Multiplication
* Division

### Stock Price

Retrieves stock price information using an external API.

### RAG Tool

Retrieves relevant information from the PDF uploaded for the current chat thread.

---

# 💾 Conversation Persistence

LangGraph's SQLite checkpointer is used to maintain conversation state.

```text
User Message
     │
     ▼
LangGraph
     │
     ▼
SQLite Checkpoint
     │
     ▼
Conversation State
```

Each conversation is associated with a thread ID.

---

# 🛠️ Tech Stack

| Component    | Technology |
| ------------ | ---------- |
| UI           | Streamlit  |
| LLM          | Groq       |
| Workflow     | LangGraph  |
| Framework    | LangChain  |
| Embeddings   | Cohere     |
| Vector Store | FAISS      |
| PDF Loader   | PyPDF      |
| Persistence  | SQLite     |
| Language     | Python     |

---

# ⚙️ Setup

From the project root:

```bash
pip install -r requirements.txt
```

Create `.env`:

```env
GROQ_API_KEY=your_groq_api_key
COHERE_API_KEY=your_cohere_api_key
```

Run:

```bash
streamlit run frontend.py
```

---

# 🧪 Example

Upload a PDF and ask:

```text
What is the main topic of this document?
```

or:

```text
Summarize the key findings.
```

or:

```text
What does the document say about X?
```

The chatbot retrieves relevant chunks from the indexed document and uses them as context for the response.

---

# 🔐 Security

API keys should be stored in `.env`.

Do not commit:

```text
.env
```

to GitHub.

Use `.env.example` to document required environment variables.

---

# 🔮 Future Improvements

Possible improvements for this version:

* Hybrid search
* Reranking
* Multi-document RAG
* Metadata filtering
* Source citations
* Retrieval evaluation
* RAGAS evaluation
* LangSmith tracing
* Better document management
* Production API using FastAPI
* Docker deployment

---

## Part of the Evolutionary Chatbot Project

This folder represents the **RAG stage** of the larger project.

See the root repository README for the complete evolution from the basic chatbot to the RAG-enabled system.
