import streamlit as st
from src.data.data_handler import DataHandler
from src.strategy.strategy import Strategy
from src.backtest.backtester import Backtester

# Hardcoded strategies
my_strategy_1 = Strategy(
    indicators={
        "high": lambda df: df["close"].rolling(window=20).max(),
        "low": lambda df: df["close"].rolling(window=20).min(),
        "vol_avg": lambda df: df["volume"].rolling(window=20).mean(),
    },
    signal_logic=lambda row: 1 if (row["close"] >= row["high"] and row["volume"] > row["vol_avg"])
    else -1 if (row["close"] <= row["low"] and row["volume"] > row["vol_avg"])
    else 0
)

my_strategy_2 = Strategy(
    indicators={
        "sma_fast": lambda df: df["close"].rolling(window=20).mean(),
        "sma_slow": lambda df: df["close"].rolling(window=60).mean(),
    },
    signal_logic=lambda row: 1 if row["sma_fast"] > row["sma_slow"] else -1
)

def main():
    st.title("Backtesting Engine")

    with st.form(key="Strategy and commodity input"):
        ticker = st.text_input("Enter a ticker below:")
        strategy_name = st.radio("Select a strategy", ["volume_breakout", "sma_crossover"])
        submit_button = st.form_submit_button("Get backtest Results")

    if submit_button:
        if not ticker or not strategy_name:
            st.warning("All fields required.")
            return

        data = DataHandler(
            symbol=ticker,
            start_date="2023-01-01",
            end_date="2023-12-31",
            provider="yfinance"
        ).load_data()

        # Choose strategy based on input
        strategy = my_strategy_1 if strategy_name == "volume_breakout" else my_strategy_2

        data = strategy.generate_signals(data)

        backtester = Backtester()
        backtester.backtest(data)
        backtester.calculate_performance()

        st.success("Backtest complete. Scroll down to see the results.")

if __name__ == "__main__":
    main()
