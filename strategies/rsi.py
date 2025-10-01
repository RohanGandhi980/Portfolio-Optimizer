import pandas as pd
import numpy as np

#relative strength index

def rsi_strategy(df: pd.DataFrame, period: int = 14, oversold: int = 30, overbought: int = 70) -> pd.DataFrame:
    """
    RSI strategy: Buy when oversold, Sell when overbought.
    """
    df = df.copy()
    if "Adj Close" not in df.columns:
        raise ValueError("DataFrame must contain 'Adj Close' for RSI strategy.")

    # Price change
    delta = df["Adj Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    # Average gains/losses
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    # RSI
    rs = avg_gain / (avg_loss + 1e-9)  # avoid divide by zero
    df["RSI"] = 100 - (100 / (1 + rs))

    # Trading rule
    df["Signal"] = 0
    df.loc[df["RSI"] < oversold, "Signal"] = 1   # Buy
    df.loc[df["RSI"] > overbought, "Signal"] = -1  # Sell

    df["Signal"] = df["Signal"].fillna(0)
    return df
