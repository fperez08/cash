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
    """Creates the google messages services

    Args:
        service_name (str, optional): Name of the google service. Defaults to "gmail".
        version (str, optional): Version of the google service. Defaults to "v1".

    Returns:
        Any: Resource object to interact with the service
    """
    creds = memoize_auth("credentials.json")
    service = build(service_name, version, credentials=creds).users()
    return service.messages()


def get_spreadsheet(service_name: str = "sheets", version: str = "v4"):
    """Creates the google spreadsheets service

    Args:
        service_name (str, optional): Name of the google service. Defaults to "sheets".
        version (str, optional): Version of the service. Defaults to "v4".

    Returns:
        Any: Resource object to interact with the service
    """
    creds = memoize_auth(f"credentials.json")
    return build(service_name, version, credentials=creds).spreadsheets()
