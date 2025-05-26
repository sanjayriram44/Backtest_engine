import pandas as pd
from typing import Dict
import streamlit as st
from src.performance.metrics import (
    calculate_total_return,
    calculate_annualized_return,
    calculate_annualized_volatility,
    calculate_sharpe_ratio,
    calculate_sortino_ratio,
    calculate_maximum_drawdown
)

class Backtester:
    def __init__(self, initial_capital: float = 10000, commission_pct: float = 0.001, commission_fixed: float = 1.0, buy_price: float = 0):
        self.initial_capital = initial_capital
        self.commission_pct = commission_pct
        self.commission_fixed = commission_fixed
        self.assets_data = {}
        self.portfolio_history = {}
        self.daily_portfolio_values = []
        self.buy_price = buy_price

    def calculate_commission(self, trade_value: float) -> float:
        return max(trade_value * self.commission_pct, self.commission_fixed)

    def execute_trade(self, asset: str, signal: int, price: float) -> None:
        data = self.assets_data[asset]
        if signal > 0 and data["cash"] > 0 and (price >= self.buy_price or self.buy_price == 0):
            trade_value = data["cash"]
            commission = self.calculate_commission(trade_value)
            shares_to_buy = (trade_value - commission) / price
            data["positions"] += shares_to_buy
            data["cash"] -= trade_value
        elif signal < 0 and data["positions"] > 0:
            trade_value = data["positions"] * price
            commission = self.calculate_commission(trade_value)
            data["cash"] += trade_value - commission
            data["positions"] = 0

    def update_portfolio(self, asset: str, price: float) -> None:
        data = self.assets_data[asset]
        data["position_value"] = data["positions"] * price
        data["total_value"] = data["cash"] + data["position_value"]
        self.portfolio_history[asset].append(data["total_value"])

    def backtest(self, data: pd.DataFrame | dict[str, pd.DataFrame]) -> None:
        if isinstance(data, pd.DataFrame):
            data = {"SINGLE_ASSET": data}
        split_capital = self.initial_capital / len(data)
        for asset, df in data.items():
            self.assets_data[asset] = {
                "cash": split_capital,
                "positions": 0,
                "position_value": 0,
                "total_value": split_capital
            }
            self.portfolio_history[asset] = []
            for _, row in df.iterrows():
                self.execute_trade(asset, row["signal"], row["close"])
                self.update_portfolio(asset, row["close"])
                if len(self.daily_portfolio_values) < len(df):
                    self.daily_portfolio_values.append(self.assets_data[asset]["total_value"])
                else:
                    self.daily_portfolio_values[len(self.portfolio_history[asset]) - 1] += self.assets_data[asset]["total_value"]

    def calculate_performance(self, plot: bool = True) -> None:
        if not self.daily_portfolio_values or all(v == self.initial_capital for v in self.daily_portfolio_values):
            st.warning("No trades were executed. Backtest results are not available.")
            return

        portfolio_values = pd.Series(self.daily_portfolio_values)
        daily_returns = portfolio_values.pct_change().dropna()
        total_return = calculate_total_return(portfolio_values.iloc[-1], self.initial_capital)
        annualized_return = calculate_annualized_return(total_return, len(portfolio_values))
        annualized_volatility = calculate_annualized_volatility(daily_returns)
        sharpe_ratio = calculate_sharpe_ratio(annualized_return, annualized_volatility)
        sortino_ratio = calculate_sortino_ratio(daily_returns, annualized_return)
        max_drawdown = calculate_maximum_drawdown(portfolio_values)

        st.write(f"Final Portfolio Value: {portfolio_values.iloc[-1]:.2f}")
        st.write(f"Total Return: {total_return * 100:.2f}%")
        st.write(f"Annualized Return: {annualized_return * 100:.2f}%")
        st.write(f"Annualized Volatility: {annualized_volatility * 100:.2f}%")
        st.write(f"Sharpe Ratio: {sharpe_ratio:.2f}")
        st.write(f"Sortino Ratio: {sortino_ratio:.2f}")
        st.write(f"Maximum Drawdown: {max_drawdown * 100:.2f}%")

        if plot:
            self.plot_performance(portfolio_values, daily_returns)


    def plot_performance(self, portfolio_values: pd.Series, daily_returns: pd.Series):
        st.subheader("📈 Portfolio Value Over Time")
        st.line_chart(portfolio_values)

        st.subheader("📊 Daily Returns Over Time")
        st.line_chart(daily_returns)
