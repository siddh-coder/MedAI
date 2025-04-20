import streamlit as st
from utils.user_history import get_user_history

def show():
    st.title("Your Medical History")
    user = st.session_state.user
    user_id = user.get("id")
    if not user_id:
        st.error("User not found in session.")
        return
    history = get_user_history(user_id)
    if not history:
        st.info("No history found yet.")
        return
    # Sort by timestamp descending
    history = sorted(history, key=lambda x: x.get("timestamp", ""), reverse=True)
    for entry in history:
        st.markdown(f"**Type:** {entry.get('type', 'Unknown')}")
        st.markdown(f"**Time:** {entry.get('timestamp', '')}")
        if entry.get('type') == 'inference':
            st.markdown(f"**Symptoms:** {', '.join(entry.get('symptoms', []))}")
            st.markdown(f"**Result:** {entry.get('result', '')}")
            st.markdown(f"**Inference Type:** {entry.get('inference_type', '')}")
        elif entry.get('type') == 'report_analysis':
            st.markdown(f"**File Name:** {entry.get('file_name', '')}")
            st.markdown(f"**Specialization:** {entry.get('specialization', '')}")
            st.markdown(f"**Tests Recommended:** {entry.get('tests', '')}")
        elif entry.get('type') == 'doctor_visit':
            st.markdown(f"**Doctor:** {entry.get('doctor_name', '')}")
            st.markdown(f"**Specialization:** {entry.get('specialization', '')}")
        elif entry.get('type') == 'chatbot':
            st.markdown(f"**Message:** {entry.get('message', '')}")
            st.markdown(f"**AI Response:** {entry.get('response', '')}")
        st.markdown("---")
