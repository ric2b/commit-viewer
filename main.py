#!/usr/bin/python3.7
from urllib.parse import urlparse

from input.git_cli import get_commit_list

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Fetch a github repo's commit list.")
    parser.add_argument(dest='url', type=str, help='the url of the github repo')
    args = parser.parse_args()

    url_parts = urlparse(args.url)
    if not all([url_parts.scheme, url_parts.netloc, url_parts.path]):
        print(url_parts)
        raise ValueError('Invalid url, please double check it.')

    for item in get_commit_list(args.url).items():
        print(f'{item[0]} {item[1]}')
