import streamlit as st

from backend import chatbot
from langchain_core.messages import HumanMessage

if 'messages_history' not in st.session_state:
    st.session_state['messages_history'] = []

# Display previous messages
for msg in st.session_state['messages_history']:
    with st.chat_message(msg['role']):
        st.text(msg['content'])

user_input = st.chat_input("Type here...")

if user_input:
    # Add user message
    st.session_state['messages_history'].append({'role': 'user', "content": user_input})
    with st.chat_message('user'):
        st.text(user_input)

    # Assistant streaming reply
    with st.chat_message('assistant'):
        placeholder = st.empty()
        full_response = " "

        for message_chunk, metadata in chatbot.stream(
            {'messages': [HumanMessage(content=user_input)]},
            config={'configurable': {'thread_id': "thread_1"}},
            stream_mode='messages'
        ):
            
            if message_chunk.content:
                full_response += message_chunk.content + " "
                placeholder.text(full_response)

        # Save final response in history
        st.session_state['messages_history'].append({'role': 'assistant', "content": full_response.strip()})
