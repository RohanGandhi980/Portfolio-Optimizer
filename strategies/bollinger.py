import pandas as pd

def bollinger_bands(df: pd.DataFrame, window: int = 20, num_std: int = 2) -> pd.DataFrame:
    """
    Bollinger Bands strategy: Buy when price < Lower Band, Sell when > Upper Band.
    """
    df = df.copy()
    if "Adj Close" not in df.columns:
        raise ValueError("DataFrame must contain 'Adj Close' for Bollinger Bands strategy.")

    rolling_mean = df["Adj Close"].rolling(window).mean()
    rolling_std = df["Adj Close"].rolling(window).std()

    df["Upper"] = rolling_mean + (rolling_std * num_std)
    df["Lower"] = rolling_mean - (rolling_std * num_std)

    # Signals
    df["Signal"] = 0
    df.loc[df["Adj Close"] < df["Lower"], "Signal"] = 1   # Buy
    df.loc[df["Adj Close"] > df["Upper"], "Signal"] = -1  # Sell

    df["Signal"] = df["Signal"].fillna(0)
    return df
