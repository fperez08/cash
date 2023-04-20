import os
import argparse
import logging

log = logging.getLogger(__name__)


def memoize(func):
    cache = dict()

    def memoized_func(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    return memoized_func


def get_gmail_params():
    my_parser = argparse.ArgumentParser(allow_abbrev=False)
    my_parser.add_argument("--query", action="store", type=str, required=True)
    my_parser.add_argument("--regex", action="store", type=str, required=True)

    return my_parser.parse_args()


def get_sheets_params():
    my_parser = argparse.ArgumentParser(allow_abbrev=False)
    my_parser.add_argument("--file", action="store", type=str, required=True)
    my_parser.add_argument("--range", action="store", type=str, required=True)

    return my_parser.parse_args()


def env(key: str):
    value = os.environ.get(key)
    if not value:
        raise Exception(f"{key} not found in the environment")
    return value
