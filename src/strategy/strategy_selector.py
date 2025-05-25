from src.strategy.strategy import Strategy

def get_strategy(name: str, lookback: int) -> Strategy:
    if name == "volume_breakout":
        return Strategy(
            indicators={
                "high": lambda df: df["close"].rolling(window=lookback).max(),
                "low": lambda df: df["close"].rolling(window=lookback).min(),
                "vol_avg": lambda df: df["volume"].rolling(window=lookback).mean(),
            },
            signal_logic=lambda row: 1 if (row["close"] >= row["high"] and row["volume"] > row["vol_avg"])
                            else -1 if (row["close"] <= row["low"] and row["volume"] > row["vol_avg"])
                            else 0
        )
    
    elif name == "sma_crossover":
        return Strategy(
            indicators={
                "sma_fast": lambda df: df["close"].rolling(window=lookback).mean(),
                "sma_slow": lambda df: df["close"].rolling(window=lookback * 3).mean(),
            },
            signal_logic=lambda row: 1 if row["sma_fast"] > row["sma_slow"] else -1
        )

    else:
        raise ValueError(f"Unknown strategy: {name}")
