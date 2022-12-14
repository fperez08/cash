import logging
import json
import os

from apis import gmail_messages as gmessage, google_sheets as sheets
from logger import setup_global_logging
from email_content import get_email_data
from utils import get_gmail_query, env

log = logging.getLogger(__name__)
logger_list = [
    logging.getLogger("__main__"),
    logging.getLogger("apis"),
    logging.getLogger("email_content"),
    logging.getLogger("utils"),
]


def main():
    setup_global_logging(level=logging.DEBUG, loggers=logger_list)
    withdrawal_query = get_gmail_query()
    with open(f"{env('CONFIG_PATH')}/cash_config.json", "r") as json_data_file:
        config = json.load(json_data_file)
        messages_id = gmessage.get_ids(query=withdrawal_query)
        messages = gmessage.get_raw_content(messages_id)
        result = get_email_data(messages, config["email"]["search_patterns"])
        sheets.update_values(
            spreadsheet_id=config["sheets"]["document_id"],
            range=config["sheets"]["table_range"],
            values=result,
        )
    if os.path.exists("token.json"):
        os.remove("token.json")


if __name__ == "__main__":
    main()
