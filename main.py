from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from data_loader import get_data
from backtester import Backtester
from strategies.buyhold import buy_and_hold
from strategies.sma_crossover import sma_crossover
from strategies.rsi import rsi_strategy
from strategies.bollinger import bollinger_bands

app = FastAPI(title="Portfolio Optimizer & Multi-Strategy Backtester")

#buy and hold
@app.get("/backtest/buyhold")
def run_buyhold(
    ticker: str = Query(..., description="e.g: ICICIBANK.NS"),
    start: str = Query("2015-01-01"),
    end: str = Query("2025-01-01")
):
    try:
        df = get_data(ticker, start, end)
        df = buy_and_hold(df)
        bt = Backtester(df)
        return JSONResponse(content={"ticker": ticker, "metrics": bt.run()})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


#sma crossover
@app.get("/backtest/sma")
def run_sma(
    ticker: str = Query(..., description="e.g., TCS.NS"),
    start: str = Query("2015-01-01"),
    end: str = Query("2025-01-01"),
    fast: int = Query(20, description="Fast SMA window"),
    slow: int = Query(50, description="Slow SMA window")
):
    try:
        df = get_data(ticker, start, end)
        df = sma_crossover(df, fast, slow)
        bt = Backtester(df)
        return JSONResponse(content={"ticker": ticker, "metrics": bt.run()})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


#rsi
@app.get("/backtest/rsi")
def run_rsi(
    ticker: str = Query(..., description="e.g., INFY.NS"),
    start: str = Query("2015-01-01"),
    end: str = Query("2025-01-01"),
    period: int = Query(14, description="RSI window"),
    oversold: int = Query(30),
    overbought: int = Query(70)
):
    try:
        df = get_data(ticker, start, end)
        df = rsi_strategy(df, period, oversold, overbought)
        bt = Backtester(df)
        return JSONResponse(content={"ticker": ticker, "metrics": bt.run()})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# bollinger bands
@app.get("/backtest/bollinger")
def run_bollinger(
    ticker: str = Query(..., description="e.g:RELIANCE.NS"),
    start: str = Query("2015-01-01"),
    end: str = Query("2025-01-01"),
    window: int = Query(20),
    num_std: int = Query(2)
):
    try:
        df = get_data(ticker, start, end)
        df = bollinger_bands(df, window, num_std)
        bt = Backtester(df)
        return JSONResponse(content={"ticker": ticker, "metrics": bt.run()})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# comparing all 4 strategies
@app.get("/backtest/compare")
def compare_strategies(
    ticker: str = Query(..., description="Stock ticker e.g: ICICIBANK.NS"),
    start: str = Query("2015-01-01"),
    end: str = Query("2025-01-01"),
    strategies: str = Query("buyhold,sma,rsi,bollinger", description="Comma-separated list of strategies"),
    fast: int = 20,
    slow: int = 50,
    rsi_period: int = 14,
    rsi_os: int = 30,
    rsi_ob: int = 70,
    bb_window: int = 20,
    bb_std: int = 2
):
    try:
        df = get_data(ticker, start, end)
        if df.empty:
            raise HTTPException(status_code=404, detail=f"No data for {ticker}")

        results = []
        for strat in strategies.split(","):
            strat = strat.strip().lower()
            df_copy = df.copy()

            if strat == "buyhold":
                df_copy = buy_and_hold(df_copy)
            elif strat == "sma":
                df_copy = sma_crossover(df_copy, fast=fast, slow=slow)
            elif strat == "rsi":
                df_copy = rsi_strategy(df_copy, period=rsi_period, oversold=rsi_os, overbought=rsi_ob)
            elif strat == "bollinger":
                df_copy = bollinger_bands(df_copy, window=bb_window, num_std=bb_std)
            else:
                continue  # skip unknown strategy names

            bt = Backtester(df_copy)
            metrics = bt.run()
            results.append({"strategy": strat, **metrics})

        return JSONResponse(content={"ticker": ticker, "comparison": results})

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))