import streamlit as st
import pandas as pd
from data_fetcher import get_stock_data
from indicators import add_indicators
from sentiment import analyze_sentiment

st.set_page_config(page_title="📈 Financial AI Agent", layout="wide")
st.title("📈 Financial AI Agent")

# Sidebar for user input
st.sidebar.header("Stock Input & Sentiment")
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g. AAPL, TSLA, MSFT):", "AAPL")
headline = st.sidebar.text_input("Enter News Headline:", "Apple launches new iPhone with strong sales")

# Run Analysis button
if st.sidebar.button("Run Analysis"):

    # Fetch and prepare stock data
    st.subheader(f"Fetching data for {ticker}...")
    df = get_stock_data(ticker)
    df = add_indicators(df)

    # Flatten MultiIndex columns if needed
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in df.columns]

    # Show latest stock data
    st.subheader("Latest Stock Data")
    st.dataframe(df.tail())

    # Plot Close + SMA + EMA
    st.subheader("Price Chart (Close + SMA + EMA)")
    st.line_chart(df[['Close', 'SMA_20', 'EMA_20']])

    # Plot RSI
    st.subheader("RSI (14-day)")
    st.line_chart(df['RSI_14'])

    # Plot MACD + Signal
    st.subheader("MACD")
    st.line_chart(df[['MACD', 'MACD_Signal']])

    # Sentiment Analysis
    st.subheader("Sentiment Analysis")
    if headline:
        result = analyze_sentiment(headline)
        label = result['label']
        score = result['score']
        st.write(f"**Sentiment:** {label}  |  **Confidence:** {score:.2f}")
