#!/usr/bin/env python3
"""
Test NVIDIA Chat Completions API

This script sends a simple chat message payload to the NVIDIA API using the official integration endpoint.
It prints out debugging information including the payload, headers, HTTP status, and full JSON response.

Ensure that:
  - You have the 'requests' package installed: pip install requests
  - Your NVIDIA API key is valid and your account has access to the specified model.
  - You are using the correct endpoint and parameters per NVIDIA documentation.
"""

import requests
import json
import sys

def main():
    print("Starting NVIDIA API test script...")

    # Configuration: Replace with your actual API key, endpoint, and model name
    API_KEY = "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"
    # Use the official integration endpoint as per NVIDIA docs
    ENDPOINT = "https://integrate.api.nvidia.com/v1/chat/completions"
    MODEL_NAME = "meta/llama-3.1-70b-instruct"  # Adjust to a model your account can access

    # Build the payload with required parameters.
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, how are you?"}
        ],
        "max_tokens": 50,    # NVIDIA requires max_tokens explicitly set
        "temperature": 0.7,
        "stream": False      # For this test, disable streaming to get a complete JSON response
    }

    # Setup HTTP headers with the API key.
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    # Debug: Print the payload and headers
    print("\nPayload to be sent:")
    print(json.dumps(payload, indent=2))
    print("\nHeaders:")
    print(headers)

    try:
        print("\nSending request to:", ENDPOINT)
        response = requests.post(ENDPOINT, headers=headers, json=payload, timeout=30)
        print("HTTP status code:", response.status_code)
    except Exception as e:
        print("Error while sending request:", str(e))
        sys.exit(1)

    # If status is not 200, print error details
    if response.status_code != 200:
        print("Error from server:")
        print(response.text)
        sys.exit(1)

    # Attempt to parse the JSON response
    try:
        data = response.json()
    except json.JSONDecodeError as e:
        print("Failed to parse JSON response:", e)
        print("Response text:", response.text)
        sys.exit(1)

    # Debug: Print the full JSON response
    print("\nFull JSON response:")
    print(json.dumps(data, indent=2))

    # Extract and print the assistant's reply if available
    choices = data.get("choices", [])
    if choices:
        assistant_reply = choices[0].get("message", {}).get("content", "")
        print("\nAssistant's reply:")
        print(assistant_reply)
    else:
        print("No 'choices' found in response.")

if __name__ == "__main__":
    main()
