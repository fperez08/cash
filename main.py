import logging

from apis import gmail_labels as glabels, gmail_messages as gmessage
from logger import setup_global_logging

log = logging.getLogger(__name__)
logger_list = [logging.getLogger("__main__"), logging.getLogger("apis")]


def main():
    setup_global_logging(level=logging.DEBUG, loggers=logger_list)
    label = glabels.get_id("Python")
    messages_id = gmessage.get_ids(max_results=2, label_id=label)
    gmessage.get_raw_content(messages_id)


if __name__ == "__main__":
    main()
