import streamlit as st
from openai import OpenAI
import os

st.write("DB username:", st.secrets["db_username"])
st.write(
    "Has environment variables been set:",
    os.environ["db_username"] == st.secrets["db_username"],
)

st.title("AC4RM-Project - Anti GPT-Abuse Chatbot")
st.write(
    "This is a simple chatbot that provents you from gpt-abuse "
    
)

openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    client = OpenAI(api_key=openai_api_key)


    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):  

        restricted_words = ["homework", "test", "exam", "help me", "complete", 
                            "answer", "assignment", "quiz", "solve", "cheat"]

        if any(word in prompt.lower() for word in restricted_words):
            response = ("Sorry, I cannot directly help you complete homework or tests, "
                        "but I can provide some guidance on your thought process. "
                        "You should do it on your own, don't over-rely on AI.")
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )


            with st.chat_message("assistant"):
                response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
