#File temporarily not in use, ignore for now
'''
import streamlit as st
import datetime
from db import message_table

messages = message_table.get_all()

for message in messages:
    with st.chat_message(message["origin"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Your message here..."):
    message_table.insert(prompt,"user",datetime.datetime.now())
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        response = st.write_stream(model_response(prompt))
    message_table.insert(prompt, "assistant", datetime.datetime.now())
'''