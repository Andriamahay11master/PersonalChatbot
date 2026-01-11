#Use UI
import streamlit as st
import requests

st.title("Retrieval-Augmented QA Chatbot")

uploaded = st.file_uploader("Upload documents", accept_multiple_files=True)
if uploaded:
    files = {f.name: f for f in uploaded}
    # Send to backend /upload endpoint (multipart)
    # Use requests.post with files parameter

user_input = st.text_input("Your question:")
if st.button("Ask"):
    # Send to backend /api/chat
    resp = requests.post("http://localhost:8000/api/chat", json={"prompt": user_input})
    st.write(resp.json().get("answer", "No answer"))
    sources = resp.json().get("sources", [])
    if sources:
        st.write("Sources:")
        for src in sources:
            st.write(f"- {src}")
    