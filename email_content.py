import email
import base64
import re
import logging

log = logging.getLogger(__name__)


def decode_message(content: str):
    """Decode the mail message using the URL- and filesystem-safe Base64 alphabet.

    Args:
        content (str): Email message content

    Returns:
        bytes: Message decoded in bytes
    """
    return base64.urlsafe_b64decode(content)


def get_content(message: bytes, content_type: str = ""):
    """Extract the content of the mail based on the given content type

    Args:
        message (bytes): Email message in bytes
        content_type (str, optional): The content type of the email message. Defaults to "".

    Returns:
        str: Email content
    """
    msg = email.message_from_bytes(message)
    payload = msg.get_payload()
    if isinstance(payload, list) and content_type:
        for content in payload:
            if content.get_content_type() == content_type:
                return content.get_payload()

    else:
        return payload


def get_data(text_message: str, regex: str):
    """Extract the data of the email message using a regex expression

    Args:
        text_message (str): Email content
        regex (str): Regex expression

    Returns:
        list: The data that matches with the regex
    """
    return re.findall(regex, text_message)


def get_email_data(messages: list, regex: str):
    """Extract the data of a list of email content

    Args:
        messages (list): List of email content
        regex (str): Regex expression to extract the data

    Returns:
        list: List of data extracted from the emails
    """
    log.info("Getting data from the emails")
    messages_decoded = list(map(lambda m: decode_message(m), messages))
    messages_content = list(map(lambda m: get_content(m), messages_decoded))
    return list(map(lambda m: get_data(m, regex), messages_content))
