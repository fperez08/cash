import logging
import re

from googleapiclient.errors import HttpError
from apis import google_services

log = logging.getLogger(__name__)


def update_values(spreadsheet_id: str, range: str, values: list):
    try:
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


def __get_range(start_point: str, rows_number):
    result = re.search("[0-9]", start_point)
    if result:
        return start_point + str(rows_number + (int(result.group()) - 1))
    else:
        log.error(f"Number not found in: {start_point}")
