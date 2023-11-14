import streamlit as st
import requests

stream = False

url = "https://chat.nbox.ai/api/chat/completions"
headers = {
    "Authorization": "tune-02693a33-aa9a-405d-aeac-4031089f8bb01699871916",
    "Content-Type": "application/json",
}

st.title("Spark GPT 🤖")
st.divider()
st.text("A chatbot made by Kush Kaushik & Ayush Singh")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        response = requests.post(
            url,
            headers=headers,
            json={
                "temperature": 0.8,
                "messages": [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                "model": "llama2-chat-13b-4k",
                "stream": stream,
                "max_tokens": 1000,
            },
        )

        response = response.json()
        full_response += response["choices"][0]["message"].get("content", "")
        message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
