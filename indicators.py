import ta

def add_indicators(df):
    """
    Adds technical indicators with fixed periods:
    - SMA_20
    - EMA_20
    - RSI_14
    - MACD and MACD_Signal
    """
    # Detect Close column dynamically
    close_col = next((col for col in df.columns if 'Close' in col), None)
    if close_col is None:
        raise ValueError("No 'Close' column found in DataFrame.")

    # Fixed indicator periods
    df['SMA_20'] = ta.trend.sma_indicator(df[close_col], window=20, fillna=True)
    df['EMA_20'] = ta.trend.ema_indicator(df[close_col], window=20, fillna=True)
    df['RSI_14'] = ta.momentum.rsi(df[close_col], window=14, fillna=True)

    # MACD
    macd = ta.trend.MACD(df[close_col])
    df['MACD'] = macd.macd()
    df['MACD_Signal'] = macd.macd_signal()

    return df
