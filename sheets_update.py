import logging
import csv

from apis import google_sheets as sheet
from logger import setup_global_logging
from utils import get_sheets_params, env

log = logging.getLogger(__name__)
logger_list = [
    logging.getLogger("__main__"),
    logging.getLogger("apis"),
    logging.getLogger("email_content"),
    logging.getLogger("utils"),
]


def main():
    setup_global_logging(level=logging.DEBUG, loggers=logger_list)
    params = get_sheets_params()
    document_id = env("DOCUMENT_ID")
    with open(params.file, "r") as file:
        reader = csv.reader(file)
        data = [row for row in reader]
        sheet.update_values(document_id, params.range, data)


if __name__ == "__main__":
    main()
