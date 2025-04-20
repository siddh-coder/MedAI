import streamlit as st
from utils.chatbot import stream_chatbot_response
from utils.user_history import add_history_entry

def show():
    st.title("MedAI Chatbot")
    st.markdown("Chat with our AI assistant for medical queries, health advice, or general questions.")
    
    api_key = st.secrets.get("HF_API_KEY", "")
    if not api_key:
        api_key = st.text_input("Enter HuggingFace API Key", type="password")
    
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    
    user = st.session_state.user
    user_id = user.get("id")
    
    user_input = st.text_area("Your message:", key="chat_input")
    if st.button("Send") and user_input.strip():
        st.session_state['chat_history'].append({"role": "user", "content": user_input})
        placeholder = st.empty()
        if api_key:
            response = stream_chatbot_response(st.session_state['chat_history'], api_key, placeholder)
            st.session_state['chat_history'].append({"role": "assistant", "content": response})
            # Save to user history
            add_history_entry(user_id, "chatbot", {
                "message": user_input,
                "response": response
            })
        else:
            st.info("Please provide your HuggingFace API Key above.")
    
    st.markdown("---")
    st.subheader("Chat History")
    for msg in st.session_state['chat_history']:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**AI:** {msg['content']}")
