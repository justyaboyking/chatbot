import streamlit as st
import requests
import json

# Show title and description.
st.title("💬 Nvidia Llama 3.3 Nemotron Super 49B Chatbot")
st.write(
    "This is a simple chatbot that uses Nvidia's Llama 3.3 Nemotron Super 49B model to generate responses. "
    "The API key is pre-filled, but you can change it if needed."
)

# Ask user for their Nvidia API key via `st.text_input`.
nvidia_api_key = st.text_input("Nvidia API Key", 
                              type="password", 
                              value="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")

if not nvidia_api_key:
    st.info("Please add your Nvidia API key to continue.", icon="🗝️")
else:
    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message.
    if prompt := st.chat_input("What would you like to know?"):
        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Prepare API request to Nvidia
        headers = {
            "Authorization": f"Bearer {nvidia_api_key}",
            "Content-Type": "application/json"
        }
        
        # Define API URL and payload
        api_url = "https://build.nvidia.com/v1/chat/completions"
        payload = {
            "model": "llama-3.3-nemotron-super-49b-v1",
            "messages": [
                {"role": m["role"], "content": m["content"]} 
                for m in st.session_state.messages
            ],
            "stream": True,
            "temperature": 0.7,
            "max_tokens": 800
        }
        
        # Generate a response using the Nvidia API
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                with st.spinner("Generating response..."):
                    response = requests.post(
                        api_url,
                        headers=headers,
                        json=payload,
                        stream=True,
                        timeout=60
                    )
                    
                    # Check for HTTP errors
                    if response.status_code != 200:
                        error_message = f"Error {response.status_code}: {response.text}"
                        st.error(error_message)
                        
                        # Try alternative endpoint if first fails
                        if response.status_code in [401, 404]:
                            alt_url = "https://build.nvidia.com/api/v1/chat/completions"
                            st.info(f"Trying alternative endpoint...")
                            response = requests.post(
                                alt_url,
                                headers=headers,
                                json=payload,
                                stream=True,
                                timeout=60
                            )
                    
                    # Process streaming response if successful
                    if response.status_code == 200:
                        for line in response.iter_lines():
                            if not line:
                                continue
                                
                            line_text = line.decode('utf-8')
                            
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
                                    break
            
            except Exception as e:
                st.error(f"Request failed: {str(e)}")
            
            # Save the assistant's response
            if full_response:
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.error("No response received. Check the API configuration.")
