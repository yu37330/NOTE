import pandas as pd
import streamlit as st
import yfinance as yf

# The code below writes the header for the web application 
st.write("""
# Forex Rate Web Application

Shown are the USD/JPY closing **price** and ***volume***!

**Period**: May 2012 - May 2022
""")

ticker_symbol = 'USDJPY=X'  # USD/JPYのティッカーシンボル

# Get ticker data by creating a ticker object
ticker_data = yf.Ticker(ticker_symbol)

# Get USD/JPY historical stock data for a specified time period as a dataframe
tickerDF = ticker_data.history(period="1mo",
                               interval="1d", start='2012-5-31', end='2022-5-31')

# Columns: Open, High, Low Close, Volume, Dividends and Stock Splits
st.write("""
         ## Forex Closing Price in JPY
         """)
st.line_chart(tickerDF.Close)

st.write("""
         ## Forex Volume in USD
         """)
st.line_chart(tickerDF.Volume)
