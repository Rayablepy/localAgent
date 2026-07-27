import asyncio
import os
from config import ACTUAL_FILE_PATH
import streamlit as st
from loader import save_data, delete_data, list_data
from main import getresponse

DIR = ACTUAL_FILE_PATH
os.makedirs(DIR, exist_ok=True)

with st.sidebar:
    st.header("Upload Data")
    uploaded_files = st.file_uploader(
        "Upload files to sample_data",
        type=["pdf", "csv", "txt", "docx", "xlsx"],
        accept_multiple_files=True,
    )
    if uploaded_files:
        for f in uploaded_files:
            dest = os.path.join(DIR, f.name)
            with open(dest, "wb") as out:
                out.write(f.getbuffer())
                save_data(f.name)
        st.success(f"Saved {len(uploaded_files)} file(s) to {DIR}")
        st.rerun()

st.sidebar.divider()
st.sidebar.header("Saved Files")
files = list_data()
if files:
    for file in files:
        cols = st.sidebar.columns([3, 1])
        cols[0].write(file)
        if cols[1].button("Delete", key=f"del_{file}"):
            delete_data(file)
            st.rerun()
else:
    st.sidebar.write("No files saved yet.")

if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
if prompt := st.chat_input("Your input here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = asyncio.run(getresponse(prompt))
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
