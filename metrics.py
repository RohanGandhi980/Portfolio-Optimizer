import pandas as pd
import numpy as np

#defining metrics like cagr, sharpe ratio, sortino, max drawdown, volatility

def cagr(equity_curve: pd.Series, period_per_year=252) -> float:
    if equity_curve is None or equity_curve.empty:
        return np.nan
    
    start_val = equity_curve.iloc[0]
    end_val = equity_curve.iloc[-1]
    n_periods = len(equity_curve)
    years = n_periods/period_per_year

    if start_val <=0 or years <=0:
        return np.nan
    return (end_val/start_val)**(1/years)-1

def sharpe(returns: pd.Series, risk_free_rate=0.0, periods_per_year = 252) -> float:
    if returns is None or returns.empty:
        return np.nan
    
    excess = returns - (risk_free_rate/periods_per_year)
    vol = returns.std()
    if vol == 0 or np.isnan(vol):
        return 0.0
    return (excess.mean()/vol)*np.sqrt(periods_per_year)

def sortino(returns:pd.Series, risk_free_rate=0.0,periods_per_year=252)->float:
    if returns is None or returns.empty:
        return np.nan
    downside = returns[returns<0]
    dd = downside.std()
    if dd == 0 or np.isnan(dd):
        return 0.0
    excess = returns - (risk_free_rate/periods_per_year)
    return (excess.mean()/dd)*np.sqrt(periods_per_year)

def max_drawdown(equity_curve:pd.Series)->float:
    if equity_curve is None or equity_curve.empty:
        return np.nan
    cummax = equity_curve.cummax()
    drawdown = equity_curve/cummax -1
    return float(drawdown.min())

def volatility(returns:pd.Series, periods_per_year=252) -> float:
    if returns is None or returns.empty:
        return np.nan
    return returns.std()*np.sqrt(periods_per_year)