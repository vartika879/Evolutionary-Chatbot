🧠 Evolutionary Chatbot

An evolving conversational AI system built with LangGraph, where the same chatbot architecture is progressively enhanced with new AI engineering capabilities.

Instead of creating multiple unrelated chatbot demos, this project follows the evolution of a conversational AI system from a basic chatbot into a more capable streaming, resume-aware, tool-using, persistent, and document-aware AI assistant.

The project is structured as a progression, with each major stage maintained separately so that the implementation and architectural changes can be studied independently.

🚀 Project Evolution
Chatbot Foundation
        ↓
Streaming Responses
        ↓
Resume-aware Conversations
        ↓
Tool Calling
        ↓
Persistent Conversations
        ↓
PDF-based RAG

Each stage introduces a new engineering concept while building upon the previous chatbot architecture.

📂 Repository Structure
Evolutionary-Chatbot/
│
├── 01_Chatbot_with_Streaming/
│   └── Streaming chatbot implementation
│
├── 02_ChatBot_resume_Chat/
│   └── Resume-aware chatbot with persistent conversation state
│
├── 03_Chatbot_with_tools/
│   ├── backend.py
│   ├── fr.py
│   ├── tool.py
│   └── README.MD
│
├── 04_Chatbot_with_rag/
│   ├── backend.py
│   ├── frontend.py
│   ├── tool.py
│   └── README.MD
│
├── chat_cp/
│   └── Additional chatbot experimentation
│
├── app.py
├── main.py
├── requirements.txt
├── pyproject.toml
├── uv.lock
├── .python-version
├── .gitignore
└── README.md
🧩 Evolution Stages
01 — Streaming Chatbot

The project begins with a conversational chatbot enhanced with streaming responses.

Instead of waiting for the complete model response, the application displays the generated response incrementally.

Key Concepts
LangGraph chatbot workflow
LLM integration
Streaming responses
Incremental AI output
Improved conversational experience

This stage establishes the foundation for the later versions.

02 — Resume Chatbot

The chatbot is extended to work with resume information, allowing users to interact with candidate-related information through conversational queries.

Key Concepts
Resume-aware conversations
Context handling
Conversation history
Thread-based conversations
Persistent state
SQLite checkpointing

This stage introduces persistent conversational state, allowing conversations to maintain context beyond a single interaction.

03 — Chatbot with Tools

The chatbot evolves from a purely conversational system into a tool-using AI agent.

Instead of depending only on the LLM's internal knowledge, the system can determine when an external tool is required and execute it.

Available Tools
Web search
Stock price lookup
Calculator
Key Concepts
LangGraph ToolNode
Tool calling
Conditional routing
Tool execution
Agentic workflows
Iterative tool usage

The workflow can be represented as:

User Query
    ↓
Chat Node
    ↓
Tool Decision
    │
    ├── No Tool Required ──→ Final Response
    │
    └── Tool Required
            ↓
        Tool Node
            ↓
        Chat Node

This allows the chatbot to perform actions beyond simple text generation.

04 — RAG-enabled Chatbot

The final major stage introduces Retrieval-Augmented Generation (RAG).

Users can upload a PDF and ask questions about its contents.

Instead of relying entirely on the LLM's internal knowledge, relevant information is retrieved from the uploaded document and provided to the model as context.

RAG Pipeline
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
Document Chunks
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
Key Concepts
PDF ingestion
Document extraction
Text chunking
Embeddings
FAISS vector search
Retrieval
RAG tool
Thread-specific document context
LangGraph orchestration

The final implementation maintains retrievers per conversation thread, allowing different conversations to maintain their own uploaded-document context.

🏗️ Final Architecture

The final version combines conversational reasoning, tool calling, retrieval, and state management into a LangGraph-based workflow.

                         ┌─────────────────────┐
                         │     Streamlit UI    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      LangGraph      │
                         │      Chat Node      │
                         └──────────┬──────────┘
                                    │
                              Tool Decision
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
          ┌──────────────────┐             ┌──────────────────┐
          │    Tool Node     │             │     Response     │
          └────────┬─────────┘             └──────────────────┘
                   │
          ┌────────┼───────────┬────────────┐
          │        │           │            │
          ▼        ▼           ▼            ▼
       Search    Stock      Calculator     RAG
                                           │
                                           ▼
                                    ┌─────────────┐
                                    │    FAISS    │
                                    └──────┬──────┘
                                           │
                                  Cohere Embeddings
                                           │
                                           ▼
                                          PDF
🔄 LangGraph Workflow

The final chatbot uses a graph-based workflow rather than a simple linear request-response pipeline.

