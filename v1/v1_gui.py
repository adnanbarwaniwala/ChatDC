from langchain_core.messages import AIMessage
from langchain.memory import ConversationBufferWindowMemory
from v1_functions import *
import streamlit as st
from streamlit_chat import message

st.set_page_config(
    page_title='ChatDC',
    page_icon=':robot_face:'
)
st.subheader('ChatDC :robot_face:')

if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'db' not in st.session_state:
    st.session_state.db = connect_to_vector_store()
if 'user_questions' not in st.session_state:
    st.session_state.user_questions = []
if 'memory' not in st.session_state:
    st.session_state.memory = ConversationBufferWindowMemory(k=2, return_messages=True)

llm_msgs = [create_system_message()]
with st.sidebar:
    user_prompt = st.text_input(label='Ask about DC:')
    if user_prompt and user_prompt != '':
        human_message = create_human_message(user_prompt, st.session_state.db)
        st.session_state.messages.append(human_message)
        st.session_state.user_questions.append(user_prompt)

        if len(st.session_state.memory.load_memory_variables({})['history']) >= 2:
            llm_msgs.extend(st.session_state.memory.load_memory_variables({})['history'])
        llm_msgs.append(human_message)

        with st.spinner('Working on your request ...'):
            response = ask_about_daly_college(llm_msgs)

        ai_message = AIMessage(content=response)
        st.session_state.messages.append(ai_message)

        st.session_state.memory.chat_memory.add_user_message(human_message.content)
        st.session_state.memory.chat_memory.add_ai_message(ai_message.content)

for i, msg in enumerate(st.session_state.messages):
    if i % 2 == 0:
        message(st.session_state.user_questions[i // 2], is_user=True, key=f'{i}+ :nerd_face:')
    else:
        message(msg.content, is_user=False, key=f'{i} + :robot_face:')
