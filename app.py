"""
app.py

このスクリプトは、ユーザーが入力したテキストを、指定された言語に翻訳する機能を提供します。
ユーザーはテキストを入力し、Google Cloud Translation APIを通じて翻訳された結果を取得します。

主な機能:
- Streamlitを使用したインタラクティブなテキスト入力インターフェースの提供。
- 入力されたテキストをGoogle Cloud Translation APIに送信し、翻訳を取得。
- 翻訳結果をStreamlitアプリケーション上で表示。
- APIリクエストとレスポンスデータをサイドバーに表示し、APIの通信内容を表示。

使用方法:
Streamlitアプリケーションとしてこのスクリプトを実行し、
ブラウザ上でテキストを入力し、翻訳結果を取得します。
    streamlit run app.py
"""

import os
import requests
import streamlit as st

# APIのエンドポイントの定義
TRANSLATION_API_ENDPOINT = "https://translation.googleapis.com/language/translate/v2"

# 環境変数からAPIキーを取得
api_key = os.environ.get("TRANSLATION_API_KEY")


def translate_text(text, target_language):
    """
    Google Translate APIを使用して指定された言語にテキストを翻訳する関数
    """
    # APIキーが設定されていない場合はリクエストを送信せずにリターン
    if not api_key:
        return "APIキーが設定されていません。"

    # APIリクエストパラメータを設定
    request_data = {
        "q": text,
        "target": target_language,
        "format": "text",
        "key": api_key,
    }

    # Google Translate APIへリクエストを送信し、レスポンスを取得
    response = requests.post(TRANSLATION_API_ENDPOINT, data=request_data)

    # レスポンスをJSON形式で解析
    response_data = response.json()

    # 翻訳結果のテキストを取得
    translated_text = response_data["data"]["translations"][0]["translatedText"]

    # APIの通信内容をサイドバーに表示（オプション）
    display_http_communication_details(request_data, response)

    # 結果をリターン
    return translated_text


def display_http_communication_details(request_data, response):
    """
    HTTPリクエストとレスポンスの詳細をサイドバーに表示する関数（オプション）
    """
    request_data["key"] = "API_KEY"
    expander = st.sidebar.expander("Communication Detail")
    expander.subheader("HTTP Request Details")
    expander.text("Method: POST")
    expander.text("Endpoint: " + TRANSLATION_API_ENDPOINT)
    expander.text("Request Body: ")
    expander.json(request_data)

    expander.subheader("HTTP Response Details")
    expander.text("Status Code: " + str(response.status_code))
    expander.text("Response body: ")
    expander.json(response.json())


# メッセージ管理用のセッションステートの初期化
if "messages" not in st.session_state:
    st.session_state.messages = []

# アプリのタイトル
st.sidebar.title("Translation App")

# 言語選択オプション
target_language = st.sidebar.selectbox(
    label="Choose Target Language:", options=["en", "ja", "fr", "ko"]
)

# ユーザーからのテキスト入力受付
input_text = st.chat_input("Enter text to translate")

# テキストが入力された場合の処理
if input_text:
    # 翻訳関数の呼び出し
    translated_text = translate_text(input_text, target_language)

    # メッセージの保存
    st.session_state.messages.append({"role": "user", "content": input_text})
    st.session_state.messages.append({"role": "assistant", "content": translated_text})

# チャットウィンドウにメッセージを表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
