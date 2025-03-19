import streamlit as st
import google.generativeai as genai

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

        # Convert the message format to work with Gemini
        gemini_messages = []
        for message in st.session_state.messages:
            role = "user" if message["role"] == "user" else "model"
            gemini_messages.append({"role": role, "parts": [{"text": message["content"]}]})

        # Generate a response using the Gemini API
        try:
            # Initialize the Gemini model
            model = genai.GenerativeModel('gemini-pro')
            
            # Create a chat session
            chat = model.start_chat(history=gemini_messages[:-1])
            
            # Generate the response with streaming
            with st.chat_message("assistant"):
                response_container = st.empty()
                full_response = ""
                
                # Send the last user message
                response = chat.send_message(
                    gemini_messages[-1]["parts"][0]["text"],
                    stream=True
                )
                
                # Stream the response
                for chunk in response:
                    if hasattr(chunk, 'text'):
                        full_response += chunk.text
                        response_container.markdown(full_response)
            
            # Store the assistant's response
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
