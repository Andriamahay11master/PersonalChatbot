# client/app.py
import streamlit as st
import requests

st.set_page_config(page_title="RAG Chatbot", layout="wide")
st.title("Retrieval-Augmented QA Chatbot")

API_BASE = "http://localhost:8000/api"

# -------------------------------
# File upload section
# -------------------------------
uploaded_files = st.file_uploader(
    "Upload documents (PDF, TXT, MD)",
    type=["pdf", "txt", "md"],
    accept_multiple_files=True
)

if uploaded_files:
    st.info(f"{len(uploaded_files)} file(s) ready to upload")

    if st.button("Upload Files"):
        files_payload = [
            ("files", (f.name, f, "application/octet-stream")) for f in uploaded_files
        ]
        try:
            resp = requests.post(f"{API_BASE}/upload", files=files_payload)
            resp.raise_for_status()
            data = resp.json()
            st.success(data.get("message", "Files uploaded successfully"))
            st.write("Uploaded files:", data.get("file_ids", []))
        except requests.exceptions.RequestException as e:
            st.error(f"Upload failed: {e}")

# -------------------------------
# Chat section
# -------------------------------
user_input = st.text_input("Your question:")

if st.button("Ask") and user_input.strip():
    payload = {"prompt": user_input}

    try:
        resp = requests.post(f"{API_BASE}/chat", json=payload)
        resp.raise_for_status()
        data = resp.json()

        answer = data.get("answer", "No answer")
        sources = data.get("sources", [])

        st.subheader("Answer")
        st.write(answer)

        if sources:
            st.subheader("Sources")
            for src in sources:
                st.write(f"- {src}")

    except requests.exceptions.RequestException as e:
        st.error(f"Chat request failed: {e}")
