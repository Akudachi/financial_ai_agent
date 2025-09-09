import matplotlib.pyplot as plt

def plot_data(df, ticker="Stock"):
    plt.figure(figsize=(10,5))
    plt.plot(df['Close'], label="Close Price")
    plt.plot(df['SMA_20'], label="SMA_20")
    plt.legend()
    plt.title(f"{ticker} Price with Indicators")
    plt.show()
