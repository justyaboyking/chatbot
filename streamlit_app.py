import streamlit as st
import requests
import json
import time

# Title and description
st.title("💬 Multi-Provider AI Chatbot")
st.write("A versatile chatbot that supports multiple AI providers including NVIDIA, Together AI, Baseten, and Fireworks AI.")

# Sidebar: API configuration
st.sidebar.header("API Configuration")
provider = st.sidebar.selectbox(
    "Select AI Provider",
    options=["NVIDIA", "Together AI", "Baseten", "Fireworks AI"],
    index=0
)

if provider == "NVIDIA":
    api_key = st.sidebar.text_input(
        "NVIDIA API Key",
        type="password",
        value="your-api-key-here"
    )
    model_name = st.sidebar.text_input(
        "Model Name",
        value="NVIDIABuild-Autogen-30"
    )
    # Use the official integration endpoint as default.
    api_endpoint = st.sidebar.selectbox(
        "API Endpoint",
        options=[
            "https://integrate.api.nvidia.com/v1/chat/completions",
            "https://api.nvidia.com/v1/chat/completions",
            "https://build.nvidia.com/v1/chat/completions",
            "https://build.nvidia.com/api/v1/chat/completions",
            "https://build.nvidia.com/nvidia/v1/chat/completions"
        ],
        index=0
    )
elif provider == "Together AI":
    api_key = st.sidebar.text_input(
        "Together AI API Key",
        type="password"
    )
    model_name = st.sidebar.selectbox(
        "Model Name",
        options=[
            "llama-3-70b-instruct",
            "llama-3-8b-instruct",
            "mistral-large",
            "togethercomputer/llama-3.1-8b-instruct"
        ],
        index=0
    )
    api_endpoint = "https://api.together.xyz/v1/chat/completions"
elif provider == "Baseten":
    api_key = st.sidebar.text_input(
        "Baseten API Key",
        type="password"
    )
    model_id = st.sidebar.text_input("Model ID")
    api_endpoint = f"https://app.baseten.co/models/{model_id}/predict"
elif provider == "Fireworks AI":
    api_key = st.sidebar.text_input(
        "Fireworks AI API Key",
        type="password"
    )
    model_name = st.sidebar.selectbox(
        "Model Name",
        options=[
            "accounts/fireworks/models/llama-v3-70b-instruct",
            "accounts/fireworks/models/mixtral-8x7b-instruct",
            "accounts/fireworks/models/llama-v3-8b-instruct"
        ],
        index=0
    )
    api_endpoint = "https://api.fireworks.ai/inference/v1/chat/completions"

temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
max_tokens = st.sidebar.slider("Max Tokens", min_value=100, max_value=2000, value=800, step=100)
debug_mode = st.sidebar.checkbox("Debug Mode")

# If no API key, show info message
if not api_key:
    st.info(f"Please add your {provider} API key to continue.", icon="🗝️")
else:
    # Initialize session state for messages
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display conversation messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Debug information if enabled
    if debug_mode:
        with st.expander("Debug Information"):
            st.write(f"Provider: {provider}")
            st.write(f"API Endpoint: {api_endpoint}")
            if provider != "Baseten":
                st.write(f"Model Name: {model_name}")
            else:
                st.write(f"Model ID: {model_id}")
            st.write(f"API Key (first 10 chars): {api_key[:10]}...")
            st.write(f"Number of Messages: {len(st.session_state.messages)}")
    
    # Chat input field
    if prompt := st.chat_input("What would you like to know?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Prepare API request
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            try:
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}"
                }
                # Build the payload (ensure required parameters are included)
                payload = {
                    "model": model_name,
                    "messages": [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": True
                }
                
                if debug_mode:
                    st.write("Request Payload:")
                    st.json(payload)
                    st.write("Request Headers:")
                    safe_headers = headers.copy()
                    safe_headers["Authorization"] = safe_headers["Authorization"][:15] + "..."
                    st.json(safe_headers)
                
                # Make the API request
                response = requests.post(api_endpoint, headers=headers, json=payload, stream=True, timeout=60)
                
                # Check for errors in HTTP response
                if response.status_code != 200:
                    error_message = f"Error {response.status_code}: {response.text}"
                    st.error(error_message)
                    if debug_mode:
                        st.write("Full response:")
                        st.code(response.text)
                        st.write("Response headers:")
                        st.json(dict(response.headers))
                    st.warning(
                        f"Troubleshooting suggestions for {provider}:\n"
                        f"1. Verify your API key is valid\n"
                        f"2. Check if the model name/ID is correct\n"
                        f"3. Make sure you have access to the specified model\n"
                        f"4. Try a different API endpoint (if applicable)"
                    )
                else:
                    # Process streaming response
                    for line in response.iter_lines():
                        if not line:
                            continue
                        line_text = line.decode("utf-8").strip()
                        if debug_mode:
                            st.code(line_text, language="json")
                        if line_text == "data: [DONE]":
                            break
                        if line_text.startswith("data: "):
                            try:
                                json_str = line_text[6:]  # Remove "data: " prefix
                                chunk = json.loads(json_str)
                                if "choices" in chunk and chunk["choices"]:
                                    delta = chunk["choices"][0].get("delta", {})
                                    content = delta.get("content", "")
                                    if content:
                                        full_response += content
                                        message_placeholder.markdown(full_response)
                            except json.JSONDecodeError as e:
                                st.error(f"Error parsing response: {e}")
                                if debug_mode:
                                    st.code(line_text)
                                break
                    message_placeholder.markdown(full_response)
            except Exception as e:
                st.error(f"Request failed: {str(e)}")
                if debug_mode:
                    st.exception(e)
            
            # Save assistant's response if available
            if full_response:
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.error(f"No response received from {provider}. Check the API configuration in the sidebar.")
    
    # Clear conversation button
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.experimental_rerun()
