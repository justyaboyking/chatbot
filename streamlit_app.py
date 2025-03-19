import streamlit as st
import requests
import json
import time

# Show title and description.
st.title("💬 Nvidia Llama 3.3 Nemotron Super 49B Chatbot")
st.write(
    "This is a simple chatbot that uses Nvidia's Llama 3.3 Nemotron Super 49B model to generate responses. "
    "The API key is pre-filled, but you can change it if needed."
)

# Configure API settings
st.sidebar.header("API Configuration")
nvidia_api_key = st.sidebar.text_input(
    "Nvidia API Key", 
    type="password", 
    value="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"
)

model_name = st.sidebar.text_input(
    "Model Name", 
    value="NVIDIABuild-Autogen-30"
)

temperature = st.sidebar.slider(
    "Temperature", 
    min_value=0.0, 
    max_value=1.0, 
    value=0.7, 
    step=0.1
)

max_tokens = st.sidebar.slider(
    "Max Tokens", 
    min_value=100, 
    max_value=2000, 
    value=800, 
    step=100
)

# Toggle advanced debugging
debug_mode = st.sidebar.checkbox("Debug Mode")

# Allow selecting between different API endpoints
api_endpoint = st.sidebar.selectbox(
    "API Endpoint",
    options=[
        "https://api.nvidia.com/v1/chat/completions",
        "https://build.nvidia.com/v1/chat/completions",
        "https://build.nvidia.com/api/v1/chat/completions",
        "https://build.nvidia.com/nvidia/v1/chat/completions"
    ],
    index=1
)

if not nvidia_api_key:
    st.info("Please add your Nvidia API key to continue.", icon="🗝️")
else:
    # Create a session state variable to store the chat messages.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Debug information panel
    if debug_mode:
        with st.expander("Debug Information"):
            st.write(f"API Endpoint: {api_endpoint}")
            st.write(f"Model Name: {model_name}")
            st.write(f"API Key (first 10 chars): {nvidia_api_key[:10]}..." if nvidia_api_key else "No API key")
            st.write(f"Number of Messages: {len(st.session_state.messages)}")
    
    # Create a chat input field
    if prompt := st.chat_input("What would you like to know?"):
        # Store and display the current prompt
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Prepare API request to Nvidia
        headers = {
            "Authorization": f"Bearer {nvidia_api_key}",
            "Content-Type": "application/json"
        }
        
        # Define API payload
        payload = {
            "model": model_name,
            "messages": [
                {"role": m["role"], "content": m["content"]} 
                for m in st.session_state.messages
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True
        }
        
        # Generate a response using the Nvidia API
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                with st.spinner("Generating response..."):
                    # Make the API request
                    if debug_mode:
                        st.write("Request Payload:")
                        st.json(payload)
                        st.write("Request Headers:")
                        safe_headers = headers.copy()
                        safe_headers["Authorization"] = safe_headers["Authorization"][:15] + "..."
                        st.json(safe_headers)
                    
                    response = requests.post(
                        api_endpoint,
                        headers=headers,
                        json=payload,
                        stream=True,
                        timeout=60
                    )
                    
                    # Check for HTTP errors
                    if response.status_code != 200:
                        error_message = f"Error {response.status_code}: {response.text}"
                        st.error(error_message)
                        
                        if debug_mode:
                            st.write("Full response:")
                            st.code(response.text)
                            st.write("Response headers:")
                            st.json(dict(response.headers))
                            
                        # Suggest troubleshooting steps
                        st.warning("""
                        Troubleshooting suggestions:
                        1. Verify your API key is valid
                        2. Try a different API endpoint from the sidebar
                        3. Check if the model name is correct
                        4. Make sure you have access to the Nvidia API
                        """)
                    
                    # Process streaming response if successful
                    else:
                        for line in response.iter_lines():
                            if not line:
                                continue
                                
                            line_text = line.decode('utf-8')
                            
                            # Debug raw response
                            if debug_mode:
                                st.code(line_text, language="json")
                                
                            # Handle SSE format
                            if line_text == "data: [DONE]":
                                break
                                
                            if line_text.startswith("data: "):
                                try:
                                    json_str = line_text[6:]  # Remove "data: " prefix
                                    chunk = json.loads(json_str)
                                    
                                    if "choices" in chunk and chunk["choices"]:
                                        if "delta" in chunk["choices"][0]:
                                            content = chunk["choices"][0]["delta"].get("content", "")
                                            if content:
                                                full_response += content
                                                message_placeholder.markdown(full_response)
                                except json.JSONDecodeError as e:
                                    st.error(f"Error parsing response: {e}")
                                    if debug_mode:
                                        st.code(line_text)
                                    break
            
            except Exception as e:
                st.error(f"Request failed: {str(e)}")
                if debug_mode:
                    st.exception(e)
            
            # Save the assistant's response
            if full_response:
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.error("No response received. Check the API configuration in the sidebar and try a different endpoint.")
    
    # Add a clear conversation button
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()
