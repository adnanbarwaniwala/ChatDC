from langchain_groq import ChatGroq
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
import os


# def create_vector_store():
#     embedding_function = OpenAIEmbeddings()
#     data = TextLoader('dc_info.txt').load()
#     text_splitter = RecursiveCharacterTextSplitter(separators=['\n\n\n'], chunk_size=1024, chunk_overlap=200)
#     chunks1 = text_splitter.split_documents(data)
#     db = Chroma.from_documents(chunks1, embedding_function, persist_directory='./vector_dc_info')
#     db.persist()
#     return db


def connect_to_vector_store():
    embedding_function = OpenAIEmbeddings()
    db = Chroma(persist_directory='./vector_dc_info', embedding_function=embedding_function)
    return db


# def manage_vector_store():
#     import os
#     if os.path.exists('./vector_dc_info'):
#         db = connect_to_vector_store()
#     else:
#         db = create_vector_store()
#
#     return db


def create_system_message():
    system_template = """"You answer user queries based on context provided to you. If the context 
    does not contain relevant information to the question or sufficient information, or if it falls outside your 
    knowledge base, respond politely with 'I don't know'. This way your responses are grounded in the most relevant 
    information available to you. My school's name is Daly College, also referred to as DC."""

    system_message = SystemMessagePromptTemplate.from_template(system_template).format()
    return system_message


def create_human_message(question: str, db):
    human_template = """
    My school's name is Daly College, also referred to as DC.
    Context:
    ```{context}```

    Answer this question using the above context:
    ```{question}```

    Guidelines for Answering: 1. Base your answer primarily on the provided context. 2. If the question is general 
    and relates to a domain you have knowledge about, you may supplement the answer with relevant points. However, 
    ensure these additions are directly relevant to the user's question. 3. If the provided context does not contain 
    information related to the question, or the question is outside your knowledge domain, respond politely with 'I don't 
    know'. 4. Keep your answer concise and focused. Don't include any information that does not directly contribute 
    to answering the user's question.

    Adhere to these guidelines to ensure accurate and useful responses to the user asking questions about DC."""

    similar_contexts = db.similarity_search(question, k=2)
    context = '\n\n\n'.join([c.page_content for c in similar_contexts])
    human_message = HumanMessagePromptTemplate.from_template(human_template).format(context=context, question=question)

    return human_message


def ask_about_daly_college(messages):
    os.environ['GROQ_API_KEY'] = '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'
    llm = ChatGroq(
        model='llama-3.1-70b-versatile',
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2
    )
    return llm.invoke(messages).content
