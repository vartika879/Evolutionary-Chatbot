# 🚀 Evolutionary Chatbot

An AI chatbot that is being **continuously evolved feature by feature** using LangGraph, LangChain, Groq, Streamlit and other modern AI technologies.

Instead of building multiple disconnected chatbot projects, this repository follows one system as it grows from a simple LLM workflow into a more capable **Agentic AI application**.

---

## 🎯 Project Vision

The goal of this project is to progressively transform a basic chatbot into a feature-rich, production-oriented AI system.

```text
Simple Chatbot
      ↓
Real-time Streaming
      ↓
Persistent Conversation State
      ↓
Multiple Chat Threads
      ↓
Tool Calling
      ↓
RAG
      ↓
Web Search
      ↓
MCP
      ↓
Multi-Agent Workflows
      ↓
Production-Grade AI Application
```

Each milestone introduces a new capability while building on the previous architecture.

---

# 🏗️ Current Version — Milestone 2

The current version focuses on **conversation state and persistent chat management**.

### ✨ Features

* ⚡ Real-time response streaming
* 🧠 LangGraph state management
* 💾 SQLite-backed checkpointing
* 💬 Multiple conversation threads
* 🆕 New Chat functionality
* 🔄 Previous conversation recovery
* 🆔 Unique thread IDs
* 🎨 Streamlit-based chat interface
* 🤖 Groq LLM integration

The backend uses `SqliteSaver` with SQLite to persist LangGraph checkpoints.

The frontend generates unique thread IDs and maintains a list of available conversation threads.

---

# 🧠 How It Works

```text
                 ┌─────────────────┐
                 │      User       │
                 └────────┬────────┘
                          ↓
                 ┌─────────────────┐
                 │  Streamlit UI   │
                 └────────┬────────┘
                          ↓
                 ┌─────────────────┐
                 │   Thread ID     │
                 └────────┬────────┘
                          ↓
                 ┌─────────────────┐
                 │    LangGraph    │
                 │   StateGraph    │
                 └────────┬────────┘
                          ↓
                 ┌─────────────────┐
                 │    Chat Node    │
                 └────────┬────────┘
                          ↓
                 ┌─────────────────┐
                 │    Groq LLM     │
                 │ Llama 3.3 70B   │
                 └────────┬────────┘
                          ↓
                 ┌─────────────────┐
                 │ SQLite Checkpoint│
                 └─────────────────┘
```

The LangGraph workflow currently follows:

```text
START → Chat Node → END
```

The chatbot is compiled with a SQLite checkpointer for conversation state persistence.

---

# 💬 Conversation Management

Each conversation receives a unique thread ID using Python's `uuid`.

```python
thread_id = uuid.uuid4()
```

A new chat creates a new thread and clears the current conversation history.

Previous conversations can then be selected from the sidebar and loaded from the LangGraph state:

```text
Sidebar
   │
   ├── Chat Thread 1
   ├── Chat Thread 2
   ├── Chat Thread 3
   └── Chat Thread 4
          │
          ↓
    Load Conversation
          │
          ↓
    LangGraph State
```

The application retrieves stored thread IDs from the SQLite-backed checkpointer.

---

# ⚡ Real-time Streaming

The chatbot uses LangGraph's streaming functionality to process model responses progressively.

```python
for message_chunk, metadata in chatbot.stream(
    {"messages": [HumanMessage(content=user_input)]},
    config=CONFIG,
    stream_mode="messages"
):
    ...
```

The Streamlit interface updates the displayed response as message chunks arrive.

---

# 🛠️ Tech Stack

| Technology    | Purpose                            |
| ------------- | ---------------------------------- |
| Python        | Core development                   |
| LangGraph     | Stateful workflow orchestration    |
| LangChain     | LLM integration                    |
| Groq          | Fast LLM inference                 |
| Llama 3.3 70B | Language model                     |
| Streamlit     | Chat interface                     |
| SQLite        | Conversation checkpoint storage    |
| Pydantic      | Data modelling                     |
| UUID          | Conversation thread identification |

---

# 📁 Current Project Structure

```text
Evolutionary-Chatbot/
│
├── chatbot/
│   ├── backened.py
│   └── frontened.py
│
├── chatbot.db
├── README.md
├── requirements.txt
└── .gitignore
```

> `chatbot.db` is a local SQLite database and should not be committed to GitHub if it contains local conversation data.

---

# 📈 Evolution Roadmap

### ✅ Milestone 1 — Streaming Chatbot

* LangGraph StateGraph
* Groq LLM
* Streamlit UI
* Real-time streaming

### ✅ Milestone 2 — Conversation State

* SQLite checkpointing
* Persistent conversation state
* Multiple threads
* New Chat
* Conversation recovery

### 🔜 Milestone 3 — Tool Calling

Planned capabilities:

* External tools
* Tool routing
* Tool execution
* Error handling

### 🔜 Milestone 4 — RAG

Planned capabilities:

* Document ingestion
* Chunking
* Embeddings
* Vector retrieval
* Context-aware responses

### 🔜 Milestone 5 — Web Search

The chatbot will be able to retrieve current information from external sources when required.

### 🔜 Milestone 6 — MCP

Exploring Model Context Protocol for connecting the chatbot with external tools and systems.

### 🔜 Milestone 7 — Multi-Agent Workflows

Introducing specialized agents and coordinated LangGraph workflows.

### 🔜 Milestone 8 — Production Architecture

The final goal is to move toward:

* Persistent database architecture
* Authentication
* Observability
* Error handling
* Security
* Evaluation
* API layer
* Scalable deployment

---

# 💡 What I'm Learning

This project is helping me understand that building AI applications is not just about connecting an LLM to a UI.

The real engineering challenge is designing:

**State → Workflow → Memory → Tools → Retrieval → Agents → Production Architecture**

The chatbot is therefore being treated as an evolving system rather than a one-time project.

---

# 🚀 Current Status

**Milestone 2 — Completed ✅**

The chatbot can now:

```text
Create Chat
     ↓
Assign Thread ID
     ↓
Chat with LLM
     ↓
Stream Response
     ↓
Save Conversation State
     ↓
Create Another Chat
     ↓
Return to Previous Thread
     ↓
Recover Conversation
```

---

## 🔗 Repository

GitHub:
https://github.com/vartika879/Evolutionary-Chatbot

---

## 👩‍💻 Author

**Vartika Gupta**

Building and exploring **LangChain, LangGraph, Agentic AI and production-oriented AI systems**.

---

⭐ This repository will continue evolving as new capabilities are added.
