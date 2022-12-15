import os
import logging

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from utils import env


SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/spreadsheets",
]
log = logging.getLogger(__name__)


def get_credentials(credentials_path: str):
    credentials = None

    if not os.path.exists(credentials_path):
        raise FileNotFoundError(f"{credentials_path} file not found")

    if os.path.exists(f"{env('TOKEN_PATH')}/token.json"):
        log.info("Generating credentials from authorized user file")
        credentials = Credentials.from_authorized_user_file(
            f"{env('TOKEN_PATH')}/token.json", SCOPES
        )

    if not credentials or not credentials.valid:
        log.info("Credentials not valid")
        if credentials and credentials.expired and credentials.refresh_token:
            log.info("Credentials expired...token needs to be refreshed")
            credentials.refresh(Request())
        else:
            if os.path.exists(f"{env('TOKEN_PATH')}/token.json"):
                os.remove(f"{env('TOKEN_PATH')}/token.json")
            raise Exception(
                "Token expired create a new one by running python3 auth_token.py"
            )

    return credentials


def generate_token(credentials_path: str):
    print("Generating auth token...please follow the instructions")
    flow = Flow.from_client_secrets_file(
        credentials_path,
        scopes=SCOPES,
        redirect_uri="urn:ietf:wg:oauth:2.0:oob",
    )
    auth_url, _ = flow.authorization_url(prompt="consent")
    print("Please go to this URL: {}".format(auth_url))

    code = input("Enter the authorization code: ")
    flow.fetch_token(code=code)

    with open("token.json", "w") as token:
        token.write(flow.credentials.to_json())
