import logging

from googleapiclient.discovery import build
from apis import google_auth as __auth
from utils import memoize

log = logging.getLogger(__name__)
memoize_auth = memoize(__auth.get_credentials)


def get_gmail_messages(
    service_name: str = "gmail",
    version: str = "v1",
):
    creds = memoize_auth("credentials.json")
    service = build(service_name, version, credentials=creds).users()
    return service.messages()


def get_spreadsheet(service_name: str = "sheets", version: str = "v4"):
    creds = memoize_auth("credentials.json")
    return build(service_name, version, credentials=creds).spreadsheets()
