import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Finance Assistant")

st.title("💬 AI Personal Finance Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_id = st.sidebar.number_input("User ID", min_value=1)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask about spending, purchases, budget...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)
res = requests.post(
    f"{API_URL}/chat/",
    json={
        "user_id": int(user_id),
        "message": prompt,
    },
)

if res.status_code != 200:
    st.error(f"Backend error: {res.text}")
else:
    data = res.json()

    if "reply" not in data:
        st.error(f"Unexpected response: {data}")
    else:
        reply = data["reply"]

        st.session_state.messages.append(
            {"role": "assistant", "content": reply}
        )

        with st.chat_message("assistant"):
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})

   
