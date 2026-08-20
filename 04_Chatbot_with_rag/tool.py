from langgraph.prebuilt import ToolNode ,tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
import requests
import os
import tempfile
from typing import Optional,Any,Dict
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_cohere import CohereEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from pydantic import BaseModel

search_tool=DuckDuckGoSearchRun()
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    groq_api_key=api_key   # ✅ correct parameter name
)

# Initialize the embeddings model
cohere_api_key = os.getenv("COHERE_API_KEY")

embeddings = CohereEmbeddings(
    model="embed-english-light-v3.0",
    cohere_api_key=cohere_api_key
)



# -------------------
# 2. PDF retriever store (per thread)
# -------------------
_THREAD_RETRIEVERS: Dict[str, Any] = {}
_THREAD_METADATA: Dict[str, dict] = {}

def _get_retriver(thread_id:Optional[str]):
    """Fetch the retriver for a thread if available"""
    if thread_id and thread_id in _THREAD_RETRIEVERS:
        return _THREAD_RETRIEVERS[thread_id]
    return None


def ingest_pdf(file_bytes:bytes,thread_id:str,filename: Optional[str]=None) -> dict:
    """
    Build a FAISS retriever for the uploaded PDF and store it for the thread.

    Returns a summary dict that can be surfaced in the UI.
    """
    if not file_bytes:
        raise ValueError("no byte recieved for ingestion.")

    with tempfile.NamedTemporaryFile(delete=False,suffix=".pdf") as temp_file:
        temp_file.write(file_bytes)
        temp_path=temp_file.name

    try:
        loader=PyPDFLoader(temp_path)
        docs=loader.load()

        splitter=RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, separators=["\n\n", "\n", " ", ""]

        )
        chunks=splitter.split_documents(docs)

        
        print("Documents:", len(docs))

        print("Number of chunks:", len(chunks))

        if not chunks:
          raise ValueError("PDF contains no extractable text.")
        print("Testing Cohere embedding...")
        
        test_embedding = embeddings.embed_query("Hello world")
        print("Embedding dimension:", len(test_embedding))

        vector_store=FAISS.from_documents(chunks,embeddings)
        retriever=vector_store.as_retriever(
            search_type="similarity", search_kwargs={"k": 4}

        )
        _THREAD_RETRIEVERS[str(thread_id)] = retriever
        _THREAD_METADATA[str(thread_id)] = {
            "filename": filename or os.path.basename(temp_path),
            "documents": len(docs),
            "chunks": len(chunks),
        }
        return {
            "filename": filename or os.path.basename(temp_path),
            "documents": len(docs),
            "chunks": len(chunks),
        }
    finally:
        # The FAISS store keeps copies of the text, so the temp file is safe to remove.
        try:
            os.remove(temp_path)
        except OSError:
            pass


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

        return{"result":result}

    except Exception as e :
        return {"error":str(e)}

@tool
def get_stock_price(symbol:str)->dict:
    """
    Fetch the latest stock price for a given ticker symbol (e.g. "AAPL", "TSLA", "IBM").
    Use this for ANY stock-price question, even if the user gives a company name instead
    of a ticker (e.g. "Tesla" -> use "TSLA"). Do not use web search for stock prices.
    """
   
   # url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=ZPRRW3OAKAOPEGWM"
   # r=requests.get(url)
   # return r.json()


    try:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey=ZPRRW3OAKAOPEGWM"
        r = requests.get(url, timeout=10)
        return r.json()
    except Exception as e:
        return {"error": str(e)}


@tool
def rag_tool(query:str,thread_id:Optional[str]=None)->dict:
    """Retrieve relevant information from the uploaded PDF for this chat thread.
    Always include the thread_id when calling this tool."""
    retriver=_get_retriver(thread_id)
    if retriver is None:
        return {
            "erroor":"No document indexed for this chat. Upload a PDF first ",
            "query":query,

        }
    result=retriver.invoke(query)
    context=[doc.page_content for doc in result]
    metadata=[doc.metadata for doc in result]

    return {
        "query":query,
        "context":context,
        "metadata":metadata,
        "source_file": _THREAD_METADATA.get(str(thread_id), {}).get("filename"),
    
    }









tools=[get_stock_price,search_tool,calculator,rag_tool]
llm_with_tools=llm.bind_tools(tools)