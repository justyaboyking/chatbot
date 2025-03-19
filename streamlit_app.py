#!/usr/bin/env python3
"""
Verbose NVIDIA API Debug Script

This script first pings the NVIDIA base URL to ensure connectivity, then sends a chat
completion request using your NVIDIA API key. It prints payload, headers, HTTP status,
and full JSON response details.

If nothing is printed or if errors occur, please verify:
  • Your NVIDIA API key is active and your account is configured for API access.
  • The MODEL_NAME is valid and available to your account.
  • Your network/firewall allows outbound HTTPS requests to integrate.api.nvidia.com.
"""

import requests
import json
import sys

def ping_server(url):
    print("Pinging server:", url)
    try:
        r = requests.get(url, timeout=10)
        print("Ping status code:", r.status_code)
        return True
    except Exception as e:
        print("Error pinging server:", e)
        return False

def main():
    print("Starting NVIDIA API debug script...\n")
    
    # Configuration: Replace with your valid values
    API_KEY = "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"
    ENDPOINT = "https://integrate.api.nvidia.com/v1/chat/completions"
    MODEL_NAME = "meta/llama-3.1-70b-instruct"  # Ensure you have access to this model

    # Check network connectivity
    base_url = "https://integrate.api.nvidia.com/"
    if not ping_server(base_url):
        print("\nCannot reach NVIDIA API server. Check your network/firewall settings.")
        sys.exit(1)

    # Build the payload (Note: max_tokens is required)
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, how are you?"}
        ],
        "max_tokens": 50,
        "temperature": 0.7,
        "stream": False  # Set to False for a complete JSON response
    }

    # Prepare headers with the API key
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    print("\nPayload to be sent:")
    print(json.dumps(payload, indent=2))
    
    print("\nHTTP Headers:")
    print(headers)

    print("\nSending request to endpoint:")
    print(ENDPOINT)
    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload, timeout=30)
        print("\nHTTP status code:", response.status_code)
    except Exception as e:
        print("\nRequest failed with exception:", e)
        sys.exit(1)

    # If we did not get a 200 status, print error details
    if response.status_code != 200:
        print("\nError response from server:")
        print(response.text)
        sys.exit(1)

    # Try to parse the JSON response
    try:
        data = response.json()
    except Exception as e:
        print("\nFailed to parse JSON response:", e)
        print("Response text:", response.text)
        sys.exit(1)

    print("\nFull JSON response received:")
    print(json.dumps(data, indent=2))

    # Optionally, extract and print the assistant's reply
    choices = data.get("choices", [])
    if choices:
        assistant_reply = choices[0].get("message", {}).get("content", "")
        print("\nAssistant's reply:")
        print(assistant_reply)
    else:
        print("\nNo 'choices' field found in the response.")

if __name__ == "__main__":
    main()
