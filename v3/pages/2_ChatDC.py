import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain.memory import ConversationBufferWindowMemory
from functions import *

st.set_page_config(
    page_title='ChatDC',
    page_icon=':robot_face:'
)

col1, col2 = st.columns([1, 4])  # Create two columns for alignment
with col1:
    # Add the circular image
    st.image('daly_college_logo.png', use_column_width=False)
with col2:
    st.markdown(
        """
        <h1 style="vertical-align: middle; font-size: 30px; margin: 0;">
            ChatDC 🤖
        </h1>
        """,
        unsafe_allow_html=True,
    )

st.info("If the ChatDC isn’t able to answer your question, please try being more specific "
        "and include all relevant information.", icon="ℹ️")

if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'db' not in st.session_state:
    st.session_state.db = manage_vector_store()
if 'memory' not in st.session_state:
    st.session_state.memory = ConversationBufferWindowMemory(k=2, return_messages=True)


# chat history
for message in st.session_state.messages:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

# user input
llm_msgs = [create_system_message()]
user_query = st.chat_input("Ask about DC...")

# Footer with disclaimer
st.markdown(
    """
    <style>
        /* Styling for footer */
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: transparent;
            color: gray;
            text-align: center;
            padding: 15px;
            font-size: 13.5px;
            z-index: 1000; /* Ensures it stays above other elements */
        }
    </style>
    <div class="footer">
        ChatDC can make mistakes. Check important info.
    </div>
    """,
    unsafe_allow_html=True
)

# Generating an answer
if user_query and user_query != "":
    with st.chat_message("Human"):
        st.markdown(user_query)
        if len(st.session_state.memory.load_memory_variables({})['history']) >= 2:
            llm_msgs.extend(st.session_state.memory.load_memory_variables({})['history'])
        human_message = create_human_message(llm_msgs[1:], user_query, st.session_state.db)

        st.session_state.messages.append(HumanMessage(content=user_query))
        llm_msgs.append(human_message)

    with st.chat_message("AI"):
        response_iterable = ask_about_daly_college(llm_msgs)
        with st.spinner("Generating the response..."):
            response = st.write_stream(response_iterable)

    st.session_state.messages.append(AIMessage(content=response))
    st.session_state.memory.chat_memory.add_user_message(user_query)
    st.session_state.memory.chat_memory.add_ai_message(response)
