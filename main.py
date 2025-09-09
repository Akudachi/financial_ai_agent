import streamlit as st
from data_fetcher import get_stock_data
from indicators import add_indicators
from sentiment import analyze_sentiment
from model import prepare_dataset, train_model
from utils import plot_data

st.title("📈 Financial AI Agent")

ticker = st.text_input("Enter Stock Ticker (e.g. AAPL, TSLA, MSFT):", "AAPL")

if st.button("Run Analysis"):
    st.write(f"Fetching data for {ticker}...")
    df = get_stock_data(ticker)
    df = add_indicators(df)
    
    st.write("### Stock Data", df.tail())

    st.write("### Plot")
    st.line_chart(df[['Close','SMA_20']])

    # Machine Learning
    X, y = prepare_dataset(df)
    model = train_model(X, y)
    pred = model.predict([X.iloc[-1]])[0]
    st.write("### AI Prediction")
    st.success("📊 Next day trend: UP ⬆️" if pred==1 else "📉 Next day trend: DOWN ⬇️")

    # Sentiment Example
    st.write("### Sentiment Analysis")
    text = st.text_input("Enter news headline:", "Apple launches new iPhone with strong sales")
    if text:
        label, score = analyze_sentiment(text)
        st.write(f"Sentiment: {label} (Confidence: {score:.2f})")
