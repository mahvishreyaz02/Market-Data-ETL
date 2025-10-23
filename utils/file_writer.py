import os
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from utils.logger import get_logger

logger = get_logger()

class FileWriter:
    def __init__(self, output_folder="output"):
        self.output_folder = output_folder
        os.makedirs(self.output_folder, exist_ok=True)

    def save_to_csv(self, df: pd.DataFrame, vendor: str, interface: str) -> str:
        date_str = datetime.now().strftime("%Y%m%d")
        filename = f"{vendor}_{interface}_{date_str}.csv"
        output_path = os.path.join(self.output_folder, filename)

        df.to_csv(output_path, index=False)
        logger.info(f"Data saved to CSV: {output_path}")
        return output_path

    def save_to_sqlite(self, df: pd.DataFrame, vendor: str, interface: str) -> str:
        db_path = os.path.join(self.output_folder, "market_data.db")
        engine = create_engine(f"sqlite:///{db_path}")

        table_name = f"{vendor.lower()}_{interface.lower()}"

        try:
            df.to_sql(table_name, engine, if_exists="append", index=False)
            logger.info(f"Data loaded into SQLite table: {table_name}")
            return db_path
        except Exception as e:
            logger.error(f"Failed to load data into SQLite: {e}")
            raise
