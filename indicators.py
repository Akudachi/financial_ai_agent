import ta

def add_indicators(df):
    # Detect Close column dynamically
    close_col = next((col for col in df.columns if 'Close' in col), None)
    if close_col is None:
        raise ValueError("No Close column found in DataFrame")

    # Simple Moving Average (20)
    df['SMA_20'] = ta.trend.sma_indicator(df[close_col], window=20, fillna=True)

    # Exponential Moving Average (20)
    df['EMA_20'] = ta.trend.ema_indicator(df[close_col], window=20, fillna=True)

    # Relative Strength Index (14)
    df['RSI_14'] = ta.momentum.rsi(df[close_col], window=14, fillna=True)

    # MACD
    macd = ta.trend.MACD(df[close_col])
    df['MACD'] = macd.macd()
    df['MACD_Signal'] = macd.macd_signal()

    return df
