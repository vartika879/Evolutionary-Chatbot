import streamlit as st
from backened import chatbot,retrieve_all_threads
from langchain_core.messages import HumanMessage
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
        placeholder = st.empty()
        full_response = " "

        for message_chunk, metadata in chatbot.stream(
            {'messages': [HumanMessage(content=user_input)]},
            config=CONFIG,
            stream_mode='messages'
        ):
            
            if message_chunk.content:
                full_response += message_chunk.content + " "
                placeholder.text(full_response)

        # Save final response in history
        st.session_state['messages_history'].append({'role': 'assistant', "content": full_response.strip()})
