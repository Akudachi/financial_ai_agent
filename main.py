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

    # Dynamically find columns
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
    plot_cols = [col for col in [close_col, sma_col, ema_col] if col in df.columns]
    if plot_cols:
        st.subheader("Price Chart (Close + SMA + EMA)")
        st.line_chart(df[plot_cols])
    else:
        st.warning("No price columns available for plotting.")

    # Plot RSI
    if rsi_col and rsi_col in df.columns:
        st.subheader("RSI (14-day)")
        st.line_chart(df[rsi_col])

    # Plot MACD + Signal
    if macd_col and macd_signal_col and macd_col in df.columns and macd_signal_col in df.columns:
        st.subheader("MACD")
        st.line_chart(df[[macd_col, macd_signal_col]])

    # Sentiment Analysis
    st.subheader("Sentiment Analysis")
    if headline:
        result = analyze_sentiment(headline)
        label = result['label']
        score = result['score']
        st.write(f"**Sentiment:** {label}  |  **Confidence:** {score:.2f}")
