import pandas as pd
from typing import Callable, Dict

class Strategy:
    def __init__(self, indicators: Dict[str, Callable[[pd.DataFrame], pd.Series]], signal_logic: Callable[[pd.Series], int]):
        self.indicators = indicators  #The indicator is passed as a dictionary, the key is the name of the indicator 
        #and the value is the function that creates it from a dataframe
        self.signal_logic = signal_logic

    def _apply_strategy(self, df: pd.DataFrame) -> None:
        for name, indicator in self.indicators.items():
            df[name] = indicator(df)
        df["signal"] = df.apply(self.signal_logic, axis=1)
        df["positions"] = df["signal"].diff().fillna(0)

    def generate_signals(self, data: pd.DataFrame | dict[str, pd.DataFrame]) -> pd.DataFrame | dict[str, pd.DataFrame]:
        if isinstance(data, dict):
            for asset_data in data.values():
                self._apply_strategy(asset_data)
        else:
            self._apply_strategy(data)
        return data
