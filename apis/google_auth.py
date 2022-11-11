import os.path
import logging

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
log = logging.getLogger(__name__)


def get_credentials():
    credentials = None

    if os.path.exists("token.json"):
        log.info("Generating credentials from authorized user file")
        credentials = Credentials.from_authorized_user_file(
            "token.json", SCOPES
        )

    if not credentials or not credentials.valid:
        log.info(f"Credentials valid: ${credentials.valid}")
        if credentials and credentials.expired and credentials.refresh_token:
            log.info(f"Credentials expired: {credentials.expired}")
            log.info("Token needs to be refreshed")
            credentials.refresh(Request())
        else:
            log.info("Generate credentials")
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            credentials = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(credentials.to_json())

    return credentials
