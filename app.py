import streamlit as st
from agent import BigQueryAgent

# 1. Page Configuration
st.set_page_config(
    page_title="BigQuery Data Agent",
    page_icon="🤖",
    layout="wide"
)

with st.sidebar:
    st.header("Settings")
    # Creates a toggle switch (True/False)
    show_charts = st.toggle("Generate Charts", value=True)

st.title("🤖 BigQuery Data Agent")

# 2. Initialize Agent in Session State (so it remembers context)
if "agent" not in st.session_state:
    with st.spinner("Initializing Vertex AI & BigQuery Connection..."):
        st.session_state.agent = BigQueryAgent()
    st.success("Agent Ready!")

# 3. Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # If there was a plot or SQL in history, we could render it here
        # For simplicity, we render visuals immediately after generation below

# 4. Handle User Input
if prompt := st.chat_input("Ask a question about your data..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.agent.process_request(prompt, enable_plot=show_charts)
            
            # A. Display Natural Language Answer
            st.markdown(response['answer'])
            
            # B. Display Plot (Only if it exists)
            if response.get('plot'):
                st.pyplot(response['plot'])
            
            # C. Display SQL (in an expander for transparency)
            with st.expander("View Generated SQL"):
                st.code(response['sql'], language='sql')
                
            # D. Display Raw Data (Only if it exists)
            if response.get('dataframe') is not None:
                with st.expander("View Raw Data"):
                    st.dataframe(response['dataframe'])

    # Save assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response['answer']})
