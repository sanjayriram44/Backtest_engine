from openbb import obb
import pandas as pd
from typing import Optional

class DataHandler:
    def __init__(self, symbol: str, start_date: Optional[str] = None, end_date: Optional[str] = None, provider: str = "yfinance"):
        self.symbol = symbol.upper()
        self.start_date = start_date
        self.end_date = end_date
        self.provider = provider

    def load_data(self) -> pd.DataFrame | dict[str, pd.DataFrame]:
        data = obb.equity.price.historical(
            symbol=self.symbol,
            start_date=self.start_date,
            end_date=self.end_date,
            provider=self.provider,
        ).to_df()
        if "," in self.symbol:
            data = data.reset_index().set_index("symbol")
            return {sym: data.loc[sym] for sym in self.symbol.split(",")}
        return data
