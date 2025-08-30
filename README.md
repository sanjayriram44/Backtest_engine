# Backtesting Engine

## Overview
This project is a **modular backtesting engine** built with **Python** and **Streamlit**. It allows users to test different trading strategies on historical data with configurable execution models, slippage assumptions, and order types.  

The engine is designed to be flexible, extensible, and user-friendly, making it a great foundation for quantitative research or algorithmic trading experimentation.

---
## Features
- **Data Handling**
  - Fetches historical equity price data from multiple providers (default: `yfinance` via OpenBB).
  - Supports single and multi-asset backtests.

- **Strategy Framework**
  - Easily define custom strategies by specifying:
    - **Indicators**: Rolling averages, volatility, breakouts, etc.
    - **Signal Logic**: Buy/sell/hold decisions based on indicator values.
  - Pre-built example strategies:
    - **Volume Breakout**
    - **SMA Crossover**

- **Execution & Slippage Modeling**
  - Supports **Market Orders** and **Limit Orders**.
  - Configurable **slippage models**:
    - Static (fixed percentage)
    - Dynamic (market impact based on volume and trade size)

- **Backtesting Engine**
  - Capital allocation and position tracking per asset.
  - Commission models: percentage-based and fixed.
  - Tracks portfolio value, cash, and positions over time.

- **Performance Analytics**
  - Metrics:
    - Total Return
    - Annualized Return
    - Annualized Volatility
    - Sharpe Ratio
    - Sortino Ratio
    - Maximum Drawdown
  - Interactive charts:
    - Portfolio value over time
    - Daily returns

- **Streamlit Frontend**
  - Intuitive UI for:
    - Ticker input
    - Strategy selection
    - Order type selection
    - Slippage model configuration
  - One-click backtest execution and results visualization.

---
## Requirements

`requirements.txt` should include:
- streamlit  
- pandas  
- numpy  
- openbb  
- yfinance  
- matplotlib *(optional, Streamlit charts used)*  

---

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

## Steps in the UI

1. Enter a ticker (e.g., AAPL).

2. Select a strategy (volume_breakout or sma_crossover).

3. Choose order type (Market or Limit).

4. Select slippage model (static, dynamic, or none).

5. Run the backtest.

6. View portfolio performance metrics and charts.


## Project Structure
src/
├── backtest/
│ └── backtester.py # Backtesting engine
├── data/
│ └── data_handler.py # Data loading (via OpenBB)
├── performance/
│ └── metrics.py # Performance metrics
├── strategy/
│ └── strategy.py # Strategy framework
main.py # Streamlit frontend


---

## Example Strategies

### Volume Breakout
- Buy when close ≥ rolling 20-day high with above-average volume.
- Sell when close ≤ rolling 20-day low with above-average volume.

### SMA Crossover
- Buy when 20-day SMA > 60-day SMA.
- Sell when 20-day SMA < 60-day SMA.

---

## Future Improvements
- Add support for crypto and futures.
- Extend order types (stop orders, trailing stops).
- Monte Carlo simulation of strategy robustness.
- Risk management modules (position sizing, leverage).
- More performance visualizations.

---

## License
MIT License
