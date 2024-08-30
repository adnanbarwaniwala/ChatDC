# ChatDC

**ChatDC** is a **chatbot** designed for **Daly College (DC), Indore**. Powered by the `llama-3.1-70b-versatile` LLM and the `Chroma` vector database, it provides detailed responses to queries about the school. This repository includes all project code, including the **GUI**.

> **Note:** This project is versioned. The first version (`v1`) is currently available, with `v2` under development. Each version's code is in its respective directory.

## Project Structure

### 📁 `v1` - First Version

- **`vector_dc_info/`**: Contains the vector database storing the vectorized information about DC.
- **`dc_info.txt`**: A text file with comprehensive details about Daly College.
- **`v1_functions.py`**: Functions used across the project.
- **`v1_gui.py`**: Code for the project's **Graphical User Interface** (GUI).

## How It Works

1. **Query Submission**: Enter your query via the Streamlit-based GUI.
2. **Similarity Search**: The query is matched against the vector database.
3. **LLM Response**: The most similar chunks are appended to the query and sent to the LLM, which generates a response.
4. **Context Maintenance**: The chatbot maintains conversational context using previous interactions.

## Features

- **Conversation History**: Previous interactions are visible in the GUI and provided to the LLM for context.
- **Expandable Database**: The database can be expanded to include more information about Daly College.

## Future Plans

- **Database Expansion**: Adding more information about Daly College.
- **`v2` Development**: Building the next version using LangGraph and LangChain agents.

## Webiste
I tried deploying my app on Streamit Cloud, but due to some errors, it isn't working. I'm trying to resolve them.
If you want to check out my website: [**ChatDC**](https://chat-dc.streamlit.app)

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or suggestions, feel free to open an issue or reach out:

- **Email**: [adnanbarwaniwala7@gmail.com](mailto:adnanbarwaniwala7@gmail.com)

## 🙏 Thank You

Thank you for exploring ChatDC! I hope you find it useful.
