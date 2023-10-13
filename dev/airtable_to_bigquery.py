"""
Exercises to demo...

1 -- Updating a Parsons connector in real time
2 -- Using the Docker environment to update the log level
"""

import logging
import os
from parsons import Table
from parsons.google.google_bigquery import GoogleBigQuery as BigQuery
from parsons.airtable import Airtable

logger = logging.getLogger(__name__)

##########


def get_airtable_data(airtable: Airtable) -> Table:
    """
    Read target Airtable base and return data in a Parsons table
    """
    pass


def write_to_bigquery(bq: BigQuery, tbl: Table):
    """
    Writes an incoming Parosns table to BigQuery
    """
    pass


def run(
    airtable_api_key: str,
    bigquery_app_creds: str,
    bigquery_project_id: str,
    log_level: int = 20,
):
    logger.setLevel(level=log_level)
    bq = BigQuery(bigquery_app_creds, bigquery_project_id)
    at = Airtable(airtable_api_key)


#####

if __name__ == "__main__":
    # Pull in relevant Docker environment variables
    AIRTABLE_API_KEY = os.environ["AIRTABLE_API_KEY"]
    BIGQUERY_APP_CREDS = os.environ["BIGQUERY_APP_CREDS"]
    BIGQUERY_PROJECT_ID = os.environ["BIGQUERY_PROJECT_ID"]
    LOG_LEVEL = os.environ.get("LOG_LEVEL", 20)

    run(
        airtable_api_key=AIRTABLE_API_KEY,
        bigquery_app_creds=BIGQUERY_APP_CREDS,
        bigquery_project_id=BIGQUERY_PROJECT_ID,
        log_level=LOG_LEVEL,
    )
