import logging

from apis import gmail_labels as glabels, gmail_messages as gmessage
from logger import setup_global_logging

log = logging.getLogger(__name__)
logger_list = [logging.getLogger("__main__"), logging.getLogger("apis")]


def main():
    setup_global_logging(level=logging.DEBUG, loggers=logger_list)
    label = glabels.get_id("Python")
    messages = gmessage.get_messages_id(max_results=2, label_id=label)
    log.info(messages)


if __name__ == "__main__":
    main()
