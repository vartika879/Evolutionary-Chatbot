from langgraph.graph import StateGraph,START, END
from typing import TypedDict, Literal, Annotated
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage,BaseMessage
from pydantic import BaseModel, Field
import operator
from langgraph.prebuilt import ToolNode,tools_condition,
import os
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from tools import llm_with_tools,tools
import asyncio

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    groq_api_key=api_key   # ✅ correct parameter name
)



class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]

def chat_node(state:ChatState):
    """LLM node that may answer or request a tool call"""
    messages = state['messages']
    response = llm_with_tools.invoke(messages)
    return {'messages':[response]}
tool_node=ToolNode(tools)




conn=sqlite3.connect(database='chatbot.db',check_same_thread=False)
# Config with thread_id
config = {"configurable": {"thread_id": "1"}}
checkpointer = SqliteSaver(conn=conn)



graph = StateGraph(ChatState)
graph.add_node("Chat_node",chat_node)
graph.add_node("tools",tool_node)

graph.add_edge(START, "Chat_node")
graph.add_conditional_edges("Chat_node",tools_condition)
graph.add_edge("tools","chat_node")


chatbot=graph.compile(checkpointer=checkpointer)
def retrieve_all_threads():
    all_threads=set()
    for checkpoint in checkpointer.list(None):
       all_threads.add(checkpoint.config["configurable"]['thread_id'])

    return list(all_threads)