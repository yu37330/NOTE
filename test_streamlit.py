import yfinance as yf
import streamlit as st
import pandas as pd
import time

# ページ設定
st.set_page_config(layout='wide')

# データ取得関数にキャッシュを追加
@st.cache_data
def load_data(ticker):
    try:
        data = yf.download(ticker, period='7d', interval='5m', progress=False)
        return data
    except Exception as e:
        st.error(f"データの取得中にエラーが発生しました: {e}")
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
