import logging
import re
import enum
import json

from googleapiclient.errors import HttpError
from apis import google_services

log = logging.getLogger(__name__)


class SheetAction(enum.Enum):
    update = 0
    append = 1


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


def __get_range(start_point: str, rows_number: int):
    result = re.search("[0-9]", start_point)
    if result:
        return start_point + str(rows_number + (int(result.group()) - 1))
    else:
        log.error(f"Number not found in: {start_point}")
        return


def __get_next_range(start_point: str):
    result = re.search("[a-zA-Z]+([0-9]+):[a-zA-Z]+([0-9]+)", start_point)
    if result:
        start_row, end_row = result.groups()
        next_row = int(end_row) + 1
        return start_point.replace(start_row, str(next_row)).replace(
            end_row, ""
        )
    else:
        log.error(f"Number not found in: {start_point}")
        return


def append_values(spreadsheet_id: str, range: str, values: list):
    try:
        sheets = google_services.get_spreadsheet().values()
        body = {"values": values}
        table_size = __get_range(range, len(values))
        response = sheets.append(
            spreadsheetId=spreadsheet_id,
            range=table_size,
            body=body,
            valueInputOption="USER_ENTERED",
        ).execute()
        log.info("Data appended successfully")
        return response

    except HttpError as error:
        log.error(f"An error occurred: {error}")
        return


def save_data(spreadsheet_id: str, values: list):
    target_sheets = []

    with open("spreadsheets_config.json", "r") as json_data_file:
        target_sheets = json.load(json_data_file)

    for index, sheet in enumerate(target_sheets):
        if sheet["action"] == SheetAction.append.name:
            response = append_values(
                spreadsheet_id=spreadsheet_id,
                range=sheet["target"],
                values=values,
            )
            target_sheets[index]["target"] = __get_next_range(
                response["updates"]["updatedRange"]
            )
            with open("spreadsheets_config.json", "w") as out_file:
                json.dump(target_sheets, out_file)
        elif sheet["action"] == SheetAction.update.name:
            update_values(
                spreadsheet_id=spreadsheet_id,
                range=sheet["target"],
                values=values,
            )
        else:
            log.error(f"Invalid action: {sheet['action']}")
