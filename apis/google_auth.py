import os.path
import logging

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
log = logging.getLogger(__name__)


def get_credentials(credentials_path: str):
    credentials = None

    if not os.path.exists(credentials_path):
        raise FileNotFoundError(f"{credentials_path} file not found")

    if os.path.exists("token.json"):
        log.info("Generating credentials from authorized user file")
        credentials = Credentials.from_authorized_user_file(
            "token.json", SCOPES
        )

    if not credentials or not credentials.valid:
        log.info("Credentials not valid")
        if credentials and credentials.expired and credentials.refresh_token:
            log.info("Credentials expired...token needs to be refreshed")
            credentials.refresh(Request())
        else:
            log.info("Generate credentials")
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES
            )
            credentials = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(credentials.to_json())

    return credentials
