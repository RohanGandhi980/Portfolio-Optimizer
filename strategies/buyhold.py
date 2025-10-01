import pandas as pd
import numpy as np
def buy_and_hold(df: pd.DataFrame) -> pd.DataFrame:
    """
    Simple Buy & Hold strategy: always long from start to end.
    """
    df = df.copy()
    df["Signal"] = 1  # always long
    return df