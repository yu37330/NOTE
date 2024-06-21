import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import streamlit as st

# 過去60日間の5分足データを取得する関数
def get_past_sixty_days_data(ticker):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=60)
    try:
        data = yf.download(ticker, start=start_date, end=end_date, interval='5m')
        data.reset_index(inplace=True)
    except Exception as e:
        st.error(f"データの取得中にエラーが発生しました: {e}")
        return None
    
    # データのヘッダーと最初の数行を表示して確認
    st.write("データのヘッダー:", data.head())
    st.write("データのカラム名:", data.columns)
    
    # 'Datetime'列の存在を確認
    if 'Datetime' not in data.columns:
        st.error("'Datetime'列がデータに存在しません")
        return None
    
    data['Datetime'] = pd.to_datetime(data['Datetime']) + timedelta(hours=9)  # JSTに変換
    return data

# ゴトー日を判定する関数
def is_gotoubi(date):
    day = date.day
    return day % 5 == 0 and day != 0

# 合成チャートを作成する関数
def create_composite_chart(df):
    df['is_gotoubi'] = df['Datetime'].apply(lambda x: is_gotoubi(x))
    gotoubi_df = df[df['is_gotoubi']].copy()

    # 0時基準にデータを調整する
    gotoubi_df.loc[:, 'time_from_midnight'] = gotoubi_df['Datetime'].dt.hour * 3600 + gotoubi_df['Datetime'].dt.minute * 60 + gotoubi_df['Datetime'].dt.second
    gotoubi_df.loc[:, 'date'] = gotoubi_df['Datetime'].dt.date

    # 0:00の価格を基準に差分を計算
    base_prices = gotoubi_df[gotoubi_df['time_from_midnight'] == 0].set_index('date')['Close']
    gotoubi_df = gotoubi_df.join(base_prices, on='date', rsuffix='_base')
    gotoubi_df.loc[:, 'price_diff'] = gotoubi_df['Close'] - gotoubi_df['Close_base']

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
    return plt

# Streamlitアプリケーション
def main():
    st.title("Composite Chart for Gotoubi Days (5-Minute Interval)")

    ticker = 'USDJPY=X'  # USD/JPYのティッカーシンボル

    # データ取得とエラーハンドリング
    df = get_past_sixty_days_data(ticker)
    if df is not None:
        st.write("Past Sixty Days Data", df)
        st.write("Composite Chart")
        plt = create_composite_chart(df)
        st.pyplot(plt)
    else:
        st.error("データの取得に失敗しました。")

if __name__ == "__main__":
    main()
