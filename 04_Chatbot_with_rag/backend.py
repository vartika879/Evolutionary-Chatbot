from __future__ import annotations
from langgraph.graph import StateGraph,START, END
from typing import TypedDict,Annotated,Dict,Any
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage,BaseMessage
from pydantic import BaseModel, Field
import operator
from langgraph.prebuilt import ToolNode,tools_condition
import os
import tempfile
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from tool import llm_with_tools,tools




load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# 1. LLM + embeddings

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    groq_api_key=api_key   # ✅ correct parameter name
)


_THREAD_RETRIEVERS: Dict[str, Any] = {}
_THREAD_METADATA: Dict[str, dict] = {}





class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]



def chat_node(state:ChatState,config=None):
    """LLM node that may answer or request a tool call"""
    thread_id=None
    if config and isinstance(config, dict):
        thread_id = config.get("configurable", {}).get("thread_id")

    system_message = SystemMessage(
        content=(
            "You are a helpful assistant. For questions about the uploaded PDF, call "
            "the `rag_tool` and include the thread_id "
            f"`{thread_id}`. You can also use the web search, stock price, and "
            "calculator tools when helpful. If no document is available, ask the user "
            "to upload a PDF."
        )
    )

    messages = [system_message, *state["messages"]]
    response = llm_with_tools.invoke(messages, config=config)
    return {"messages": [response]}


tool_node = ToolNode(tools)




   
# Check Pointers

conn=sqlite3.connect(database='chatbot.db',check_same_thread=False)
# Config with thread_id
#config = {"configurable": {"thread_id": "1"}}
checkpointer = SqliteSaver(conn=conn)

# Graph

graph = StateGraph(ChatState)
graph.add_node("Chat_node",chat_node)
graph.add_node("tools",tool_node)

graph.add_edge(START, "Chat_node")
graph.add_conditional_edges("Chat_node",tools_condition)
graph.add_edge("tools","Chat_node")


chatbot=graph.compile(checkpointer=checkpointer)



# Helpers
def retrieve_all_threads():
    all_threads=set()
    for checkpoint in checkpointer.list(None):
       all_threads.add(checkpoint.config["configurable"]['thread_id'])
    return list(all_threads)

def thread_has_document(thread_id:str)->bool:
    return str(thread_id) in _THREAD_RETRIEVERS

def thread_document_metadata(thread_id: str) -> dict:
    return _THREAD_METADATA.get(str(thread_id), {})