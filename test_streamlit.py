import pandas as pd
import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

# The code below writes the header for the web application 
st.write("""
# Stock Price Web Application

Shown are the stock closing **price** and ***volume*** of Amazon!

**Period**: May 2012 - May 2022
""")

# https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75

ticker_symbol = 'AMZN'

# Get ticker data by creating a ticker object
ticker_data = yf.Ticker(ticker_symbol)

# Get Amazon historical stock data for a specified time period as a dataframe
tickerDF = ticker_data.history(period="1mo", interval="5m")

# Columns: Open, High, Low Close, Volume, Dividends and Stock Splits
st.write("## Stock Closing Price in USD")
st.line_chart(tickerDF.Close)

st.write("## Stock Volume in USD")
st.line_chart(tickerDF.Volume)

# ゴトー日を判定する関数
def is_gotoubi(date):
    day = date.day
    return day % 5 == 0 and day != 0

# 合成チャートを作成する関数
def create_composite_chart(df):
    df['is_gotoubi'] = df.index.to_series().apply(lambda x: is_gotoubi(x))
    gotoubi_df = df[df['is_gotoubi']].copy()

    # 0時基準にデータを調整する
    gotoubi_df.index = pd.to_datetime(gotoubi_df.index)
    gotoubi_df['time_from_midnight'] = gotoubi_df.index.hour * 3600 + gotoubi_df.index.minute * 60 + gotoubi_df.index.second
    gotoubi_df['date'] = gotoubi_df.index.date

    # 0:00の価格を基準に差分を計算
    base_prices = gotoubi_df[gotoubi_df['time_from_midnight'] == 0].set_index('date')['Close']
    gotoubi_df = gotoubi_df.join(base_prices, on='date', rsuffix='_base')
    gotoubi_df['price_diff'] = gotoubi_df['Close'] - gotoubi_df['Close_base']

    # ピボットテーブルを作成
    pivot_df = gotoubi_df.pivot(index='time_from_midnight', columns='date', values='price_diff')

    # 各時点での中央値を計算
    median_series = pivot_df.median(axis=1)

    # チャートを描画
    plt.figure(figsize=(12, 6))
    plt.plot(median_series.index, median_series.values, label='Median Price Difference from 0:00')
    plt.title('Composite Chart for Gotoubi Days (5-Minute Interval)')
    plt.xlabel('Time from Midnight (seconds)')
    plt.ylabel('Median Price Difference')
    plt.axhline(y=0, color="#565656", alpha=0.3)
    plt.grid(True)

    # X軸の表示を時間形式に変更し、0:00から12:00まで表示
    hours = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    plt.xticks([h * 3600 for h in hours], [f'{h}:00' for h in hours])
    plt.xlim([0, 12 * 3600])

    # Y軸の表示範囲を設定
    plt.ylim([-0.1, 0.2])

    # 9:55に縦線を追加
    plt.axvline(x=9*3600 + 55*60, color='red', linestyle='--', label='9:55')

    # 3:30から9:55に斜め矢印を追加
    plt.annotate('', xy=(9*3600 + 55*60, 0.15), xytext=(3.5*3600, -0.05),
                 arrowprops=dict(facecolor='red', shrink=0.05, width=5, headwidth=15))

    plt.legend()
    st.pyplot(plt)

# ゴトー日の変動グラフを追加
st.write("## Gotoubi Days Price Variation")
create_composite_chart(tickerDF)
