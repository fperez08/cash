import logging

from apis import gmail_messages as gmessage
from logger import setup_global_logging
from email_content import get_email_data
from utils import get_params

log = logging.getLogger(__name__)
logger_list = [
    logging.getLogger("__main__"),
    logging.getLogger("apis"),
    logging.getLogger("email_content"),
    logging.getLogger("utils"),
]


def main():
    setup_global_logging(level=logging.DEBUG, loggers=logger_list)
    params = get_params()

    messages_id = gmessage.get_ids(query=params.query)
    messages = gmessage.get_raw_content(messages_id)
    result = get_email_data(messages, params.regex)
    log.info(result)


if __name__ == "__main__":
    main()
