# ChatDC
**ChatDC** is a **chatbot** for my school **Daly College (DC), Indore**. It uses the `llama-3.1-70b-versatile` LLM along with the `Chroma` vector database to answer user queries about my school. This repository contains all the project code and code for its **GUI**. 

**Note:** *As I update the project, I'll create different versions. Currently, the first version of the project `v1` is available and I'm working on `v2`, the second version. The code for each version can be found in their relevant directories.* 

## Project Structure


## Working
- Enter the query using the GUI built with `streamlit`
- Similarity search is carried out with the contents of the vector database
- The question, along with the most similar chunks, are appended to a prompt sent to the LLM
- The LLM generates a response

## Additional Features
- History of previous conversations is provided to the LLM to maintain conversational context.
- The history of all the previous interactions is visible in GUI.

## Further Improvements
- Expanding the information about DC in the database
- Building `v2` of ChatDC using LangGraph and LangChain agents.

## License
This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Contact
For questions or suggestions, please open an issue or contact me directly:

- **Email**: adnanbarwaniwala7@gmail.com

## 🙏 Thank You
Thank you for spending time on my repo. Hope you enjoyed it!

