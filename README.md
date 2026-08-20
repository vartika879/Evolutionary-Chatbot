🧠 Evolutionary Chatbot
An evolving conversational AI system built with LangGraph, where the core chatbot architecture is progressively enhanced across modular stages—from a basic streaming bot into a tool-using, persistent, and document-aware AI agent.

🚀 Progression Overview
Rather than creating disjointed prototypes, each stage isolates and tackles a specific AI engineering problem:

Plaintext
Chatbot Foundation ──► Streaming Responses ──► Context Persistence ──► Tool Calling ──► PDF-based RAG
Stage	Focus Area	Core Technologies / Concepts
01 — Streaming Chatbot	Real-time output streaming	LangGraph, LangChain, Groq, Streamlit
02 — Resume-aware Chatbot	Persistent conversational memory	SqliteSaver, Thread-based state, SQLite
03 — Tool-Calling Agent	Dynamic execution & agentic routing	ToolNode, Web Search, Financial APIs, Math Tools
04 — RAG-enabled Assistant	Grounded PDF Question-Answering	Cohere Embeddings, FAISS, PyPDF, Custom RAG Tool
🏗️ Architecture & Workflow
The system relies on a stateful graph that dynamically decides between direct generation and cyclic tool execution:

Plaintext
       ┌──────────────┐
       │ Streamlit UI │
       └──────┬───────┘
              │
              ▼
       ┌──────────────┐
       │  Chat Node   │◄─────────────────────────┐
       └──────┬───────┘                          │
              │                                  │
       [Tool Required?]                          │
        ├── No ──────────────────► [ END / Final Output ]
        └── Yes                                  │
             │                                   │
             ▼                                   │
       ┌──────────────┐                          │
       │  Tool Node   │──────────────────────────┘
       └──────┬───────┘
              ├── Web Search
              ├── Stock Lookup
              ├── Calculator
              └── RAG Tool ──► FAISS Vector Store ──► Cohere Embeddings ──► Uploaded PDF
📂 Repository Structure
Plaintext
Evolutionary-Chatbot/
│
├── 01_Chatbot_with_Streaming/     # Basic conversational bot with token streaming
├── 02_ChatBot_resume_Chat/        # Context-aware chat with SQLite checkpoints
├── 03_Chatbot_with_tools/         # Dynamic tool-calling implementation
│   ├── backend.py
│   ├── fr.py
│   └── tool.py
├── 04_Chatbot_with_rag/           # End-to-end PDF RAG with LangGraph routing
│   ├── backend.py
│   ├── frontend.py
│   └── tool.py
├── requirements.txt
└── README.md
🛠️ Tech Stack
Frameworks & Orchestration: LangGraph, LangChain

LLM Provider: Groq

Vector Search & Embeddings: FAISS, Cohere

State Persistence: SQLite via SqliteSaver

Frontend: Streamlit

Document Processing: PyPDF, RecursiveCharacterTextSplitter

⚙️ Quick Start
1. Clone the repository

Bash
git clone https://github.com/vartika879/Evolutionary-Chatbot.git
cd Evolutionary-Chatbot
2. Set up virtual environment

Bash
# macOS/Linux
python -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\Activate.ps1
3. Install dependencies

Bash
pip install -r requirements.txt
4. Configure Environment Variables

Create a .env file in the root directory:

Code snippet
GROQ_API_KEY=your_groq_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
5. Launch the RAG Chatbot (Stage 04)

Bash
cd 04_Chatbot_with_rag
streamlit run frontend.py
💬 Example Queries
Web Search: "What are the latest updates in LangGraph?"

Stock Tool: "What is the current trading price of NVDA?"

Calculator: "Calculate (450 * 18) / 2.5"

PDF RAG (Post-upload): "Summarize the methodology section from the uploaded paper."

🚧 Roadmap
[ ] Hybrid dense/sparse search (BM25 + FAISS)

[ ] Cross-encoder reranking for context compression

[ ] LangSmith observability and trace evaluation

[ ] FastAPI backend decouple with Docker containerization

👩‍💻 Author
Vartika Gupta

AI Engineer focused on LangGraph, RAG Systems, and Autonomous Agents.

GitHub: @vartika879

LinkedIn: Vartika Gupta

