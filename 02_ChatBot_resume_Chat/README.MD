🚀 **My chatbot just got a memory upgrade.**

I’m building one AI chatbot and evolving it feature by feature — instead of creating disconnected projects every time I learn something new.

Today, I completed **Milestone 2** of my **Evolutionary Chatbot**:

🧠 **Persistent Conversation State**
I moved from in-memory checkpointing to **SQLite-backed persistence using LangGraph’s `SqliteSaver`**.

💬 **Multiple Conversation Threads**
Each conversation gets its own unique `thread_id`, allowing me to create and switch between different chats.

🔄 **Conversation Recovery**
Previous conversations can be retrieved and loaded again instead of starting from scratch every time.

⚡ **Real-time Streaming**
The chatbot continues to stream responses as they are generated.

🎨 **Streamlit Chat Interface**
Added a sidebar for creating new chats and switching between saved conversations.

### The workflow now looks like:

**User → Streamlit → Thread ID → LangGraph → Groq LLM → SQLite Checkpointer**

What I found interesting while building this:

**The difficult part isn't simply making an LLM respond.
It's designing how state, conversations, and workflows should behave around the LLM.**

And this is still just **Version 2.**

Next, I want to evolve this same system with:

→ Tool Calling
→ RAG
→ Web Search
→ MCP
→ Multi-Agent Workflows
→ Production-grade architecture

The goal isn't to build a chatbot once.

**The goal is to keep engineering the same system until it becomes a complete Agentic AI application. 🚀**

🔗 **GitHub:**
https://github.com/vartika879/Evolutionary-Chatbot

#LangGraph #LangChain #AgenticAI #GenerativeAI #AIEngineering #Python #Groq #Streamlit #SQLite #LLM #AIProjects #LearningInPublic
