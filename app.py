import databutton as db
import streamlit as st
import os

st.subheader(" Create Instant ChatBot 🤖 using `embedchain`")
st.markdown(" Repo : [Embdedchain](https://github.com/embedchain/embedchain)")


OPENAI_API_KEY = db.secrets.get(name="OPENAI_API_KEY")
# OPENAI_API_KEY
OPENAI_API_KEY = st.text_input("Enter your OPEN AI API Key", type="password")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

import time
import openai
from embedchain import App


@st.cache_resource
def botadd(URL):
    databutton_bot = App()
    # Embed Online Resources
    databutton_bot.add("web_page", URL)
    return databutton_bot


if "btn_state" not in st.session_state:
    st.session_state.btn_state = False

prompt = st.text_input(
    "Enter a URL: ",
    placeholder="https://docs.databutton.com/howto/store-and-load-faiss-vectordb",
)
btn = st.button("Initialize Bot")

if btn or st.session_state.btn_state:
    st.session_state.btn_state = True
    databutton_bot = botadd(prompt)
    st.success("Bot Ready ☑️! ")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            assistant_response = databutton_bot.query(prompt)

        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        # Add assistant response to chat history
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )
else:
    st.info("Initiate a bot first!")
