import streamlit as st

# Gemini APIライブラリのインポートをトライ
try:
    import google.generativeai as genai
    from google.api_core.exceptions import ResourceExhausted
    gemini_available = True
except ImportError:
    gemini_available = False

st.title("💬 Chatbot (Gemini API)")

if not gemini_available:
    st.error(
        "Gemini API用ライブラリ（google-generativeai）がインストールされていません。\n"
        "下記コマンドでインストールしてください。\n\n"
        "`pip install google-generativeai`"
    )
else:
    gemini_api_key = st.text_input("Gemini API Key", type="password")
    if not gemini_api_key:
        st.info("Gemini APIキーを入力してください。", icon="🗝️")
    else:
        # Gemini APIキーを設定
        genai.configure(api_key=gemini_api_key)

        # 利用可能なモデル一覧を取得して、最初のものを使う（推奨）
        available_models = [m.name for m in genai.list_models() if "generateContent" in m.supported_generation_methods]
        if available_models:
            selected_model = available_models[0]
        else:
            selected_model = "gemini-pro" # フォールバック

        model = genai.GenerativeModel(selected_model)

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
