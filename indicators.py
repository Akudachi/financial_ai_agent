import ta

def add_indicators(df, sma_window=20, ema_window=20, rsi_window=14):
    """
    Adds technical indicators to the stock DataFrame:
    - Simple Moving Average (SMA)
    - Exponential Moving Average (EMA)
    - Relative Strength Index (RSI)
    - MACD and MACD Signal

    Parameters:
        df (pd.DataFrame): Stock data with 'Close' column
        sma_window (int): Window size for SMA
        ema_window (int): Window size for EMA
        rsi_window (int): Window size for RSI

    Returns:
        pd.DataFrame: DataFrame with new indicator columns
    """
    # Detect Close column dynamically
    close_col = next((col for col in df.columns if 'Close' in col), None)
    if close_col is None:
        raise ValueError("No 'Close' column found in DataFrame.")

    # Simple Moving Average (SMA)
    df[f'SMA_{sma_window}'] = ta.trend.sma_indicator(df[close_col], window=sma_window, fillna=True)

    # Exponential Moving Average (EMA)
    df[f'EMA_{ema_window}'] = ta.trend.ema_indicator(df[close_col], window=ema_window, fillna=True)

    # Relative Strength Index (RSI)
    df[f'RSI_{rsi_window}'] = ta.momentum.rsi(df[close_col], window=rsi_window, fillna=True)

    # MACD
    macd = ta.trend.MACD(df[close_col])
    df['MACD'] = macd.macd()
    df['MACD_Signal'] = macd.macd_signal()

    return df
