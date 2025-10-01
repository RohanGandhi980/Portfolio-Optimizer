import pandas as pd
import numpy as np

def sma_crossover(df: pd.DataFrame, fast: int = 20, slow: int = 50) -> pd.DataFrame:
    """
    SMA crossover: long when fast SMA > slow SMA, else 0.
    """
    df = df.copy()
    if "Adj Close" not in df.columns:
        raise ValueError("DataFrame must contain 'Adj Close' for SMA strategy.")

    df["SMA_Fast"] = df["Adj Close"].rolling(fast).mean()
    df["SMA_Slow"] = df["Adj Close"].rolling(slow).mean()
    df["Signal"] = np.where(df["SMA_Fast"] > df["SMA_Slow"], 1, 0)

    # Fill start values with 0 to avoid NaNs
    df["Signal"] = df["Signal"].fillna(0)
    return df