# ChatDC

**ChatDC** is a **chatbot** designed for **Daly College (DC), Indore**. Powered by the `Deepseek-R1` LLM and the `Chroma` vector database, it provides detailed responses to queries about the school. This repository includes all project code, including the **GUI**.

> **Note:** This project is versioned. Each version's code is in its respective directory.

## Project Structure

### 📁 `v3` - Third (Latest) Version

- **`vector_dc_info/`**: Stores the vectorized information about DC as embeddings.
- **`dc_info.txt`**: A text file with comprehensive details about Daly College. Its information is vectorised and stored in the `vector_dc_nfo` directory.
- **`v3_functions.py`**: Functions used across the project.
- **`1_Overview.py`**: Code for the GUI of the project's welcome page.
- **`pages/2_ChatDC.py`**: Code for GUI of the project's main page. It allows the user to ask questions about Daly College. 

## Features and Working

1. **Query Submission**: Enter your query via the Streamlit-based GUI.
2. **Query Expansion**: The query is expanded by the `Deepseek-R1 LLM` to improve its clarity and to include the context of previous interactions if required. 
3. **Similarity Search**: The expanded query is matched against the vector database.
4. **LLM Response**: The most similar chunks are appended to the query and sent to the LLM, which generates a response.
5. **Context Maintenance**: The chatbot maintains conversational context using previous interactions.
6. **Expandable Database**: The database can be expanded to include more information about Daly College.

## Version 2 Improvements
- **Expanded Event Coverage**  
  ChatDC can now answer questions about almost all 2023 events and activities at Daly College.

## Version 3 Improvements
- **Enhanced Knowledge Base**  
  Can provide in-depth information on school facilities, educational boards, and faculty details now.
- **Advanced LLM Upgrade**  
  Switched from `Llama-3.3-70b-versatile` to **Deepseek-R1** for more accurate, context-aware answers.  
- **Real-Time Response Streaming**  
  Answers from the LLM are streamed to the user in real time.  
- **Improved User Interface**  
  Added a new welcome page that provides an overview of the app and its features.
 
## Website
You can try out the latest version of ChatDC here: [**ChatDC**](https://chatdc.onrender.com)

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or suggestions, feel free to open an issue or reach out:

- **Email**: [adnanbarwaniwala7@gmail.com](mailto:adnanbarwaniwala7@gmail.com)

## 🙏 Thank You

Thank you for exploring ChatDC! I hope you find it useful.
