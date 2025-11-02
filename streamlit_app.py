import streamlit as st
from openai import OpenAI, RateLimitError

# ...（省略）...

if prompt := st.chat_input("What is up?"):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # OpenAI APIへのリクエスト
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

    except RateLimitError:
        st.error("OpenAI APIの利用制限に達しました。時間をおいて再度お試しください。")
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
