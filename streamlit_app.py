import streamlit as st
import google.generativeai as genai
from google.api_core import exceptions

# Show title and description.
st.title("💬 Gemini Chatbot")
st.write(
    "This is a simple chatbot that uses Google's Gemini model to generate responses. "
)

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    
    # API Key input
    gemini_api_key = st.text_input("Google AI API Key", type="password", value="AIzaSyBry97WDtrisAkD52ZbbTShzoEUHenMX_w")
    
    # Model selection
    model_name = st.selectbox(
        "Select Gemini Model",
        ["gemini-1.5-flash", "gemini-1.5-pro"],
        index=0
    )
    
    # Context management
    st.header("Context Management")
    
    # Initialize context in session state if not present
    if "context" not in st.session_state:
        st.session_state.context = ""
    
    # Text area for additional context
    st.session_state.context = st.text_area(
        "Add Background Information/Context",
        st.session_state.context,
        height=200,
        help="This information will be included with every prompt sent to the model."
    )
    
    # File uploader for additional context
    uploaded_file = st.file_uploader("Or Upload a Text File", type=["txt"])
    if uploaded_file is not None:
        file_contents = uploaded_file.read().decode("utf-8")
        if st.button("Add File Contents to Context"):
            st.session_state.context += "\n\n" + file_contents
            st.experimental_rerun()
    
    # Clear context button
    if st.button("Clear Context"):
        st.session_state.context = ""
        st.experimental_rerun()

# Main chat interface
if not gemini_api_key:
    st.info("Please add your Google AI API key in the sidebar to continue.", icon="🗝️")
else:
    # Configure the Gemini API
    genai.configure(api_key=gemini_api_key)

    # Create a session state variable to store the chat messages.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field
    if prompt := st.chat_input("What is up?"):
        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            # Initialize the model
            model = genai.GenerativeModel(model_name)
            
            # Create the complete prompt by combining context and the user's prompt
            complete_prompt = prompt
            if st.session_state.context:
                complete_prompt = f"""
                Context information:
                {st.session_state.context}
                
                Based on the above context, please respond to this question or request:
                {prompt}
                """
            
            # Generate content with streaming
            with st.chat_message("assistant"):
                response_container = st.empty()
                full_response = ""
                
                # Generate content with the complete prompt
                response = model.generate_content(
                    complete_prompt,
                    stream=True
                )
                
                # Stream the response
                for chunk in response:
                    if hasattr(chunk, 'text'):
                        full_response += chunk.text
                        response_container.markdown(full_response)
                    
                # Store the response (only storing the original prompt, not the context-enhanced one)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            st.info("Please check if your API key has access to Gemini 1.5 models.")

    # Add a button to clear the chat history
    if st.session_state.messages and st.button("Clear Conversation"):
        st.session_state.messages = []
        st.experimental_rerun()
