"""
Exercises to demo...

1 -- Updating a Parsons connector in real time
2 -- Using the Docker environment to update the log level
3 -- Using the interactive shell to update environmental variables

Link to Airtable base: https://airtable.com/app45g5Qp3gEN5QFf/tblQlADbbgtQLsFJu/viwTTgsZ5nKMzOK0z?blocks=hide
"""


import os
import logging
from time import sleep
from dev.utils.git_helper import check_parsons_branch
from dev.utils.dev_logger import logger
from parsons import Table
from parsons.google.google_bigquery import GoogleBigQuery as BigQuery
from parsons.airtable import Airtable
from parsons.docker_dev.docker_dev import Dev

logging.getLogger("parsons.google.google_cloud_storage").setLevel(logging.WARNING)

##########


def get_airtable_data(airtable: Airtable) -> Table:
    """
    Read target Airtable base and return data in a Parsons table
    """

    base_data = airtable.get_records()

    # Forgive my PETL wrongdoings
    data = Table(base_data.unpack_list("College"))

    transform_columns = [
        "id",
        "created_time",
        "birth_date",
        "country",
        "exp",
        "ht",
        "no",
        "player",
        "pos",
        "wt",
        "college_0",
        "college_1",
    ]

    # Transformations
    data.match_columns(transform_columns, fuzzy_match=True)
    data.rename_column("exp", "experience")  # Experience
    data.rename_column("ht", "height")  # Height
    data.rename_column("wt", "weight")  # Weight
    data.rename_column("no", "number")  # Number
    data.rename_column("pos", "position")  # Position

    return data


def write_table_to_bigquery(bq: BigQuery, tbl: Table, target_table: str):
    """
    Writes an incoming Parosns table to BigQuery
    """

    logger.debug(f"Writing {tbl.num_rows} rows to {target_table}")
    logger.debug(f"Columns: {', '.join([x for x in tbl.columns])}")
    resp = bq.copy(tbl=tbl, table_name=target_table, if_exists="drop")


def run_airtable_to_bigquery(
    airtable__access_token: str,
    bigquery__app_creds: str,
    bigquery__project_id: str,
    airtable__base_key: str = "app45g5Qp3gEN5QFf",
    airtable__table_name: str = "Roster",
    bigquery__target_table: str = "ianferguson_dev.nyk_roster",
    secret_message: str = None,
    dev: bool = False,
):
    logger.info(f"Running in dev: {dev}")
    if dev:
        logger.setLevel(level=logging.DEBUG)
        bigquery__target_table = f"{bigquery__target_table}__dev"
        logger.debug(f"Target table updated to {bigquery__target_table}...")

    # Make sure that the current Parsons branch is set to dev
    check_parsons_branch()
    logger.debug("Parsons branch confirmed")

    if secret_message:
        logger.info(secret_message)
        sleep(10)

    # Instantiate connectors
    logger.debug("Setting up BigQuery connector...")
    bq = BigQuery(bigquery__app_creds, bigquery__project_id)

    logger.debug("Setting up Airtable connector...")
    at = Airtable(
        base_key=airtable__base_key,
        table_name=airtable__table_name,
        personal_access_token=airtable__access_token,
    )

    ###

    # Query Airtable base
    airtable_data = get_airtable_data(airtable=at)

    # Apply live updates from docker dev connector
    docker_connector = Dev(tbl=airtable_data)
    airtable_data = docker_connector.run()

    # Write table to BigQuery
    write_table_to_bigquery(
        bq=bq, tbl=airtable_data, target_table=bigquery__target_table
    )

    logger.info(f"Successfully wrote to {bigquery__target_table}")


#####

if __name__ == "__main__":
    # Pull in relevant Docker environment variables
    AIRTABLE_ACCESS_TOKEN = os.environ["AIRTABLE_ACCESS_TOKEN"]
    BIGQUERY_APP_CREDENTIALS = os.environ["BIGQUERY_APP_CREDENTIALS"]
    BIGQUERY_PROJECT_ID = os.environ["BIGQUERY_PROJECT_ID"]
    DEV = os.environ["DEV"].upper() == "TRUE"
    SECRET_MESSAGE = os.environ.get("SECRET_MESSAGE")

    run_airtable_to_bigquery(
        airtable__access_token=AIRTABLE_ACCESS_TOKEN,
        bigquery__app_creds=BIGQUERY_APP_CREDENTIALS,
        bigquery__project_id=BIGQUERY_PROJECT_ID,
        secret_message=SECRET_MESSAGE,
        dev=DEV,
    )
