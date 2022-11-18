import logging

from apis import gmail_messages as gmessage, google_sheets as sheets
from logger import setup_global_logging
from email_content import get_email_data

log = logging.getLogger(__name__)
logger_list = [
    logging.getLogger("__main__"),
    logging.getLogger("apis"),
]

withdrawal_query = "label:withdrawal  after:2022/11/8 before:2022/11/23"
regexs = [
    r"\$.+M.N.",
    r"[0-9]{4}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} \w{2}",
]
document_id = "19isFSGeTYZavZI2PyDcvNcG8_v38SifEFTXapzntV3M"


def main():
    setup_global_logging(level=logging.DEBUG, loggers=logger_list)
    messages_id = gmessage.get_ids(query=withdrawal_query)
    messages = gmessage.get_raw_content(messages_id)
    result = get_email_data(messages, regexs)
    sheets.save_data(spreadsheet_id=document_id, values=result)


if __name__ == "__main__":
    main()
