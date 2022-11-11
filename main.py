import logging

from apis import gmail_labels as glabels
from logger import setup_global_logging

log = logging.getLogger(__name__)
logger_list = [logging.getLogger("__main__"), logging.getLogger("apis")]


def main():
    setup_global_logging(level=logging.DEBUG, loggers=logger_list)
    label_id = glabels.get_id("Python")
    log.info(label_id)


if __name__ == "__main__":
    main()
