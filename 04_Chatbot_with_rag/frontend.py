import streamlit as st
from backend import chatbot,retrieve_all_threads,thread_document_metadata
from tool import ingest_pdf
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage
import uuid



#********************************Utility function***************************
def generate_thread_id():
    thread_id=uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id=generate_thread_id()
    st.session_state['thread_id']=thread_id
    add_thread(thread_id)#add_thread(st.session_state['thread_id'])
    st.session_state['messages_history']=[]

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
      st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    CONFIG={'configurable': {"thread_id":thread_id}}
    state=chatbot.get_state(config=CONFIG)

    return state.values.get("messages",[])


#*********************************SEssion Setup********************************
if 'messages_history' not in st.session_state:
    st.session_state['messages_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id']=generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads']=retrieve_all_threads()

if "ingested_docs" not in st.session_state:
    st.session_state["ingested_docs"] = {}

add_thread(st.session_state['thread_id'])

thread_key = str(st.session_state["thread_id"])
thread_docs = st.session_state["ingested_docs"].setdefault(thread_key, {})
threads = st.session_state["chat_threads"][::-1]
selected_thread = None


#*******************************Sidebar***************************************
st.sidebar.title("ChatBot using LangGraph")
st.sidebar.markdown(f"**Thread ID:** `{thread_key}`")


if st.sidebar.button("New Chat"):
    reset_chat()
    st.rerun


if thread_docs:
    latest_doc = list(thread_docs.values())[-1]
    st.sidebar.success(
        f"Using `{latest_doc.get('filename')}` "
        f"({latest_doc.get('chunks')} chunks from {latest_doc.get('documents')} pages)"
    )
else:
    st.sidebar.info("No PDF indexed yet.")

uploaded_pdf = st.sidebar.file_uploader("Upload a PDF for this chat", type=["pdf"])
if uploaded_pdf:
    if uploaded_pdf.name in thread_docs:
        st.sidebar.info(f"`{uploaded_pdf.name}` already processed for this chat.")
    else:
        with st.sidebar.status("Indexing PDF…", expanded=True) as status_box:
            summary = ingest_pdf(
                uploaded_pdf.getvalue(),
                thread_id=thread_key,
                filename=uploaded_pdf.name,
            )
            thread_docs[uploaded_pdf.name] = summary
            status_box.update(label="✅ PDF indexed", state="complete", expanded=False)

st.sidebar.subheader("Past conversations")
if not threads:
    st.sidebar.write("No past conversations yet.")
else:
    for thread_id in threads:
        if st.sidebar.button(str(thread_id), key=f"side-thread-{thread_id}"):
            selected_thread = thread_id


#*******************************Main UI ******************************************
st.title("🧠 OrchestrAI")
st.caption("Your Intelligent AI Workspace")


# loading the conversation history
for msg in st.session_state['messages_history']:
    with st.chat_message(msg['role']):
        st.text(msg['content'])

user_input = st.chat_input("Ask about your document or ask anything use tools...")

if user_input:
    # Add user message
    st.session_state['messages_history'].append({'role': 'user', "content": user_input})
    with st.chat_message('user'):
        st.text(user_input)


    CONFIG={'configurable': {'thread_id': st.session_state['thread_id']},
            "metadata":{'thread_id': st.session_state['thread_id']},
            "run_name":"chat_turn"
            }
    # Assistant streaming reply
    with st.chat_message('assistant'):
        status_holder={"box":None}

        def ai_only_stream():
            for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode='messages'
           ):
             # 1) LLM has decided to call one or more tools
                tool_calls = getattr(message_chunk, "tool_calls", None)
                if tool_calls:
                    for call in tool_calls:
                        tool_name = call.get("name", "tool")
                        label = f"🔧 Using tool: `{tool_name}` ..."
                        if status_holder["box"] is None:
                            status_holder["box"] = st.status(label, expanded=False)
                        else:
                            status_holder["box"].update(label=label)


                # 2) A tool has finished and returned its result
                if isinstance(message_chunk, ToolMessage):
                    tool_name = getattr(message_chunk, "name", "tool")
                    label = f"✅ Got result from `{tool_name}`"
                    if status_holder["box"] is None:
                        status_holder["box"] = st.status(label, expanded=False)
                    else:
                        status_holder["box"].update(label=label, state="running",expanded=True)







                if isinstance(message_chunk,AIMessage) and message_chunk.content:
                    yield message_chunk.content

        ai_message=st.write_stream(ai_only_stream)

        #placeholder = st.empty()
        #full_response = " "
        if status_holder["box"] is not None:
            status_holder["box"].update(
                label="✅ Tool finished", state="complete", expanded=False
                )
        

        # Save final response in history
    st.session_state['messages_history'].append({'role': 'assistant', "content": (ai_message or "").strip()})

    doc_meta = thread_document_metadata(thread_key)
    if doc_meta:
        st.caption(
            f"Document indexed: {doc_meta.get('filename')} "
            f"(chunks: {doc_meta.get('chunks')}, pages: {doc_meta.get('documents')})"
        )

st.divider()

if selected_thread:
    st.session_state["thread_id"] = selected_thread
    messages = load_conversation(selected_thread)

    temp_messages = []
    for msg in messages:
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        temp_messages.append({"role": role, "content": msg.content})
    st.session_state["message_history"] = temp_messages
    st.session_state["ingested_docs"].setdefault(str(selected_thread), {})
    st.rerun()
