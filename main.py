import logging
import time
import google.cloud.logging
import os

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if int(os.environ.get("PRODUCTION", 0)) == 1:
        logging_client = google.cloud.logging.Client()
        logging_client.setup_logging()

    while True:
        logging.info("Sleeping for 5 seconds")
        time.sleep(5)