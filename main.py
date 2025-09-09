import streamlit as st
import pandas as pd
from data_fetcher import get_stock_data
from indicators import add_indicators
from sentiment import analyze_sentiment

st.set_page_config(page_title="📈 Financial AI Agent", layout="wide")
st.title("📈 Financial AI Agent")

# Sidebar input
st.sidebar.header("Stock & Sentiment Input")
ticker = st.sidebar.text_input("Enter Stock Ticker:", "AAPL")
headline = st.sidebar.text_input("Enter News Headline:", "Apple launches new iPhone with strong sales")

# Run Analysis
if st.sidebar.button("Run Analysis"):

    # Fetch stock data and add indicators
    st.subheader(f"Fetching data for {ticker}...")
    df = get_stock_data(ticker)
    df = add_indicators(df)

    # Flatten MultiIndex columns
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in df.columns]

    # Dynamically detect columns
    close_col = next((col for col in df.columns if 'Close' in col), None)
    sma_col = next((col for col in df.columns if 'SMA' in col), None)
    ema_col = next((col for col in df.columns if 'EMA' in col), None)
    rsi_col = next((col for col in df.columns if 'RSI' in col), None)
    macd_col = next((col for col in df.columns if 'MACD' in col and 'Signal' not in col), None)
    macd_signal_col = next((col for col in df.columns if 'MACD_Signal' in col or 'Signal' in col), None)

    # Show latest stock data
    st.subheader("Latest Stock Data")
    st.dataframe(df.tail())

    # Plot Close + SMA + EMA
    price_cols = [col for col in [close_col, sma_col, ema_col] if col and col in df.columns]
    if price_cols:
        st.subheader("Price Chart (Close + SMA + EMA)")
        st.line_chart(df[price_cols])
    else:
        st.warning("No price columns available for plotting.")

    # Plot RSI
    if rsi_col and rsi_col in df.columns:
        st.subheader("RSI (14-day)")
        st.line_chart(df[rsi_col])
    else:
        st.info("RSI column not available.")

    # Plot MACD + Signal
    macd_cols = [col for col in [macd_col, macd_signal_col] if col and col in df.columns]  # FIXED
    if macd_cols:
        st.subheader("MACD")
        st.line_chart(df[macd_cols])
    else:
        st.info("MACD columns not available.")

    # Sentiment Analysis
    st.subheader("Sentiment Analysis")
    if headline:
        result = analyze_sentiment(headline)
        if isinstance(result, list) and len(result) > 0:
            label = result[0].get('label', 'N/A')
            score = result[0].get('score', 0)
            st.write(f"**Sentiment:** {label}  |  **Confidence:** {score:.2f}")
        else:
            st.warning("Sentiment analysis failed or returned unexpected format.")
