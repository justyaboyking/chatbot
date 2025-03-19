#!/usr/bin/env python3

import requests
import json

API_KEY = "nvapi-REPLACE_THIS_WITH_YOUR_KEY"
ENDPOINT = "https://integrate.api.nvidia.com/v1/chat/completions"
MODEL_NAME = "meta/llama-3.1-70b-instruct"  # or whichever model you have access to

def main():
    # Basic payload: system message + user message
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"}
        ],
        # NVIDIA often requires these parameters:
        "max_tokens": 50,
        "temperature": 0.7,
        "stream": False
    }

    # HTTP headers, including the Bearer token
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    print("Sending request to NVIDIA Chat Completions API...")
    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload, timeout=30)
    except Exception as e:
        print(f"Request failed: {e}")
        return

    # Check HTTP status code
    print(f"HTTP status code: {response.status_code}")

    if response.status_code != 200:
        print("Error details:", response.text)
        return

    # Parse JSON response
    try:
        data = response.json()
    except json.JSONDecodeError:
        print("Invalid JSON received from server:")
        print(response.text)
        return

    # Print the entire response
    print("Full JSON response:")
    print(json.dumps(data, indent=2))

    # If the response has choices, print the assistant’s reply
    choices = data.get("choices", [])
    if choices:
        # The content is typically in choices[0].message.content
        assistant_msg = choices[0].get("message", {}).get("content", "")
        print("\nAssistant's reply:")
        print(assistant_msg)
    else:
        print("No 'choices' found in the response.")

if __name__ == "__main__":
    main()
