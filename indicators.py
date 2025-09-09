import ta
import pandas as pd

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    # Ensure we only take the "Close" column as a 1D Series
    if isinstance(df.columns, pd.MultiIndex):
        close = df['Close'].iloc[:, 0]  # take first level if multi-index
    else:
        close = df['Close']

    # Add 20-day Simple Moving Average
    df['SMA_20'] = ta.trend.sma_indicator(close=close, window=20)

    # You can add more indicators here if needed
    return df
