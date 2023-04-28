import os
import argparse
import logging

log = logging.getLogger(__name__)


def memoize(func):
    """Function to cache the value returned by a function when is called with
    the same parameter

    Args:
        func (function): Function to be executed

    Returns:
        function: The memoized function
    """
    cache = dict()

    def memoized_func(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    return memoized_func


def get_gmail_params():
    """Get the parameters used for the gmail_data script

    Returns:
        dict: A dictionary with the parameters
    """
    my_parser = argparse.ArgumentParser(allow_abbrev=False)
    my_parser.add_argument("--query", action="store", type=str, required=True)
    my_parser.add_argument("--regex", action="store", type=str, required=True)

    return my_parser.parse_args()


def get_sheets_params():
    """Get the parameters used for the sheets_update script

    Returns:
        dict: A dictionary with the parameters
    """
    my_parser = argparse.ArgumentParser(allow_abbrev=False)
    my_parser.add_argument("--file", action="store", type=str, required=True)
    my_parser.add_argument("--range", action="store", type=str, required=True)

    return my_parser.parse_args()


def env(key: str):
    """Helper function to get the value of a env variable,
    raise an exception if the variable is not found.

    Args:
        key (str): Name of the env variable

    Raises:
        Exception: Message to inform the user that the variable was not found

    Returns:
        str: The value of the env variable
    """
    value = os.environ.get(key)
    if not value:
        raise Exception(f"{key} not found in the environment")
    return value
