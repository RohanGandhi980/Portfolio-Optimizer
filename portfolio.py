import numpy as np
import pandas as pd
from scipy.optimize import minimize
from data_loader import get_data

def _annualize_returns(returns: pd.DataFrame, periods_per_year=252):
    mu = returns.mean() * periods_per_year
    cov = returns.cov() * periods_per_year
    return mu, cov

def _neg_sharpe(weights, mu, cov, rf=0.0):
    ret = weights @ mu
    vol = np.sqrt(weights @ cov @ weights)
    if vol == 0:
        return 1e6
    return -(ret - rf) / vol

def max_sharpe_weights(mu, cov, rf=0.0, weight_bounds=(0.0, 1.0)):
    n = len(mu)
    x0 = np.repeat(1.0 / n, n)
    bounds = [weight_bounds] * n
    cons = [{"type": "eq", "fun": lambda w: np.sum(w) - 1.0}]
    res = minimize(_neg_sharpe, x0, args=(mu, cov, rf), method="SLSQP", bounds=bounds, constraints=cons)
    if not res.success:
        raise ValueError(f"Optimization failed: {res.message}")
    return res.x

def build_return_matrix(tickers, start="2018-01-01", end="2025-01-01"):
    prices = []
    used = []
    for t in tickers:
        df = get_data(t, start=start, end=end)
        if df is not None and not df.empty:
            prices.append(df["Adj Close"].rename(t))
            used.append(t)
    if not prices:
        raise ValueError("No valid tickers with data.")
    price_df = pd.concat(prices, axis=1).dropna(how="any")
    returns = price_df.pct_change().dropna()
    return returns, used

def optimize_portfolio(tickers, start="2018-01-01", end="2025-01-01", rf=0.0, bounds=(0.0, 1.0)):
    returns, used = build_return_matrix(tickers, start=start, end=end)
    mu, cov = _annualize_returns(returns)
    w = max_sharpe_weights(mu.values, cov.values, rf=rf, weight_bounds=bounds)
    weights = dict(zip(used, np.round(w, 4)))
    portfolio_return = float(w @ mu.values)
    portfolio_vol = float(np.sqrt(w @ cov.values @ w))
    sharpe = (portfolio_return - rf) / portfolio_vol if portfolio_vol > 0 else np.nan

    return {
        "tickers_used": used,
        "weights": weights,
        "annual_return": round(portfolio_return, 4),
        "annual_volatility": round(portfolio_vol, 4),
        "sharpe": round(float(sharpe), 4)
    }
