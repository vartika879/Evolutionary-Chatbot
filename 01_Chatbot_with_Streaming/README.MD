# 🤖 Chatbot with Streaming using LangGraph

A conversational AI chatbot built with **LangGraph, LangChain, Groq and Streamlit**, featuring **real-time token streaming** and **conversation state management**.

The project demonstrates how LangGraph can be used to build a structured chatbot workflow instead of directly calling an LLM from the application layer.

## 🚀 Features

* ⚡ Real-time streaming AI responses
* 🧠 Conversation state management using LangGraph
* 💾 In-memory checkpointing with `MemorySaver`
* 🔄 Thread-based conversation configuration
* 🤖 Groq LLM integration
* 🎨 Interactive Streamlit chat interface
* 🏗️ Graph-based chatbot architecture using `StateGraph`

## 🏗️ Architecture

```text
User
  │
  ▼
Streamlit Chat Interface
  │
  ▼
HumanMessage
  │
  ▼
LangGraph StateGraph
  │
  ▼
Chat Node
  │
  ▼
Groq Llama 3.3 70B
  │
  ▼
Streaming Response
  │
  ▼
Streamlit UI
```

## 📁 Project Structure

```text
Chatbot_with_Streaming/
│
├── backend.py
├── chatbot.py
└── README.md
```

### `backend.py`

Contains the LangGraph chatbot backend.

It defines:

* `ChatState`
* Groq LLM
* Chat node
* LangGraph `StateGraph`
* `MemorySaver` checkpoint
* Graph compilation

The chatbot graph follows:

```text
START → Chat_node → END
```

The graph is compiled with a checkpointer to maintain state.

### `chatbot.py`

Contains the Streamlit frontend.

It:

* Accepts user messages
* Displays previous conversation
* Streams the assistant response
* Updates the UI while tokens are being generated
* Stores the final assistant response in session history

The application uses `chatbot.stream()` with `stream_mode="messages"` for streaming responses.

## 🛠️ Tech Stack

| Technology    | Purpose                         |
| ------------- | ------------------------------- |
| Python        | Core programming language       |
| LangGraph     | Workflow and state management   |
| LangChain     | LLM integration                 |
| Groq          | LLM inference                   |
| Llama 3.3 70B | Language model                  |
| Streamlit     | Web interface                   |
| Pydantic      | Data validation                 |
| python-dotenv | Environment variable management |

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd Chatbot_with_Streaming
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Groq API key

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

The backend loads the API key from the environment and initializes the Groq chat model.

## ▶️ Run the Application

Start the Streamlit application:

```bash
streamlit run chatbot.py
```

Then open the local Streamlit URL shown in your terminal.

## 🧩 LangGraph Workflow

The chatbot uses a simple LangGraph workflow:

```text
START
  │
  ▼
Chat_node
  │
  ▼
Groq LLM
  │
  ▼
END
```

The graph receives the current message state, sends the messages to the LLM and returns the generated response.

## 🔥 Streaming

Instead of waiting for the complete response, the application processes streamed message chunks:

```python
for message_chunk, metadata in chatbot.stream(
    {'messages': [HumanMessage(content=user_input)]},
    config={'configurable': {'thread_id': 'thread_1'}},
    stream_mode='messages'
):
    ...
```

This allows the UI to display the response progressively as it is generated.

## 🧠 What I Learned

Through this project, I explored:

* LangGraph `StateGraph`
* Nodes and edges
* Graph execution
* Typed state
* Message-based state
* Checkpointing with `MemorySaver`
* Thread configuration
* LLM streaming
* LangGraph + Streamlit integration

## 🔮 Future Improvements

Possible next improvements include:

* Persistent database-backed conversation memory
* Multiple conversation threads
* Conversation reset functionality
* Token usage tracking
* LangSmith tracing and observability
* Tool calling
* Retrieval-Augmented Generation (RAG)
* Authentication and user-specific sessions
* Production deployment using FastAPI + Streamlit

## 👩‍💻 Author

**Vartika Gupta**

Building AI applications with **LangChain, LangGraph and Agentic AI**.
