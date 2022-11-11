import logging

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from apis import google_auth as __auth

log = logging.getLogger(__name__)


def get_id(label_name: str):
    try:
        print(__package__)
        creds = __auth.get_credentials()
        service = build("gmail", "v1", credentials=creds)
        results = service.users().labels().list(userId="me").execute()
        labels = results.get("labels", [])
        if not labels:
            log.error("Labels not found")
            return

        label_found = filter(lambda label: label["name"] == label_name, labels)
        return label_found.__next__()

    except HttpError as error:
        log.error(f"An error occurred: {error}")
        return
