import streamlit as st
from src.data.data_handler import DataHandler
from src.strategy.strategy import Strategy
from src.backtest.backtester import Backtester

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

    if "order_type_selected" not in st.session_state:
        st.session_state.order_type_selected = False

    if "slippage_type_selected" not in st.session_state:
        st.session_state.slippage_type_selected = False

    ticker = st.text_input("Enter a ticker below:")
    strategy_name = st.radio("Select a strategy", ["volume_breakout", "sma_crossover"])
    order_type = st.radio("Select order type:", ["Market Order", "Limit Order"])

    if st.button("Confirm Order Type"):
        st.session_state.order_type_selected = True
        st.session_state.selected_order_type = order_type

    buy_price = 0
    if st.session_state.order_type_selected and st.session_state.selected_order_type == "Limit Order":
        buy_price = st.number_input("Enter Entry Price:", min_value=0.0, step=0.01, format = "%.5f")

    slippage_type = st.radio("Select a slippage model:", ["static", "dynamic", "None"])

    if st.button("Confirm slippage_model"):
        st.session_state.slippage_type_selected = True
        st.session_state.selected_slippage_type = slippage_type

    slippage_pct = 0
    impact_factor = 0
    if st.session_state.slippage_type_selected and st.session_state.selected_slippage_type == "static":
        slippage_pct = st.number_input("Enter the slippage percentage (e.g. 0.001 = 0.1%):", min_value=0.0, step=0.0001, value=0.001,format = "%.5f")
    elif st.session_state.slippage_type_selected and st.session_state.selected_slippage_type == "dynamic":
        slippage_pct = st.number_input("Enter base slippage (e.g. 0.001 = 0.1%):", min_value=0.0, step=0.0001, value=0.001, format = "%.5f")
        impact_factor = st.number_input("Enter impact factor (e.g. 0.01):", min_value=0.0, step=0.0001, value=0.01, format = "%.5f")

    if st.button("Run Backtest"):
        if not ticker or not strategy_name:
            st.warning("All fields required.")
            return

        data = DataHandler(
            symbol=ticker,
            start_date="2023-01-01",
            end_date="2023-12-31",
            provider="yfinance"
        ).load_data()

        strategy = my_strategy_1 if strategy_name == "volume_breakout" else my_strategy_2
        data = strategy.generate_signals(data)

        price_input = buy_price if st.session_state.selected_order_type == "Limit Order" else 0
        use_dynamic = st.session_state.selected_slippage_type == "dynamic"

        backtester = Backtester(
            buy_price=price_input,
            slippage_pct=slippage_pct,
            impact_factor=impact_factor,
            use_dynamic_slippage=use_dynamic
        )
        backtester.backtest(data)
        backtester.calculate_performance()

if __name__ == "__main__":
    main()
