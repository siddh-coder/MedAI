import json
import requests
import streamlit as st

API_URL = "https://router.huggingface.co/nebius/v1/chat/completions"

def query_chatbot(messages, api_key, model="aaditya/Llama3-OpenBioLLM-70B", max_tokens=512, stream=True):
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "messages": messages,
        "max_tokens": max_tokens,
        "model": model,
        "stream": stream,
    }
    response = requests.post(API_URL, headers=headers, json=payload, stream=True)
    for line in response.iter_lines():
        if not line.startswith(b"data:"):
            continue
        if line.strip() == b"data: [DONE]":
            return
        yield json.loads(line.decode("utf-8").lstrip("data:").rstrip("/n"))

def stream_chatbot_response(messages, api_key, placeholder, model="aaditya/Llama3-OpenBioLLM-70B"):
    text = ""
    for chunk in query_chatbot(messages, api_key, model=model):
        delta = chunk["choices"][0]["delta"].get("content", "")
        text += delta
        placeholder.markdown(text)
    return text
