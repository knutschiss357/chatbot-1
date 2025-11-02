import streamlit as st
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

# タイトルと説明
st.title("💬 Chatbot (Gemini API)")
st.write(
    "このチャットボットはGoogle Gemini APIを使って応答を生成します。"
    "利用にはGemini APIキーが必要です。APIキーは [Google AI Studio](https://aistudio.google.com/app/apikey) で取得できます。"
)

# ユーザーのGemini APIキー入力
gemini_api_key = st.text_input("Gemini API Key", type="password")
if not gemini_api_key:
    st.info("Gemini APIキーを入力してください。", icon="🗝️")
else:
    # Geminiクライアント設定
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-pro')

    # セッション状態でメッセージ保存
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 既存のチャット履歴表示
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 入力フォーム
    if prompt := st.chat_input("What's up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            # Gemini APIへリクエスト
            history = [
                {"role": m["role"], "parts": [m["content"]]}
                for m in st.session_state.messages
            ]
            response = model.generate_content(history)
            content = response.text

            with st.chat_message("assistant"):
                st.markdown(content)
            st.session_state.messages.append({"role": "assistant", "content": content})

        except ResourceExhausted:
            st.error("Gemini APIのレートリミットに達しました。時間を空けて再度お試しください。")
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
