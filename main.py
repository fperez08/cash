import logging

from apis import gmail_labels as glabels, gmail_messages as gmessage
from logger import setup_global_logging
from email_content import decode_message, get_content, get_data

log = logging.getLogger(__name__)
logger_list = [
    logging.getLogger("__main__"),
    logging.getLogger("apis"),
]


def main():
    setup_global_logging(level=logging.DEBUG, loggers=logger_list)
    label = glabels.get_id("Withdrawal")
    messages_id = gmessage.get_ids(max_results=2, label_id=label)
    messages = gmessage.get_raw_content(messages_id)
    message_decoded = decode_message(messages[0])
    content = get_content(message_decoded)
    data = get_data(content, r"<b>\$(.+)<\/b>")
    log.info(data)


if __name__ == "__main__":
    main()
