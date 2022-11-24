import argparse


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
            query = query + value
    return query
