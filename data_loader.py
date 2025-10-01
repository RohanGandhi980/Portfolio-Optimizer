import pandas as pd 
import numpy as np

#loading yahoo query
try:
    from yahooquery import Ticker as YQTicker
except ImportError:
    YQTicker = None

#yfinance now
try:
    import yfinance as yf
except ImportError:
    yf = None


def _standardize(df: pd.DataFrame) -> pd.DataFrame:

    if df is None or df.empty:
        return pd.DataFrame()
    
    #keeping standard column names
    rename_map = {
        "open":"Open", "close":"Close", "high":"High","low":"Low",
        "adjclose":"Adj Close", "adj_close":"Adj Close", "volume":"Volume"
    }

    df = df.rename(columns={c: rename_map.get(c.lower(),c) for c in df.columns})

    required = ["Open","High","Low","Close","Adj Close","Volume"]

    for c in required:
        if c not in df.columns:
            if c == "Adj Close" and "Close" in df.columns:
                df["Adj Close"] = df["Close"]
            else:
                df[c] = pd.NA
    
    #sort and drop na 
    df = df[required].copy()
    df = df.sort_index()
    df = df.dropna(how="any")

    if not isinstance(df.index, pd.DatetimeIndex):
        if "date" in df.columns:
            df.set_index(pd.to_datetime(df["date"]))
            df = df.drop(columns=["date"])

    df.index = pd.to_datetime(df.index)
    df = df[~df.index.duplicated(keep="last")]
    return df

def get_data(ticker: str, start="2015-01-01", end="2025-01-01")->pd.DataFrame:
    #fetch ohlcv data
    #first trying for ticker data from yahooquery else falling back to yfinance

    tick = ticker.strip().upper()
    tried=[]

    candidates = []
    if tick.endswith(".NS") or tick.endswith(".BO"):
        candidates.append(tick)
    else:
        candidates.extend([f"{tick}.NS",f"{tick}.BO", tick])

    #trying yahooquery first
    if YQTicker:
        for sym in candidates:
            try:
                print(f"Trying yahooquery for {sym}..")
                yq = YQTicker(sym)
                df = yq.history(start=start,end=end)
                if df is not None or df is not df.empty:
                    if isinstance(df.index, pd.MultiIndex):
                        df = df.reset_index()

                        df = df.set_index("date")
                    df = _standardize(df)
                    if not df.empty:
                        print(f"Data loaded from yahooquery for {sym}")
                        return df
            except Exception as e:
                tried.append((sym, f"YahooQuery: {e}"))

    #falling back to yfinance now
    if yf: 
        for sym in candidates:
            try:
                print(f"Trying yfinance for {sym}")
                df = yf.download(start=start, end=end, progress=False, timeout=30)
                df = _standardize(df)
                if not df.empty:
                    print(f"Data loaded from yahoofinance for {sym}")
                    return df
            except Exception as e:
                tried.append((sym, f"yfinance: {e}"))

    raise ValueError(f"No data available for {ticker}. Tried: {tried}")

            






