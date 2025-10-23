import json
import argparse 
from utils.logger import get_logger
from utils.file_writer import FileWriter
from vendors.bloomberg_vendor import BloombergVendor
from vendors.barclays_vendor import BarclaysVendor
from vendors.dataquery_vendor import DataQueryVendor

def load_config():
    with open("config/vendor_config.json", "r") as file:
        return json.load(file)

def main():
    logger = get_logger()
    logger.info("Market Data ETL Process Started")

    parser = argparse.ArgumentParser(description="Run the Market Data ETL process.")
    parser.add_argument("vendor", help="The name of the vendor (e.g., Bloomberg).")
    parser.add_argument("interface", help="The interface to use for the vendor.")
    parser.add_argument("--start_date", required=True, help="Start date in YYYY-MM-DD format.")
    parser.add_argument("--end_date", required=True, help="End date in YYYY-MM-DD format.")
    parser.add_argument("--symbols", nargs='*', help="Optional list of stock symbols to process (e.g., AAPL GOOG).")
    
    args = parser.parse_args()

    vendor_name = args.vendor
    interface_name = args.interface
    start_date = args.start_date
    end_date = args.end_date
    symbols = args.symbols #list of strings or None

    config = load_config()

    if vendor_name not in config:
        logger.error(f"Unknown vendor: {vendor_name}")
        exit(1)

    if interface_name not in config[vendor_name]["interfaces"]:
        logger.error(f"Invalid interface '{interface_name}' for vendor '{vendor_name}'")
        exit(1)

    vendor_map = {
        "Bloomberg": BloombergVendor,
        "Barclays": BarclaysVendor,
        "DataQuery": DataQueryVendor,
    }

    VendorClass = vendor_map[vendor_name]

    etl = VendorClass(vendor_name, interface_name, start_date, end_date)

    try:
        logger.info(f"Fetching data for symbols: {symbols or 'random sample'}...")
        etl.fetch_data(symbols=symbols)

        if etl.raw_data is None or etl.raw_data.empty:
            logger.warning("No data fetched. Aborting ETL process.")
            print("No data fetched for the given symbols or date range.") 
            return 

        logger.info("Transforming data...")
        transformed_df = etl.transform_data()

        logger.info("Saving data...")
        writer = FileWriter()
        csv_path = writer.save_to_csv(transformed_df, vendor_name, interface_name)
        db_path = writer.save_to_sqlite(transformed_df, vendor_name, interface_name)
        
        success_message = f"ETL complete. CSV saved to: {csv_path}. DB saved to: {db_path}."
        logger.info(success_message)
        print(success_message) 

    except Exception as e:
        logger.exception(f"ETL process failed: {e}")
        exit(1)

if __name__ == "__main__":
    main()
