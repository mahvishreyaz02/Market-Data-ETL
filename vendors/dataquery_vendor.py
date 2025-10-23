import os
import pandas as pd
from datetime import datetime
from interfaces.base_vendor import BaseVendor
from helpers.data_fetcher import DataFetcher


class DataQueryVendor(BaseVendor):

    def fetch_data(self, symbols: list[str] | None = None) -> None:
        print("Fetching data from DataQuery...")

        self.raw_data = DataFetcher.load_and_filter_csvs(
            data_path=os.path.join("data", "stocks"),
            start_date=self.start_date,
            end_date=self.end_date,
            symbols=symbols, 
            n_random=4
        )

        if not self.raw_data.empty:
            print(f"DataQuery: Fetched {len(self.raw_data)} rows")
        else:
            print("DataQuery: No data fetched.")

    def transform_data(self) -> pd.DataFrame:
        if self.raw_data.empty:
            return pd.DataFrame()

        print("Transforming DataQuery data...")

        df = self.raw_data.copy()
        median_vol = df["Volume"].median()
        df["HighVolumeFlag"] = df["Volume"].apply(lambda v: "Yes" if v > median_vol else "No")
        df["Source"] = "DataQuery"
        df["LoadTime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.transformed_data = df[
            ["Symbol", "Date", "Open", "Close", "High", "Low", "Volume", "HighVolumeFlag", "Source", "LoadTime"]
        ]
        return self.transformed_data
