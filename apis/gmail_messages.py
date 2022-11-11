import logging

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from apis import google_auth as __auth

log = logging.getLogger(__name__)


def get_messages_id(
    max_results: int = 1, label_id: str = None, query: str = None
):
    try:
        creds = __auth.get_credentials()
        service = build("gmail", "v1", credentials=creds)
        results = (
            service.users()
            .messages()
            .list(
                userId="me",
                labelIds=label_id,
                q=query,
                maxResults=max_results,
            )
            .execute()
        )
        messages = results.get("messages", [])

        if not messages:
            log.error("Messages not found")
            return

        return list(map(lambda m: m["id"], messages))

    except HttpError as error:
        log.error(f"An error occurred: {error}")
        return
