import yfinance as yf
import streamlit as st
import pandas as pd

# Streamlitアプリケーションのタイトル
st.title('Stock Price Analysis')

# ユーザーから入力を受け取るテキストボックス
ticker = st.text_input('Enter Stock Ticker', 'AAPL')

# データ取得関数
def load_data(ticker):
    data = yf.download(ticker, period='1d', interval='1m')
    return data

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
    st.set_page_config(layout='wide')
    st.write('Stock Price Analysis App')
