from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
import streamlit as st


def connect_to_vector_store():
    embedding_function = OpenAIEmbeddings(model='text-embedding-3-small', api_key=st.secrets['general']['openai_api_key'])
    db = Chroma(persist_directory='./vector_dc_info', embedding_function=embedding_function)
    return db


def create_system_message():
    system_template = """"You're a chatbot that assists users with queries about my school Daly College, also called DC.
    You have a friendly conversation with them, answering all their queries very accurately."""
    system_message = SystemMessage(content=system_template)
    return system_message


def create_human_message(question: str, db):
    human_template = """
    My school's name is Daly College, also referred to as DC.
    Context:
    ```{}```

    Query:
    ```{}```

    Guidelines for Answering:
    - If the user query is general and not related to DC, answer it using your knowledge and without the context.
    - Else use the context to answer the query if it's related to DC.
    - If neither the context nor your knowledge provides an answer, apologize and politely state you don't know the answer.
    - Answer concisely. Don't include any unnecessary information."""

    similar_contexts = db.similarity_search(question, k=2)
    context = '\n\n\n'.join([c.page_content for c in similar_contexts])
    human_message = HumanMessage(content=human_template.format(context, question))

    return human_message


def ask_about_daly_college(messages):
    import streamlit as st
    groq_api_key = st.secrets["general"]["groq_api_key"]
    llm = ChatGroq(
        model='llama-3.1-70b-versatile',
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=groq_api_key
    )
    return llm.invoke(messages).content
