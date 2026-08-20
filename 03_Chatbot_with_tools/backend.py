from langgraph.graph import StateGraph,START, END
from typing import TypedDict, Literal, Annotated
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage,BaseMessage
from pydantic import BaseModel, Field
import operator
from langgraph.prebuilt import ToolNode,tools_condition
import os
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from tool import llm_with_tools,tools

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    groq_api_key=api_key   # ✅ correct parameter name
)



class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]

SYSTEM_PROMPT = SystemMessage(content="""You are a helpful assistant with access to three tools:

1. calculator - use ONLY for arithmetic (add, sub, mul, div) between two numbers.
   Example: "what is 45 * 12", "divide 100 by 4".

2. get_stock_price - use this for ANY question about a stock's current/latest price,
   for ANY company, even if the user only gives the company name and not the ticker.
   You must figure out the correct ticker symbol yourself from your own knowledge and
   pass it to the tool. Do NOT use search_tool to look up the ticker or the price.
   Common examples: Tesla -> TSLA, Apple -> AAPL, Microsoft -> MSFT, Google/Alphabet -> GOOGL,
   Amazon -> AMZN, Meta/Facebook -> META, IBM -> IBM, Netflix -> NFLX, Nvidia -> NVDA.
   If you are unsure of the exact ticker, make your best guess based on the company name
   and call get_stock_price with it anyway — never fall back to search_tool for this.

3. search_tool (DuckDuckGo search) - use ONLY for questions that need current/real-time
   information from the web that is NOT a stock price and NOT a calculation, such as
   news, weather, or general facts you don't already know.

Rules:
- Math question -> ALWAYS calculator. Never search_tool.
- ANY question mentioning a stock, share, or company's price -> ALWAYS get_stock_price
  with your best-guess ticker symbol. NEVER use search_tool for this, even if you are
  not 100% sure of the ticker.
- If you can answer directly from your own knowledge without needing live/current data,
  just answer directly without calling any tool.
- Use search_tool only when none of the above apply.
""")

def chat_node(state:ChatState):
    """LLM node that may answer or request a tool call"""
    messages = state['messages']
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [SYSTEM_PROMPT] + messages
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
graph.add_edge("tools","Chat_node")


chatbot=graph.compile(checkpointer=checkpointer)
def retrieve_all_threads():
    all_threads=set()
    for checkpoint in checkpointer.list(None):
       all_threads.add(checkpoint.config["configurable"]['thread_id'])

    return list(all_threads)