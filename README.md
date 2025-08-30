# Backtesting Engine

## Overview
This project is a **modular backtesting engine** built with **Python** and **Streamlit**. It lets you test trading strategies on historical data with configurable execution models, slippage assumptions, and order types. The engine is designed to be flexible, extensible, and straightforward to demo.

---

## Features
- **Data Handling**
  - Historical equity prices via OpenBB (default provider: `yfinance`).
  - Single- or multi-asset backtests.

- **Strategy Framework**
  - Define custom strategies by composing:
    - **Indicators** (e.g., rolling highs/lows, SMAs).
    - **Signal logic** (buy/sell/hold).
  - Included example strategies:
    - **Volume Breakout**
    - **SMA Crossover**

- **Execution & Slippage**
  - **Market** and **Limit** orders.
  - **Static slippage** (fixed %) and **Dynamic slippage** (market-impact based on dollar volume).

- **Backtesting Engine**
  - Capital allocation, positions, commissions (percent and fixed), portfolio value tracking.

- **Performance Analytics**
  - Total Return, Annualized Return/Volatility, Sharpe, Sortino, Max Drawdown.
  - Charts for portfolio value and daily returns.

- **Streamlit UI**
  - Inputs for ticker, strategy, order type, slippage model.
  - One-click backtest and metric display.

---

## Requirements

Add these to `requirements.txt`:
- streamlit  
- pandas  
- numpy  
- openbb  
- yfinance  
- matplotlib  *(optional; Streamlit charts are used)*

---

## Usage

Run the Streamlit app:
```bash
streamlit run main.py
```
## Steps in the UI

1. Enter a ticker (e.g., AAPL).

2. Choose a strategy (volume_breakout or sma_crossover).

3. Select order type (Market or Limit).

4. Pick slippage model (static, dynamic, or none).

5. Run the backtest.

6. Review metrics and charts.

---
## Project Structure
```text
src/
├── backtest/
│   └── backtester.py       # Backtesting engine
├── data/
│   └── data_handler.py     # Data loading (via OpenBB)
├── performance/
│   └── metrics.py          # Performance metrics
├── strategy/
│   └── strategy.py         # Strategy framework
main.py                      # Streamlit frontend entry point
requirements.txt             # Dependencies
README.md                    # Documentation
.gitignore                   # Git ignore rules
```

---

## Example Strategies
1. Volume Breakout

   Buy when close ≥ rolling 20-day high with above-average volume.

   Sell when close ≤ rolling 20-day low with above-average volume.

2. SMA Crossover

   Buy when 20-day SMA > 60-day SMA.

   Sell when 20-day SMA < 60-day SMA.

---

## License

MIT License
