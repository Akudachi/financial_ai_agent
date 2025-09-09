import streamlit as st
import pandas as pd
from data_fetcher import get_stock_data
from indicators import add_indicators
from sentiment import analyze_sentiment

st.set_page_config(page_title="📈 Financial AI Agent", layout="wide")
st.title("📈 Financial AI Agent")

# ------------------ Sidebar Inputs ------------------
st.sidebar.header("Stock & Sentiment Input")

# Popular stocks
popular_stocks = {
    "Apple": "AAPL",
    "Tesla": "TSLA",
    "Microsoft": "MSFT",
    "Amazon": "AMZN",
    "Google": "GOOGL"
}

# Select stock
stock_choice = st.sidebar.selectbox(
    "Select Stock:", list(popular_stocks.keys()) + ["Other"]
)

if stock_choice == "Other":
    ticker = st.sidebar.text_input("Enter Stock Ticker:", "AAPL")
else:
    ticker = popular_stocks[stock_choice]

headline = st.sidebar.text_input("Enter News Headline:", f"{stock_choice} latest news")

# Additional parameters
period = st.sidebar.selectbox("Select data period:", ["1mo", "3mo", "6mo", "1y"])
interval = st.sidebar.selectbox("Select interval:", ["1d", "1h", "15m"])
SMA_window = st.sidebar.number_input("SMA window:", min_value=5, max_value=100, value=20)
EMA_window = st.sidebar.number_input("EMA window:", min_value=5, max_value=100, value=20)
RSI_window = st.sidebar.number_input("RSI window:", min_value=5, max_value=50, value=14)

# ------------------ Run Analysis ------------------
if st.sidebar.button("Run Analysis"):

    st.subheader(f"Fetching data for {ticker}...")
    df = get_stock_data(ticker, period=period, interval=interval)

    if df.empty:
        st.error("Failed to fetch data. Please check the ticker symbol.")
    else:
        # Add indicators
        df = add_indicators(df, sma_window=SMA_window, ema_window=EMA_window, rsi_window=RSI_window)

        # Flatten MultiIndex columns
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in df.columns]

        # Detect columns dynamically
        close_col = next((col for col in df.columns if 'Close' in col), None)
        sma_col = next((col for col in df.columns if 'SMA' in col), None)
        ema_col = next((col for col in df.columns if 'EMA' in col), None)
        rsi_col = next((col for col in df.columns if 'RSI' in col), None)
        macd_col = next((col for col in df.columns if 'MACD' in col and 'Signal' not in col), None)
        macd_signal_col = next((col for col in df.columns if 'MACD_Signal' in col or 'Signal' in col), None)

        # Latest stock data
        st.subheader("Latest Stock Data")
        st.dataframe(df.tail())

        # Price chart
        price_cols = [col for col in [close_col, sma_col, ema_col] if col and col in df.columns]
        if price_cols:
            st.subheader("Price Chart (Close + SMA + EMA)")
            st.line_chart(df[price_cols])

        # RSI chart
        if rsi_col and rsi_col in df.columns:
            st.subheader("RSI (14-day)")
            st.line_chart(df[rsi_col])
        else:
            st.info("RSI column not available.")

        # MACD chart
        macd_cols = [col for col in [macd_col, macd_signal_col] if col and col in df.columns]
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
