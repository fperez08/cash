import argparse
import logging
from datetime import datetime, timedelta

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


def get_params():
    my_parser = argparse.ArgumentParser(allow_abbrev=False)
    my_parser.add_argument("--label", action="store", type=str, required=True)
    my_parser.add_argument("--days", action="store", type=str, required=True)

    args = my_parser.parse_args()
    arguments = args._get_kwargs()
    return arguments[::-1]


def get_gmail_query():
    query = ""
    for param in get_params():
        key, value = param
        if key != "days":
            query = f"{key}:{value} "
        else:
            date_range = get_date_range(int(value))
            query = query + date_range
    log.info(query)
    return query


def get_date_range(days: int):
    date_format = "%Y/%m/%d"
    after = "after:"
    before = "before:"
    current_date = datetime.now()
    after_date = current_date - timedelta(days=days)
    before = before + current_date.date().strftime(date_format)
    after = after + after_date.date().strftime(date_format)
    return after + " " + before
