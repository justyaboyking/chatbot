#!/usr/bin/env python3
"""
Alternative NVIDIA API Test Script

This script iterates over several known NVIDIA Chat Completions API endpoints.
It sends a basic payload and prints the HTTP status and response for each endpoint.
Use this to determine which endpoint, if any, is working with your new API key.

Requirements:
  - Python 3.7+
  - requests (install via: pip install requests)
  
Before running, ensure:
  • Your NVIDIA account has access to the model you specify.
  • The API key is valid and activated.
  • You are not blocked by network/firewall restrictions.
  
If none of the endpoints returns a successful response, it may be an account
or configuration issue that requires contacting NVIDIA developer support.
"""

import requests
import json
import sys

def test_endpoint(endpoint, headers, payload):
    try:
        print(f"\nTrying endpoint: {endpoint}")
        response = requests.post(endpoint, headers=headers, json=payload, timeout=30)
        print("HTTP status code:", response.status_code)
        if response.status_code == 200:
            return response
        else:
            print("Error details:", response.text)
    except Exception as e:
        print("Exception occurred:", str(e))
    return None

def main():
    # Replace with your actual API key and desired model name
    API_KEY = "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"
    MODEL_NAME = "meta/llama-3.1-70b-instruct"  # Ensure you have access to this model

    # List of known endpoints to try
    endpoints = [
        "https://integrate.api.nvidia.com/v1/chat/completions",
        "https://api.nvidia.com/v1/chat/completions",
        "https://build.nvidia.com/v1/chat/completions",
        "https://build.nvidia.com/api/v1/chat/completions",
        "https://build.nvidia.com/nvidia/v1/chat/completions"
    ]

    # Build the payload (NVIDIA requires max_tokens to be explicitly set)
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, how are you?"}
        ],
        "max_tokens": 50,
        "temperature": 0.7,
        "stream": False  # For testing, we disable streaming
    }

    # HTTP headers including the API key
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    # Print the payload and headers for debugging purposes
    print("Payload to be sent:")
    print(json.dumps(payload, indent=2))
    print("\nHeaders:")
    print(headers)

    successful = False
    # Try each endpoint until one responds successfully
    for endpoint in endpoints:
        response = test_endpoint(endpoint, headers, payload)
        if response:
            try:
                data = response.json()
                print("\nSuccessful response from endpoint:")
                print(endpoint)
                print("\nFull JSON response:")
                print(json.dumps(data, indent=2))
                successful = True
                break  # Exit after the first successful response
            except json.JSONDecodeError as e:
                print("Failed to parse JSON from response:", e)
    
    if not successful:
        print("\nAll endpoints were tried and no successful response was received.")
        print("Troubleshooting suggestions:")
        print(" - Verify your API key is valid and activated.")
        print(" - Check that your NVIDIA account has access to the model:", MODEL_NAME)
        print(" - Confirm you are using the correct endpoint (consult NVIDIA documentation).")
        print(" - Verify that network/firewall settings allow outgoing requests to NVIDIA's servers.")
        print("If problems persist, please contact NVIDIA developer support.")

if __name__ == "__main__":
    main()
