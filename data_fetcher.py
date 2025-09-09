<<<<<<< HEAD
import yfinance as yf
import pandas as pd

def get_stock_data(ticker="AAPL", period="6mo", interval="1d"):
    data = yf.download(ticker, period=period, interval=interval)
    data.dropna(inplace=True)
    return data
=======
import yfinance as yf
import pandas as pd

def get_stock_data(ticker="AAPL", period="6mo", interval="1d"):
    data = yf.download(ticker, period=period, interval=interval)
    data.dropna(inplace=True)
    return data
>>>>>>> 647a1a0ecdbb67439beb8685a67f4906de223262
