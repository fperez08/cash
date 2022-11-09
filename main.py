from apis import gmail_labels as glabels
from logger import __get_logger

log = __get_logger(__name__)


def main():
    label_id = glabels.get_id("Python")
    print(label_id)


if __name__ == "__main__":
    main()
