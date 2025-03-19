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

    # Show available models for debugging
    try:
        models = [m.name for m in genai.list_models()]
        with st.expander("Available Gemini models"):
            st.write(models)
    except Exception as e:
        st.warning(f"Could not list available models: {str(e)}")

    # Create a chat input field
    if prompt := st.chat_input("What is up?"):
        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            # Find a model name that contains "gemini"
            gemini_model_name = None
            try:
                for model in genai.list_models():
                    if "gemini" in model.name.lower():
                        gemini_model_name = model.name
                        break
            except:
                # Fallback to common model names if listing fails
                gemini_model_name = "models/gemini-1.0-pro"
            
            if not gemini_model_name:
                # Hardcoded fallback options to try with newer recommended models first
                model_options = [
                    "gemini-1.5-flash",
                    "models/gemini-1.5-flash",
                    "gemini-1.5-pro",
                    "models/gemini-1.5-pro"
                ]
            else:
                model_options = [gemini_model_name]
                
            # Try different model name formats
            success = False
            last_error = None
            
            for model_name in model_options:
                try:
                    st.info(f"Trying model: {model_name}")
                    
                    # Initialize the model with the current name format
                    model = genai.GenerativeModel(model_name)
                    
                    # Prepare the content for the generation
                    messages = []
                    for msg in st.session_state.messages:
                        if msg["role"] == "user":
                            messages.append({"role": "user", "parts": [msg["content"]]})
                        else:
                            messages.append({"role": "model", "parts": [msg["content"]]})
                    
                    # Generate content with simple prompt approach
                    with st.chat_message("assistant"):
                        response_container = st.empty()
                        full_response = ""
                        
                        # Try simple content generation instead of chat
                        response = model.generate_content(
                            prompt,
                            stream=True
                        )
                        
                        for chunk in response:
                            if hasattr(chunk, 'text'):
                                full_response += chunk.text
                                response_container.markdown(full_response)
                            
                    # Store the response
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                    
                    success = True
                    break
                
                except Exception as e:
                    last_error = str(e)
                    continue
            
            if not success:
                st.error(f"Failed to generate response with any model variant: {last_error}")
                
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            st.info("Try checking if your API key is correct and has access to Gemini models.")
