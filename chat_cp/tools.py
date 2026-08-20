from langgraph.prebuilt import ToolNode ,tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
import requests
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
search_tool=DuckDuckGoSearchRun(region="us-en")
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    groq_api_key=api_key   # ✅ correct parameter name
)

@tool
def calculator(first_num:float, second_num:float,operation:str)->dict:
    """
    Perform a basic arithmetic operation on two numbers.
    Supported operation add,sub,mul,div
    """
    try:
        if operation=="add":
            result=first_num + second_num

        elif operation=="sub":
            result=first_num - second_num

        elif operation=="mul":
            result=first_num * second_num

        elif operation=="div":
            if second_num==0:
                return {"error":"Division by zero is not allowed"}
            result=first_num / second_num

        else:
            return {"error":f"Unsupported operation '{operation}"}

    except Exception as e :
        return {"error":str(e)}

@tool
def get_stock_price(symbol:str)->dict:
    """
    Fetch latest stock Price for a given ymbol (e.g. "APPL","TSLA)
    Using Alpha Vantage with api key in the Url.
    """
   
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=ZPRRW3OAKAOPEGWM"
    r=requests.get(url)
    return r.json()

        
tools=[get_stock_price,search_tool,calculator]
llm_with_tools=llm.bind_tools(tools)