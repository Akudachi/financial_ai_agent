import streamlit as st
import pandas as pd

# Try importing plotly
try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

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

# Graph type selection
chart_type = st.sidebar.selectbox(
    "Select Chart Type:", ["Line Chart", "Candlestick", "Bar Chart"]
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

        # Flatten MultiIndex columns
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in df.columns]

        # Detect columns dynamically
        close_col = next((col for col in df.columns if 'Close' in col), None)

        # Latest stock data
        st.subheader("Latest Stock Data")
        st.dataframe(df.tail())

        # ------------------ Chart Rendering ------------------
        if close_col and close_col in df.columns:
            st.subheader(f"{chart_type} of {ticker}")

            if PLOTLY_AVAILABLE:
                if chart_type == "Candlestick":
                    fig = go.Figure(data=[go.Candlestick(
                        x=df.index,
                        open=df['Open'],
                        high=df['High'],
                        low=df['Low'],
                        close=df[close_col]
                    )])
                    st.plotly_chart(fig, use_container_width=True)

                elif chart_type == "Bar Chart":
                    fig = go.Figure(data=[go.Bar(x=df.index, y=df[close_col])])
                    st.plotly_chart(fig, use_container_width=True)

                else:  # Line Chart
                    fig = go.Figure(data=[go.Scatter(x=df.index, y=df[close_col], mode="lines")])
                    st.plotly_chart(fig, use_container_width=True)

            else:
                st.warning("Plotly not installed. Falling back to simple Streamlit line chart.")
                st.line_chart(df[close_col])

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
