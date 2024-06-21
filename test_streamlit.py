

import pandas as pd
import streamlit as st
import yfinance as yf


#The code below writes the header for the web application 
st.write("""
# Stock Price Web Application

 
Shown are the stock closing **price** and ***volume*** of Amazon!

**Period**: May 2012 - May 2022
         
""")

#https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75

ticker_symbol = 'AMZN'

#get ticker data by creating a ticker object

ticker_data = yf.Ticker(ticker_symbol)

#get amazon historical stock data for a specified time period as a dataframe

tickerDF = ticker_data.history(period="2mo",
                               interval="5m")

#columns: Open, High, Low Close, Volume, Dividends and Stock Splits

st.write("""
         ## Stock Closing Price in USD
         """    )
st.line_chart(tickerDF.Close)

st.write("""
         ## Stock Volume in USD
         """    )
st.line_chart(tickerDF.Volume)
