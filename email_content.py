import email
import base64
import re
import logging

log = logging.getLogger(__name__)


def decode_message(content: str):
    return base64.urlsafe_b64decode(content)


def get_content(message: bytes, content_type: str = ""):
    msg = email.message_from_bytes(message)
    payload = msg.get_payload()
    if isinstance(payload, list) and content_type:
        for content in payload:
            if content.get_content_type() == content_type:
                return content.get_payload()

    else:
        return payload


def get_data(text_message: str, regex: str):
    result = re.findall(regex, text_message)
    return result


def get_email_data(messages: list, regex: str):
    log.info("Getting data from the emails")
    messages_decoded = list(map(lambda m: decode_message(m), messages))
    messages_content = list(map(lambda m: get_content(m), messages_decoded))
    return list(map(lambda m: get_data(m, regex), messages_content))
