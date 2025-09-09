import streamlit as st
from data_fetcher import get_stock_data
from indicators import add_indicators
from sentiment import analyze_sentiment
from utils import plot_data

st.title("📈 Financial AI Agent")

# Input for stock ticker
ticker = st.text_input("Enter Stock Ticker (e.g. AAPL, TSLA, MSFT):", "AAPL")

if st.button("Run Analysis"):
    st.write(f"Fetching data for {ticker}...")
    df = get_stock_data(ticker)
    df = add_indicators(df)
    
    # Show latest stock data
    st.write("### Stock Data", df.tail())

    # Plot Close price + SMA
    st.write("### Plot")
    st.line_chart(df[['Close','SMA_20']])

    # Sentiment Analysis
    st.write("### Sentiment Analysis")
    text = st.text_input("Enter news headline:", "Apple launches new iPhone with strong sales")
    if text:
        result = analyze_sentiment(text)
        label = result['label']
        score = result['score']
        st.write(f"Sentiment: {label} (Confidence: {score:.2f})")
