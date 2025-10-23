from abc import ABC, abstractmethod
import pandas as pd

class BaseVendor(ABC):

    def __init__(self, vendor_name: str, interface_name: str, start_date: str, end_date: str):
        self.vendor_name = vendor_name
        self.interface_name = interface_name
        self.start_date = start_date
        self.end_date = end_date
        self.raw_data = pd.DataFrame() 
        self.transformed_data = pd.DataFrame()


    @abstractmethod
    def fetch_data(self, symbols: list[str] | None = None) -> None:
        pass

    @abstractmethod
    def transform_data(self) -> pd.DataFrame:
        pass

    def load_data(self, output_path: str):
        if not self.transformed_data.empty:
            self.transformed_data.to_csv(output_path, index=False)
            print(f"Data successfully saved to {output_path}")
        else:
            print("No transformed data to save.")
