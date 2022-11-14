import logging

from googleapiclient.errors import HttpError
from apis import google_client_factory as google_client

log = logging.getLogger(__name__)


def get_id(label_name: str):
    try:
        label_service = google_client.get_gmail_service(
            google_client.GmailResource.labels
        )
        results = label_service.list(userId="me").execute()
        labels = results.get("labels", [])
        if not labels:
            log.error("Labels not found")
            return

        label_found = filter(lambda label: label["name"] == label_name, labels)
        return label_found.__next__()["id"]

    except HttpError as error:
        log.error(f"An error occurred: {error}")
        return
