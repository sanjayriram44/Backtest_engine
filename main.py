import streamlit as st
import yaml

from src.data.data_handler import DataHandler
from src.strategy.strategy_selector import get_strategy
from src.backtest.backtester import Backtester


st.title("Backtesting Engine")


def load_config(path: str) -> dict:
    with open(path, "r") as yaml_file:
        return yaml.safe_load(yaml_file)


def main():
    config = load_config("config/strategy_config.yaml")

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
            start_date=config["start_date"],
            end_date=config["end_date"],
            provider=config.get("provider", "yfinance"),
        ).load_data()

        strategy = get_strategy(
            name=strategy_name,
            lookback=config.get("lookback", 20)
        )

        data = strategy.generate_signals(data)

        backtester = Backtester()
        backtester.backtest(data)
        backtester.calculate_performance()

        # Display performance metrics or results here (optional)
        st.success("Backtest complete. Check logs or results as needed.")


if __name__ == "__main__":
    main()
