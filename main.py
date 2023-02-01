import logging
import json

from apis import gmail_messages as gmessage
from logger import setup_global_logging
from email_content import get_email_data
from utils import get_gmail_query

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
    with open("cash_config.json", "r") as json_data_file:
        config = json.load(json_data_file)
        messages_id = gmessage.get_ids(query=withdrawal_query)
        messages = gmessage.get_raw_content(messages_id)
        result = get_email_data(messages, config["email"]["search_patterns"])
        log.info(result)
    # if os.path.exists("token.json"):
    #    os.remove("token.json")


if __name__ == "__main__":
    main()
