import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain.memory import ConversationBufferWindowMemory
from v3_functions import *

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

st.info("If ChatDC isn’t able to answer your question, please try being more specific "
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
user_query = st.chat_input("Ask about Daly College")

# Footer with disclaimer
import streamlit.components.v1 as components

components.html(
    """
    <script>
      // Create the footer element in the parent document if it doesn't exist.
      function createFooter() {
          if (window.parent && window.parent.document) {
              if (!window.parent.document.getElementById('dynamic-footer')) {
                  var footer = window.parent.document.createElement('div');
                  footer.id = 'dynamic-footer';
                  footer.innerHTML = "ChatDC can make mistakes. Check important info.";
                  window.parent.document.body.appendChild(footer);

                  // Create and append a <style> tag to style the footer.
                  var style = window.parent.document.createElement('style');
                  style.innerHTML = `
                    #dynamic-footer {
                        position: fixed;
                        bottom: 10px;
                        left: 50%;
                        transform: translateX(-50%);
                        padding: 5px 10px;
                        border-radius: 5px;
                        font-size: 0.9em;
                        transition: transform 0.1s ease-out;
                        z-index: 9999;
                        color: grey;
                        background: transparent;
                    }
                  `;
                  window.parent.document.head.appendChild(style);
              }
          }
      }

      // Adjust the footer position based on the sidebar's width.
      function adjustFooter() {
          var sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
          var footer = window.parent.document.getElementById('dynamic-footer');
          if (sidebar && footer) {
              var sidebarWidth = sidebar.offsetWidth;
              if (sidebarWidth > 0) {
                  // Sidebar is open: shift footer 50px right from center.
                  footer.style.transform = "translateX(calc(-50% + 50px))";
              } else {
                  // Sidebar is closed: shift footer 20px left from center.
                  footer.style.transform = "translateX(calc(-50% - 20px))";
              }
          }
      }

      // Initialize the footer.
      createFooter();

      // Try to select the sidebar element.
      var sidebarElement = window.parent.document.querySelector('[data-testid="stSidebar"]');

      // Use ResizeObserver to catch size changes of the sidebar.
      if (sidebarElement && window.ResizeObserver) {
          const resizeObserver = new ResizeObserver(function(entries) {
              adjustFooter();
          });
          resizeObserver.observe(sidebarElement);
      }

      // Use MutationObserver to catch changes in sidebar attributes (such as class or inline styles).
      if (sidebarElement && window.MutationObserver) {
          const mutationObserver = new MutationObserver(function(mutationsList) {
              adjustFooter();
          });
          mutationObserver.observe(sidebarElement, { attributes: true, attributeFilter: ['style', 'class'] });
      }

      // Also update on parent window resize.
      window.parent.addEventListener('resize', adjustFooter);

      // Fallback: if neither observer is available, poll at 100ms intervals.
      if (!window.ResizeObserver && !window.MutationObserver) {
          setInterval(adjustFooter, 100);
      }
    </script>
    """,
    height=0)

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
