**Market Data ETL Pipeline**
This is a modular ETL pipeline for processing stock market data. It's designed to simulate a real-world scenario where data is fetched from multiple "vendors" (like Bloomberg or Barclays), transformed based on unique rules, and then loaded into a central database and CSV reports.

It's built to be flexible-you can run a job manually from your command line or trigger it from a simple web API.


**Tech Stack:**
- Python
- Flask: For the web API layer.
- Pandas: For all the data manipulation.
- SQLAlchemy: For writing to the SQLite database.


**How It Works**

1. *Trigger:* A user (or API client) starts a job by providing:
- A vendor (e.g., Bloomberg)
- An interface (e.g., GetData)
- A start_date and end_date
- (Optional) A list of symbols (e.g., ["AAPL", "TSLA"])

2. *Route:* The main controller (main.py) finds the correct vendor handler (like BloombergVendor) based on the request.

3. *Extract (E):* The handler uses the DataFetcher to read the right CSV files from the data/stocks/ folder. If no symbols were given, it grabs a random sample.

4. *Transform (T):* The data is filtered by the date range, and then the vendor-specific logic is applied (e.g., Bloomberg adds a DailyReturn column, while Barclays adds an AvgPrice column).

5. *Load (L):* The FileWriter takes the final, clean DataFrame and:
- Appends it to a table in the output/market_data.db SQLite database.
- Saves it as a new, timestamped CSV file in the output/ folder.



**How to Run the ETL**

You have two ways to run a job:

1. Using the Command Line (CLI)

*Example 1: Run for specific symbols*
(This will process AAPL and MSFT data from Bloomberg for the specified date range)

python main.py Bloomberg GetData --start_date 2020-01-01 --end_date 2020-01-31 --symbols AAPL MSFT

*Example 2: Run for a random sample*
(If you don't provide any symbols, it'll pick a few random ones)

python main.py Barclays MarketFeed --start_date 2021-01-01 --end_date 2021-01-10

2. Using the API (via Postman or curl)

*Step 1: Start the Flask server*

python app.py

It will be running at http://127.0.0.1:5000


*Step 2: Send a POST request*

Send a POST request to the /run_etl endpoint with a JSON body.

Endpoint: POST http://127.0.0.1:5000/run_etl

JSON Body (Example for specific symbols):

{
"vendor": "Barclays",
"interface": "MarketFeed",
"start_date": "2020-02-01",
"end_date": "2020-02-28",
"symbols": ["MSFT", "TSLA", "FAKETICKER"]
}

(Note: The logger will tell you that FAKETICKER wasn't found, but it will process the ones it did find)


JSON Body (Example for random sample):

{
"vendor": "DataQuery",
"interface": "DataPull",
"start_date": "2022-01-01",
"end_date": "2022-01-05",
"symbols": null
}


curl equivalent:

curl -X POST http://127.0.0.1:5000/run_etl \
-H "Content-Type: application/json" \
-d '{
"vendor": "Barclays",
"interface": "MarketFeed",
"start_date": "2020-02-01",
"end_date": "2020-02-28",
"symbols": ["MSFT", "TSLA"]
}'