START
  │
  ▼
Chat Node
  │
  ├──────── No tool required ────────→ END
  │
  ▼
Tool Node
  │
  └──────────────────────────────────→ Chat Node

This enables iterative tool execution:

Receive the user query
Determine whether a tool is required
Execute the selected tool
Return the tool result to the model
Continue the workflow if another tool is required
Generate the final response
🛠️ Tech Stack
AI / LLM
Python
LangChain
LangGraph
Groq
RAG
PyPDF
Recursive Character Text Splitter
Cohere Embeddings
FAISS
Agent / Tools
LangGraph ToolNode
Web Search
Stock Price Lookup
Calculator
Custom RAG Tool
Application
Streamlit
Persistence
SQLite
LangGraph SqliteSaver
✨ Key Features
Conversational AI
LangGraph-based orchestration
Streaming responses
Resume-aware conversations
Tool calling
Web search
Stock price retrieval
Calculator tool
Persistent conversation state
Thread-based conversations
SQLite checkpointing
PDF ingestion
Document chunking
Cohere embeddings
FAISS vector search
Retrieval-Augmented Generation
Thread-specific document retrieval
Iterative tool execution
🔐 Environment Variables

Create a .env file in the project root:

GROQ_API_KEY=your_groq_api_key
COHERE_API_KEY=your_cohere_api_key

Never commit your .env file to GitHub.

⚙️ Installation
1. Clone the repository
git clone https://github.com/vartika879/Evolutionary-Chatbot.git
cd Evolutionary-Chatbot
2. Create a virtual environment
python -m venv .venv
3. Activate the environment

Windows PowerShell

.venv\Scripts\Activate.ps1

macOS / Linux

source .venv/bin/activate
4. Install dependencies
pip install -r requirements.txt
5. Configure API keys

Create a .env file:

GROQ_API_KEY=your_groq_api_key
COHERE_API_KEY=your_cohere_api_key
▶️ Running the Latest RAG Version

The latest major version is located in:

04_Chatbot_with_rag/

Navigate to the directory:

cd 04_Chatbot_with_rag

Run the Streamlit application:

streamlit run frontend.py

Upload a PDF from the application and start asking questions about the document.

💬 Example Queries
General Conversation
What can you help me with?
Web Search
What are the latest developments in Generative AI?
Calculator
Calculate 125 * 48
Stock Tool
What is the latest price of AAPL?
RAG

After uploading a PDF:

What is the main topic of this document?


Summarize the key findings.


What does the document say about X?


Which section discusses Y?
🎯 Why This Project?

The goal of this project was not to build another isolated chatbot demo.

Instead, it explores how a conversational AI application can evolve as new capabilities are introduced.

Each stage focuses on a different engineering problem:

LLM Integration
      ↓
Streaming
      ↓
Context Handling
      ↓
State Persistence
      ↓
Tool Calling
      ↓
Agentic Workflow
      ↓
RAG

This makes the repository both a practical project and a progression through important LLM application engineering concepts.

🧠 Learning Outcomes

Through this project, I explored and implemented:

LangGraph
StateGraph
Nodes and edges
Conditional routing
ToolNode
Graph-based orchestration
Iterative workflows
Conversational State
Conversation history
Thread-based state
Persistent state
SQLite checkpointing
Tool Calling
Tool definition
Tool selection
Tool execution
Tool result handling
Multi-step tool workflows
RAG
PDF ingestion
Document extraction
Text splitting
Embeddings
Vector stores
Similarity retrieval
Retrieval-Augmented Generation
Document-grounded responses
Application Development
Streamlit integration
Modular Python structure
Environment configuration
LLM application workflows
🚧 Future Improvements

The project can be further evolved toward a production-grade AI system with:

Hybrid search
Retrieval reranking
Metadata filtering
Conversational RAG
Citation-aware responses
Multi-document retrieval
Document-level access control
Background document ingestion
RAG evaluation
Retrieval quality evaluation
LangSmith tracing and evaluation
FastAPI backend
Docker deployment
Production monitoring
Improved observability
👩‍💻 Author
Vartika Gupta

Aspiring AI Engineer focused on:

Generative AI • LangChain • LangGraph • RAG • AI Agents • LLM Applications

GitHub: github.com/vartika879
LinkedIn: linkedin.com/in/vartika-gupta-560b3b36b
⭐ Project Philosophy

Build one system. Keep evolving it.

This repository documents that evolution — from a simple conversational workflow to a more capable tool-using, stateful, and document-aware AI system powered by LangGraph.

If you find this project useful, consider giving it a ⭐ on GitHub.
