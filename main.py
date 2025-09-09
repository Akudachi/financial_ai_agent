import streamlit as st
import pandas as pd
import plotly.graph_objects as go
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

# Chart type selection
chart_type = st.sidebar.selectbox(
    "Select Chart Type:",
    ["Line Chart", "Candlestick Chart", "OHLC Bar Chart"]
)

# ------------------ Run Analysis ------------------
if st.sidebar.button("Run Analysis"):

    st.subheader(f"Fetching data for {ticker}...")
    df = get_stock_data(ticker, period=period, interval=interval)

    if df.empty:
        st.error("Failed to fetch data. Please check the ticker symbol.")
    else:
        # Add indicators
        df = add_indicators(df)

        # Flatten MultiIndex columns if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in df.columns]

        # Detect columns dynamically
        open_col = next((col for col in df.columns if 'Open' in col), None)
        high_col = next((col for col in df.columns if 'High' in col), None)
        low_col = next((col for col in df.columns if 'Low' in col), None)
        close_col = next((col for col in df.columns if 'Close' in col), None)
        sma_col = next((col for col in df.columns if 'SMA' in col), None)
        ema_col = next((col for col in df.columns if 'EMA' in col), None)
        rsi_col = next((col for col in df.columns if 'RSI' in col), None)
        macd_col = next((col for col in df.columns if 'MACD' in col and 'Signal' not in col), None)
        macd_signal_col = next((col for col in df.columns if 'MACD_Signal' in col or 'Signal' in col), None)

        # ------------------ Latest Stock Data ------------------
        st.subheader("Latest Stock Data")
        st.dataframe(df.tail())

        # ------------------ Chart Rendering ------------------
        if chart_type == "Line Chart":
            price_cols = [col for col in [close_col, sma_col, ema_col] if col and col in df.columns]
            if price_cols:
                st.subheader("Price Chart (Close + SMA + EMA)")
                st.line_chart(df[price_cols])
            else:
                st.info("Price data not available for line chart.")

        elif chart_type == "Candlestick Chart":
            if open_col and high_col and low_col and close_col:
                st.subheader(f"{stock_choice} Candlestick Chart")
                fig = go.Figure(data=[go.Candlestick(
                    x=df.index,
                    open=df[open_col],
                    high=df[high_col],
                    low=df[low_col],
                    close=df[close_col],
                    increasing_line_color='green',
                    decreasing_line_color='red'
                )])
                fig.update_layout(xaxis_rangeslider_visible=False)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Cannot create candlestick chart: missing OHLC data.")

        elif chart_type == "OHLC Bar Chart":
            if open_col and high_col and low_col and close_col:
                st.subheader(f"{stock_choice} OHLC Bar Chart")
                fig = go.Figure(data=[go.Ohlc(
                    x=df.index,
                    open=df[open_col],
                    high=df[high_col],
                    low=df[low_col],
                    close=df[close_col],
                    increasing_line_color='green',
                    decreasing_line_color='red'
                )])
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Cannot create OHLC chart: missing OHLC data.")

        # ------------------ RSI Chart ------------------
        if rsi_col and rsi_col in df.columns:
            st.subheader("RSI (14-day)")
            st.line_chart(df[rsi_col])
        else:
            st.info("RSI column not available.")

        # ------------------ MACD Chart ------------------
        macd_cols = [col for col in [macd_col, macd_signal_col] if col and col in df.columns]
        if macd_cols:
            st.subheader("MACD")
            st.line_chart(df[macd_cols])
        else:
            st.info("MACD columns not available.")

        # ------------------ Sentiment Analysis ------------------
        st.subheader("Sentiment Analysis")
        if headline:
            result = analyze_sentiment(headline)
            if isinstance(result, list) and len(result) > 0:
                label = result[0].get('label', 'N/A')
                score = result[0].get('score', 0)
                st.write(f"**Sentiment:** {label}  |  **Confidence:** {score:.2f}")
            else:
                st.warning("Sentiment analysis failed or returned unexpected format.")
