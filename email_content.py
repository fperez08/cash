import email
import base64
import re


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
    result = re.search(regex, text_message)
    if result:
        return result.groups()
    else:
        return result
