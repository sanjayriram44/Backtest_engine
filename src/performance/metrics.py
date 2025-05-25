import numpy as np
import pandas as pd

def calculate_total_return(final_portfolio_value, initial_capital):
    return (final_portfolio_value / initial_capital) - 1

def calculate_annualized_return(total_return, num_days):
    return np.power((1 + total_return), 252 / num_days) - 1

def calculate_annualized_volatility(daily_returns):
    return daily_returns.std() * np.sqrt(252)

def calculate_sharpe_ratio(annualized_return, annualized_volatility, risk_free_rate=0):
    try:
        return (annualized_return - risk_free_rate) / annualized_volatility
    except ZeroDivisionError:
        return np.nan

def calculate_sortino_ratio(daily_returns, annualized_return, risk_free_rate=0):
    negative_returns = daily_returns[daily_returns < 0]
    downside_volatility = negative_returns.std() * np.sqrt(252)
    return (annualized_return - risk_free_rate) / downside_volatility if downside_volatility > 0 else np.nan

def calculate_maximum_drawdown(portfolio_values):
    drawdown = portfolio_values / portfolio_values.cummax() - 1
    return drawdown.min()
