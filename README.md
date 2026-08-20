# Evolutionary LangGraph Chatbot

An evolving AI chatbot project built with LangGraph, where the same chatbot architecture is progressively enhanced with streaming, resume understanding, tool calling, persistent conversations, and Retrieval-Augmented Generation (RAG).

Instead of building multiple unrelated chatbot demos, this project documents the evolution of a conversational AI system from a basic chatbot into a more capable, tool-using, persistent and document-aware AI assistant.

---

## 🚀 Project Evolution

```text
Basic Chatbot
      ↓
Streaming Responses
      ↓
Resume-aware Chatbot
      ↓
Tool Calling
      ↓
Persistent Conversations
      ↓
PDF-based RAG
```

Each stage is maintained in a separate folder so the architectural progression can be studied independently.

---

## 📂 Project Structure

```text
evolutionary-langgraph-chatbot/
│
├── 01_Basic_Chatbot/
├── 02_Streaming_Chatbot/
├── 03_Resume_Chatbot/
├── 04_Chatbot_with_Tools/
├── 05_Chatbot_with_Database/
│
├── 06_Chatbot_with_RAG/
│   ├── frontend.py
│   ├── backend.py
│   └── tool.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 🧠 Evolution Stages

## 01 — Basic Chatbot

The project starts with a basic conversational interface.

### Focus

* LLM integration
* User input
* AI responses
* Basic conversational flow

This establishes the foundation for later improvements.

---

## 02 — Streaming Chatbot

The chatbot is enhanced to stream the model's response instead of waiting for the complete response.

### Focus

* Token/response streaming
* Improved user experience
* Incremental AI output

---

## 03 — Resume Chatbot

The chatbot is extended to work with resume information.

### Focus

* Resume-aware conversations
* Context-based responses
* Structured interaction with candidate information

---

## 04 — Chatbot with Tools

The chatbot evolves from a purely conversational system into a tool-using agent.

The system can decide when a tool is required instead of relying only on the LLM's internal knowledge.

### Tools

* Web search
* Stock price lookup
* Calculator
* RAG tool in the final version

---

## 05 — Persistent Chatbot

Conversation persistence is introduced so conversations can survive beyond a single interaction.

### Focus

* Thread-based conversations
* Conversation history
* Persistent state
* SQLite checkpointing

---

## 06 — RAG-enabled Chatbot

The final stage adds document-grounded question answering.

Users can upload a PDF and ask questions about its content.

### RAG Pipeline

```text
PDF
 │
 ▼
PyPDFLoader
 │
 ▼
Document Extraction
 │
 ▼
RecursiveCharacterTextSplitter
 │
 ▼
Chunks
 │
 ▼
Cohere Embeddings
 │
 ▼
FAISS Vector Store
 │
 ▼
Retriever
 │
 ▼
RAG Tool
 │
 ▼
LangGraph
 │
 ▼
LLM Response
```

The final implementation maintains retrievers per conversation thread, allowing different chat threads to have their own uploaded document context.

---

# 🏗️ Final Architecture

```text
                         ┌──────────────────┐
                         │    Streamlit UI  │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │    LangGraph     │
                         │   Chat Node      │
                         └────────┬─────────┘
                                  │
                           Tool Decision
                                  │
                 ┌────────────────┴────────────────┐
                 │                                 │
                 ▼                                 ▼
        ┌──────────────────┐              ┌──────────────────┐
        │    Tool Node     │              │      Response    │
        └────────┬─────────┘              └──────────────────┘
                 │
       ┌─────────┼──────────┬────────────┐
       │         │          │            │
       ▼         ▼          ▼            ▼
    Search    Stock      Calculator     RAG
                                      │
                                      ▼
                                ┌────────────┐
                                │   FAISS    │
                                └─────┬──────┘
                                      │
                                Cohere Embeddings
                                      │
                                      ▼
                                     PDF
```

---

# 🔄 LangGraph Workflow

The final chatbot uses a graph-based workflow:

```text
START
  │
  ▼
Chat Node
  │
  ├────────────── No tool required ──────────────► END
  │
  ▼
Tool Node
  │
  └──────────────────────────────────────────────► Chat Node
```

This enables iterative tool execution instead of a simple linear chatbot pipeline.

---

# 🛠️ Tech Stack

### AI / LLM

* Python
* LangChain
* LangGraph
* Groq

### RAG

* Cohere Embeddings
* FAISS
* PyPDF
* Recursive Character Text Splitter

### Agent / Tools

* LangGraph ToolNode
* Web Search
* Stock Price API
* Calculator
* Custom RAG Tool

### Application

* Streamlit

### Persistence

* SQLite
* LangGraph SqliteSaver

---

# ✨ Key Features

* Conversational AI
* Streaming responses
* Resume-aware interaction
* Tool calling
* Web search
* Stock price retrieval
* Calculator tool
* Persistent conversations
* Thread-based conversation state
* PDF ingestion
* Document chunking
* Cohere embeddings
* FAISS vector search
* Retrieval-Augmented Generation
* Thread-specific document retrieval
* LangGraph-based orchestration

---

# 🔐 Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
COHERE_API_KEY=your_cohere_api_key
```

Never commit the `.env` file to GitHub.

---

# ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/evolutionary-langgraph-chatbot.git
cd evolutionary-langgraph-chatbot
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create your `.env` file and add your API keys.

---

# ▶️ Running the Application

Navigate to the final RAG version:

```bash
cd 06_Chatbot_with_RAG
```

Run Streamlit:

```bash
streamlit run frontend.py
```

Upload a PDF from the sidebar and ask questions about the document.

---

# 🧪 Example Queries

### General

```text
What can you help me with?
```

### Web Search

```text
What are the latest developments in generative AI?
```

### Calculator

```text
Calculate 125 * 48
```

### Stock Tool

```text
What is the latest price of AAPL?
```

### RAG

After uploading a PDF:

```text
What is the main topic of this document?

Summarize the key findings.

What does the document say about X?

Which section discusses Y?
```

---

# 🎯 Why This Project?

The goal of this project was not to build another isolated chatbot demo.

Instead, the project explores how a conversational AI system can evolve as new capabilities are introduced.

Each stage introduces a new engineering concept:

```text
LLM Integration
      ↓
Streaming
      ↓
Context Handling
      ↓
Tool Calling
      ↓
State Persistence
      ↓
Agentic Workflow
      ↓
RAG
```

This makes the repository both a project and a progression of AI engineering concepts.

---

# 📌 Learning Outcomes

Through this project, the following concepts were explored:

* LangGraph StateGraph
* Nodes and edges
* Conditional routing
* ToolNode
* Tool calling
* Conversation state
* Thread-based state
* SQLite checkpointing
* PDF document ingestion
* Text chunking
* Embeddings
* Vector databases
* Retrieval
* RAG pipelines
* Multi-tool AI workflows
* Streamlit integration

---

# 🚧 Future Improvements

Potential future improvements include:

* Hybrid search
* Reranking retrieved documents
* Metadata filtering
* Conversational RAG
* Citation-aware answers
* Streaming RAG responses
* Document-level access control
* Multi-document retrieval
* Background document ingestion
* Evaluation with RAG metrics
* LangSmith tracing and evaluation
* Production API using FastAPI
* Docker deployment

---

## 👩‍💻 Author

Vartika Gupta

Aspiring AI Engineer focused on Generative AI, LangChain, LangGraph, RAG and AI Agent systems.

GitHub: YOUR_GITHUB_URL

LinkedIn: YOUR_LINKEDIN_URL
