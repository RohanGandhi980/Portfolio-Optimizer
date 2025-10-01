import io
import base64
import matplotlib
matplotlib.use("Agg")  # non-interactive backend safe for servers
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def _fig_to_base64(fig) -> str:
    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png", dpi=120, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("ascii")

def plot_equity_curve(equity: pd.Series, title: str = "Equity Curve") -> str:
    if equity is None or equity.empty:
        return ""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(equity.index, equity.values)
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Equity")
    return _fig_to_base64(fig)

def plot_efficient_frontier(mu, cov, weights_opt=None) -> str:
    """
    Simple random sampling frontier + mark optimal portfolio if provided.
    """
    fig, ax = plt.subplots(figsize=(8, 6))

    # Random portfolios
    n_assets = len(mu)
    rets, vols = [], []
    for _ in range(3000):
        w = np.random.random(n_assets)
        w /= w.sum()
        r = w @ mu
        v = np.sqrt(w @ cov @ w)
        rets.append(r)
        vols.append(v)
    ax.scatter(vols, rets, s=8, alpha=0.3)

    # Optimal
    if weights_opt is not None:
        opt_r = weights_opt @ mu
        opt_v = np.sqrt(weights_opt @ cov @ weights_opt)
        ax.scatter([opt_v], [opt_r], marker="*", s=180, label="Max Sharpe")
        ax.legend()

    ax.set_xlabel("Volatility")
    ax.set_ylabel("Return")
    ax.set_title("Efficient Frontier (sampled)")
    return _fig_to_base64(fig)
