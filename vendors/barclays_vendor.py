import os
import pandas as pd
from datetime import datetime
from interfaces.base_vendor import BaseVendor
from helpers.data_fetcher import DataFetcher


class BarclaysVendor(BaseVendor):

    def fetch_data(self, symbols: list[str] | None = None) -> None:
        print("Fetching data from Barclays...")

        self.raw_data = DataFetcher.load_and_filter_csvs(
            data_path=os.path.join("data", "stocks"),
            start_date=self.start_date,
            end_date=self.end_date,
            symbols=symbols, 
            n_random=4
        )

        if not self.raw_data.empty:
            print(f"Barclays: Fetched {len(self.raw_data)} rows")
        else:
            print("Barclays: No data fetched.")

    def transform_data(self) -> pd.DataFrame:
        if self.raw_data.empty:
            return pd.DataFrame()

        print("Transforming Barclays data...")
        df = self.raw_data.copy()
        df["AvgPrice"] = ((df["Open"] + df["Close"]) / 2).round(2)
        df.rename(columns={"Date": "TradeDate", "Volume": "TradedVolume"}, inplace=True)
        df["Source"] = "Barclays"
        df["LoadTime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.transformed_data = df[
            ["Symbol", "TradeDate", "Open", "Close", "AvgPrice", "High", "Low", "TradedVolume", "Source", "LoadTime"]
        ]
        return self.transformed_data
