import streamlit as st
from backend import chatbot,retrieve_all_threads
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

add_thread(st.session_state['thread_id'])

#*******************************Sidebar***************************************
st.sidebar.title("ChatBot using LangGraph")

if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("My Conversations")

for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id']=thread_id

        messages = load_conversation(thread_id)

        temp_messages=[]
        for message in messages:
            if isinstance(message,HumanMessage):
                role='user'
            else:
                role='assistant'
            temp_messages.append({'role':role,'content':message.content})

        st.session_state['messages_history'] = temp_messages


#*******************************Main UI ******************************************



# loading the conversation history
for msg in st.session_state['messages_history']:
    with st.chat_message(msg['role']):
        st.text(msg['content'])

user_input = st.chat_input("Type here...")

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
                        status_holder["box"].update(label=label, state="complete")







                if isinstance(message_chunk,AIMessage) and message_chunk.content:
                    yield message_chunk.content

        ai_message=st.write_stream(ai_only_stream)

        #placeholder = st.empty()
        #full_response = " "
        if status_holder["box"] is not None:
            status_holder["box"].update(state="complete")
        

        # Save final response in history
    st.session_state['messages_history'].append({'role': 'assistant', "content": (ai_message or "").strip()})
