import argparse

from apis.google_auth import generate_token

if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(allow_abbrev=False)
    my_parser.add_argument("--path", action="store", type=str, required=True)

    args = my_parser.parse_args()
    generate_token("credentials.json", args.path)
