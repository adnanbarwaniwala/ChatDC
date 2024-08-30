# ChatDC
**ChatDC** is a **chatbot** for my school **Daly College (DC), Indore**. It uses the `llama-3.1-70b-versatile` LLM along with the `Chroma` vector database to answer user queries about my school. This repository contains all the project code, along with code for its **GUI**. 

## Working
- Enter the query using the GUI built with `streamlit`
- Similarity search is carried out with the contents of the vector database
- The question, along with the most similar chunks, are appended to a prompt sent to the LLM
- The LLM generates a response

## Additiional Features
- History of previous conversations is provided to the LLM to maintain conversational context.
- The history of all the previous interactions are visible in GUI.

## Further Improvements
- Expanding the information about DC in the database
- Building `v2` of ChatDC using LangGraph and LangChain agents.

