import streamlit as st
import google.generativeai as genai
from google.api_core import exceptions

# Show title and description.
st.title("💬 Gemini Chatbot")
st.write(
    "This is a simple chatbot that uses Google's Gemini model to generate responses. "
    "To use this app, you need to provide a Google AI Studio API key, which you can get from Google AI Studio. "
)

# Ask user for their Gemini API key via `st.text_input`.
gemini_api_key = st.text_input("Google AI API Key", type="password", value="AIzaSyBry97WDtrisAkD52ZbbTShzoEUHenMX_w")
if not gemini_api_key:
    st.info("Please add your Google AI API key to continue.", icon="🗝️")
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
            # Use only the recommended newer model
            model_name = "gemini-1.5-flash"
            st.info(f"Using model: {model_name}")
            
            # Initialize the model
            model = genai.GenerativeModel(model_name)
            
            # Generate content with streaming
            with st.chat_message("assistant"):
                response_container = st.empty()
                full_response = ""
                
                # Generate content based on the current prompt only
                response = model.generate_content(
                    prompt,
                    stream=True
                )
                
                # Stream the response
                for chunk in response:
                    if hasattr(chunk, 'text'):
                        full_response += chunk.text
                        response_container.markdown(full_response)
                    
                # Store the response
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            
            # Try alternative approach with a different model if first one fails
            try:
                st.info("Trying alternative model: gemini-1.5-pro")
                model = genai.GenerativeModel("gemini-1.5-pro")
                
                with st.chat_message("assistant"):
                    response_container = st.empty()
                    
                    # Generate simple non-streaming response as fallback
                    response = model.generate_content(prompt)
                    if hasattr(response, 'text'):
                        response_container.markdown(response.text)
                        st.session_state.messages.append({"role": "assistant", "content": response.text})
                    else:
                        response_container.markdown("Failed to generate a response.")
                        
            except Exception as fallback_error:
                st.error(f"Alternative model also failed: {str(fallback_error)}")
                st.info("Please check if your API key has access to Gemini 1.5 models.")
