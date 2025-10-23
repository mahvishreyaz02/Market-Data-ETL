import logging
import os
from datetime import datetime


def get_logger(name="ETLLogger"):

    os.makedirs("logs", exist_ok=True)
    log_filename = datetime.now().strftime("logs/etl_%Y%m%d.log")

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[    #defines where the logs should go
            logging.FileHandler(log_filename),  # writes logs to a file
            logging.StreamHandler()  # prints logs to console
        ]
    )

    logger = logging.getLogger(name)
    return logger
