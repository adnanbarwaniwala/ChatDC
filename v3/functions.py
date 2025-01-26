from langchain_openai import OpenAIEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from openai import OpenAI
import streamlit as st
import chardet
import tiktoken


def create_vector_store():
    embedding_function = OpenAIEmbeddings(api_key=st.secrets['general']['openai_api_key'])
    with open("dc_info.txt", 'rb') as f:
        result = chardet.detect(f.read())
        encoding = result['encoding']
    data = TextLoader("dc_info.txt", encoding=encoding).load()

    text_splitter = RecursiveCharacterTextSplitter(separators=['\n\n\n'], chunk_size=1024, chunk_overlap=200)
    chunks = text_splitter.split_documents(data)
    db = Chroma.from_documents(chunks, embedding_function, persist_directory='./vector_dc_info')
    return db


def connect_to_vector_store():
    embedding_function = OpenAIEmbeddings(api_key=st.secrets['general']['openai_api_key'])
    db = Chroma(persist_directory='./vector_dc_info', embedding_function=embedding_function)
    return db


def manage_vector_store():
    import os
    if os.path.exists('vector_dc_info'):
        db = connect_to_vector_store()
    else:
        db = create_vector_store()

    return db


def create_system_message():
    system_template = """"You're a chatbot that assists users with queries about my school Daly College, also called DC.
    You have a friendly conversation with them, answering all their queries very accurately."""
    system_message = SystemMessage(content=system_template)
    return system_message


def create_human_message(prv_messages, question: str, db):
    with st.spinner("Expanding user query...."):
        client = OpenAI(api_key=st.secrets['general']['deepseek_api_key'], base_url="https://api.deepseek.com")

        messages = [{
            'role': 'system',
            'content': """You are part of a school chatbot system. The school is Daly College (DC)."""
        }]
        for index, message in enumerate(prv_messages):
            if index % 2 == 0:
                messages.append({'role': 'user', 'content': message.content})
            else:
                messages.append({'role': 'assistant', 'content': message.content})

        messages.append({
            'role': 'user',
            # 'content': f"""Using the context of these previous conversations, frame this user query into a proper question \
            # that can be sent to a vector database to retrieve appropriate contexts related to the user query. Only provide \
            # the final question and no other text. The question should be short and concise.
            # User query: {question}"""

            'content': f"""You have access to the conversation history between a user and AI, as well as a 
            new user question. The new user question is: {question}
            Your task is as follows:
            1. Determine if the new question depends on the conversation history.
                - If it does rely on the conversation history, reframe or expand the question to incorporate any relevant 
                details so that it becomes self-contained and clear.
                - If it does not rely on the conversation history or if its the first user question, leave the question 
                unchanged.
            2. Output only the final version of the question —either revised or original— without any additional commentary 
            or explanation.
            3. Whenever you're thinking of mentioning Daly College in the final version of the question, mention it as 
            DC always.
            4. If the user is asking an event's date, it's mentioned in the school calendar. Add to the final version of 
            the question that the required info is mentioned in the school calendar."""
        })

        response = client.chat.completions.create(
            model="deepseek-reasoner",
            messages=messages
        )

        llm_question = response.choices[0].message.content
    with st.sidebar:
        with st.expander("Expanded Question Reasoning"):
            st.write(response.choices[0].message.reasoning_content)
        with st.expander("Expanded Question"):
            st.write(llm_question)


    with st.spinner("Retrieving relevant contexts..."):
        similar_contexts = db.similarity_search(llm_question, k=3)
        # tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")
        # total_tokens = 0
        # included_contexts = []
        # for context in similar_contexts:
        #     context_tokens = len(tokenizer.encode(context.page_content))
        #     if total_tokens + context_tokens <= 4000:
        #         included_contexts.append(context)
        #         total_tokens += context_tokens
        #     else:
        #         break

        human_template = """My school's name is Daly College, also referred to as DC.
        Context:
        ```{}```

        Query:
        ```{}```

        Guidelines for Answering:
        - If the user query is general and not related to DC, answer it using your own knowledge and without the context.
        - Else use the context to answer the query if it's related to DC.
        - If neither the context nor your knowledge provides an answer, apologize and politely state you don't know the answer.
        - Answer concisely. Don't include any unnecessary information."""

        context = '\n\n\n'.join([c.page_content for c in similar_contexts])
        human_message = HumanMessage(content=human_template.format(context, question))

        with st.sidebar:
            with st.expander("Human Message"):
                st.write(human_message.content)

        return human_message


def ask_about_daly_college(msgs):
    with st.spinner("Querying model..."):
        client = OpenAI(api_key=st.secrets['general']['deepseek_api_key'], base_url="https://api.deepseek.com")

        messages = [{"role": "system", "content": msgs[0].content}]
        for index, message in enumerate(msgs[1:]):
            if index % 2 == 0:
                messages.append({'role': 'user', 'content': message.content})
            else:
                messages.append({'role': 'assistant', 'content': message.content})

        with st.sidebar:
            with st.expander("Messages sent to LLM"):
                st.write(messages)

        response = client.chat.completions.create(
            model="deepseek-reasoner",
            messages=messages,
            stream=True
        )
        return response

