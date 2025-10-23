import os
import pandas as pd
import random
from utils.logger import get_logger

logger = get_logger()

class DataFetcher:
    @staticmethod
    def load_and_filter_csvs(
        data_path: str,
        start_date: str,
        end_date: str,
        symbols: list[str] | None = None,
        n_random: int = 4
    ) -> pd.DataFrame:


        if not os.path.isdir(data_path):
            logger.error(f"Data directory not found at: {data_path}")
            return pd.DataFrame()

        all_files = [f for f in os.listdir(data_path) if f.upper().endswith(".CSV")]
        all_symbols_map = {f.upper().replace(".CSV", ""): f for f in all_files}
        
        files_to_load = []
        
        # Case 1: Specific symbols are requested
        if symbols:
            missing_symbols = []
            for sym in symbols:
                upper_sym = sym.upper()
                if upper_sym in all_symbols_map:
                    files_to_load.append(all_symbols_map[upper_sym])
                else:
                    missing_symbols.append(sym)
            
            if missing_symbols:
                logger.warning(f"The following symbols were not found and will be skipped: {missing_symbols}")

        # Case 2: No symbols requested, get a random sample
        else:
            if len(all_files) > 0:
                files_to_load = random.sample(all_files, min(n_random, len(all_files)))


        if not files_to_load:
            logger.warning("No files to load. Either no symbols were matched or the data directory is empty.")
            return pd.DataFrame()

        dfs = []
        for file in files_to_load:
            symbol = file.upper().replace(".CSV", "")
            try:
                df = pd.read_csv(os.path.join(data_path, file))
                df["Symbol"] = symbol
                dfs.append(df)
            except Exception as e:
                logger.error(f"Could not read or process file: {file}. Error: {e}")
        
        if not dfs:
            return pd.DataFrame()

        combined_df = pd.concat(dfs, ignore_index=True)

        try:
            combined_df['Date'] = pd.to_datetime(combined_df['Date'])
            start_date_dt = pd.to_datetime(start_date)
            end_date_dt = pd.to_datetime(end_date)
            mask = (combined_df['Date'] >= start_date_dt) & (combined_df['Date'] <= end_date_dt)
            return combined_df.loc[mask].copy()
        except Exception as e:
            logger.error(f"Error filtering dates. Ensure dates are in correct format. Error: {e}")
            return pd.DataFrame()
