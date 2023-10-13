"""
Exercises to demo...

1 -- Updating a Parsons connector in real time
2 -- Using the Docker environment to update the log level
3 -- Using the interactive shell to update environmental variables
"""

import logging
import os
from dev.utils.git_helper import check_parsons_branch
from parsons import Table
from parsons.google.google_bigquery import GoogleBigQuery as BigQuery
from parsons.airtable import Airtable
from parsons.docker_dev.docker_dev import Dev

logger = logging.getLogger(__name__)

##########


def get_airtable_data(airtable: Airtable) -> Table:
    """
    Read target Airtable base and return data in a Parsons table
    """

    return airtable.get_records()


def write_table_to_bigquery(bq: BigQuery, tbl: Table, target_table: str):
    """
    Writes an incoming Parosns table to BigQuery
    """

    logger.debug(f"Writing {tbl.num_rows} rows to {target_table}")
    bq.copy(tbl=tbl, table_name=target_table, if_exists="drop")


def run_airtable_to_bigquery(
    airtable__access_token: str,
    bigquery__app_creds: str,
    bigquery__project_id: str,
    log_level: int = 20,
    airtable__base_key: str = "app45g5Qp3gEN5QFf",
    airtable__table_name: str = "Roster",
    bigquery__target_table: str = "ianferguson_dev.nyk_roster",
):
    # Make sure that the current Parsons branch is set to dev
    check_parsons_branch()

    # Set log level
    # logger.setLevel(level=log_level)

    # Instantiate connectors
    bq = BigQuery(bigquery__app_creds, bigquery__project_id)
    at = Airtable(
        base_key=airtable__base_key,
        table_name=airtable__table_name,
        personal_access_token=airtable__access_token,
    )

    ###

    airtable_data = get_airtable_data(airtable=at)
    write_table_to_bigquery(
        bq=bq, tbl=airtable_data, target_table=bigquery__target_table
    )


#####

if __name__ == "__main__":
    # Pull in relevant Docker environment variables
    AIRTABLE_ACCESS_TOKEN = os.environ["AIRTABLE_ACCESS_TOKEN"]
    BIGQUERY_APP_CREDENTIALS = os.environ["BIGQUERY_APP_CREDENTIALS"]
    BIGQUERY_PROJECT_ID = os.environ["BIGQUERY_PROJECT_ID"]
    LOG_LEVEL = os.environ.get("LOG_LEVEL", 20)

    run_airtable_to_bigquery(
        airtable__access_token=AIRTABLE_ACCESS_TOKEN,
        bigquery__app_creds=BIGQUERY_APP_CREDENTIALS,
        bigquery__project_id=BIGQUERY_PROJECT_ID,
        log_level=LOG_LEVEL,
    )
