import logging

from googleapiclient.errors import HttpError
from apis import google_services

log = logging.getLogger(__name__)


def get_ids(max_results: int = None, label_id: str = None, query: str = None):
    try:
        log.info(f"Getting email ids with gmail query: {query}")
        msg_service = google_services.get_gmail_messages()
        results = msg_service.list(
            userId="me",
            labelIds=label_id,
            q=query,
            maxResults=max_results,
        ).execute()
        messages = results.get("messages", [])

        if not messages:
            log.error(f"Messages not found with gmail query: {query}")
            return

        return list(map(lambda m: m["id"], messages))

    except HttpError as error:
        log.error(f"An error occurred: {error}")
        return


def get_raw_content(label_ids: list):
    log.info("Getting emails raw content")
    return list(map(lambda l: get_content(l), label_ids))


def get_content(label_id: int):
    try:
        msg_service = google_services.get_gmail_messages()
        results = msg_service.get(
            userId="me", id=label_id, format="raw"
        ).execute()
        if not results:
            log.error("Message not found")
            return
        return results.get("raw", "")

    except HttpError as error:
        log.error(f"An error occurred: {error}")
        return
