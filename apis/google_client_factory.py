import logging
import enum

from googleapiclient.discovery import build
from apis import google_auth as __auth
from utils import memoize

log = logging.getLogger(__name__)
memoize_auth = memoize(__auth.get_credentials)


class GmailResource(enum.Enum):
    labels = 0
    messages = 1


def get_gmail_service(
    resource: GmailResource,
    service_name: str = "gmail",
    version: str = "v1",
):
    creds = memoize_auth("credentials.json")
    service = build(service_name, version, credentials=creds).users()

    if resource.name == GmailResource.labels.name:
        return service.labels()
    elif resource.name == GmailResource.messages.name:
        return service.messages()
    else:
        log.error(f"Incorrect gmail resource: {resource.name}")
        return
