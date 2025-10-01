# Portfolio Optimizer & Multi-Strategy Backtester

A backtesting and portfolio optimization framework powered by **FastAPI**, designed for Indian and global stock markets.  
It fetches OHLCV data from **Yahoo Finance (`yfinance` + `yahooquery`)**, applies multiple trading strategies, and evaluates performance with industry-standard metrics like **CAGR, Sharpe Ratio, Sortino Ratio, Volatility, and Max Drawdown**.  

## Features
- Data fetching via **Yahoo Finance API** (`yfinance`, `yahooquery`)
- Multiple strategies supported:
  - Buy & Hold
  - SMA Crossover
  - RSI
  - Bollinger Bands
- Portfolio level backtesting with multiple tickers
- Metrics: CAGR, Sharpe, Sortino, Max Drawdown, Volatility


---

##  Installation
Clone the repository and install dependencies:

```bash
# Clone the repo
git clone https://github.com/RohanGandhi980/Portfolio-Optimizer.git
cd Portfolio-Optimizer

# Create a virtual environment (if using any api keys)
python -m venv venv
source venv/bin/activate   #mac
venv\Scripts\activate      #windows

#installing required files
pip install -r requirements.txt

uvicorn main:app --reload

#server should be running at - http://127.0.0.1:8000/docs

```
---
## Example Response


  "ticker": "TCS.NS",
  
  "metrics": 
  
    "Final Equity": 25487.25,
    
    "CAGR": 0.1184,
    
    "Sharpe": 0.65,
    
    "Sortino": 0.88,
    
    "Max Drawdown": -0.32,
    
    "Volatility": 0.21
    
  


