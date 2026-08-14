from langgraph.graph import StateGraph,START, END
from typing import TypedDict, Literal, Annotated
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage,BaseMessage
from pydantic import BaseModel, Field
import operator
import os
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    groq_api_key=api_key   # ✅ correct parameter name
)



class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]

def chat_node(state:ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {'messages':[response]}


# Config with thread_id
config = {"configurable": {"thread_id": "1"}}
checkpoint = MemorySaver()
graph = StateGraph(ChatState)
graph.add_node("Chat_node",chat_node)

graph.add_edge(START, "Chat_node")
graph.add_edge("Chat_node", END)

chatbot=graph.compile(checkpointer=checkpoint)



