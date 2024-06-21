import yfinance as yf
import streamlit as st
import pandas as pd
import time

# ページ設定
st.set_page_config(layout='wide')

# データ取得関数に再試行ロジックを追加
def load_data(ticker, retries=3, delay=5):
    for attempt in range(retries):
        try:
            data = yf.download(ticker, period='1d', interval='15m', progress=False)
            return data
        except Exception as e:
            st.error(f"データの取得中にエラーが発生しました: {e}")
            if attempt < retries - 1:
                st.info(f"{delay}秒後に再試行します...")
                time.sleep(delay)
            else:
                st.error("データの取得に失敗しました。")
                return None

# Streamlitアプリケーションのタイトル
st.title('Stock Price Analysis')

# ユーザーから入力を受け取るテキストボックス
ticker = st.text_input('Enter Stock Ticker', 'AAPL')

# ボタンがクリックされたときにデータを取得する
if st.button('Load Data'):
    data = load_data(ticker)
    if data is not None and not data.empty:
        st.write('Data Loaded Successfully')
        st.write(data.tail())  # 最新のデータを表示
        st.line_chart(data['Close'])  # 終値のチャートを表示
    else:
        st.error('Failed to load data')

# アプリケーションの実行
if __name__ == '__main__':
    st.write('Stock Price Analysis App')
