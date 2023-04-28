import logging
import re

from googleapiclient.errors import HttpError
from apis import google_services

log = logging.getLogger(__name__)


def update_values(spreadsheet_id: str, range: str, values: list):
    """Update the Google spreed sheet with the given value

    Args:
        spreadsheet_id (str): Id of the spreed sheet
        range (str): Table range
        values (list): List of values to save in the spreed sheet
    """
    try:
        log.info("Updating sheet values...")
        sheets = google_services.get_spreadsheet().values()
        body = {"values": values}
        table_size = __get_range(range, len(values))
        sheets.update(
            spreadsheetId=spreadsheet_id,
            range=table_size,
            body=body,
            valueInputOption="USER_ENTERED",
        ).execute()
        log.info("Sheet updated successfully")

    except HttpError as error:
        log.error(f"An error occurred: {error}")
        return


def __get_range(start_point: str, rows_number: int):
    """Helper function to determine the end of the range where the data is going to be saved

    Args:
        start_point (str): Point in the document where the first value will be placed,
        for example: A1
        rows_number (int): The number of rows that is going to be updated

    Returns:
        str: The range where the data is going to be placed, for example: A1:B5
    """
    result = re.search("[0-9]+", start_point)
    if result:
        return start_point + str(rows_number + (int(result.group()) - 1))
    else:
        log.error(f"Number not found in: {start_point}")
        return
