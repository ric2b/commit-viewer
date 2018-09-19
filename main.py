#!/usr/bin/python3.7
from urllib.parse import urlparse

from input import git_cli, github_api

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Fetch a github repo's commit list.")
    parser.add_argument(dest='url', type=str, help='the url of the github repo')
    args = parser.parse_args()

    url_parts = urlparse(args.url)
    if not all([url_parts.scheme, url_parts.netloc, url_parts.path]):
        raise ValueError('Invalid url, please double check it.')

    try:
        # todo: actually test it (rate-limited right now)
        commit_list = github_api.get_commit_list(url_parts)
    except Exception as e:
        print(e)
        commit_list = git_cli.get_commit_list(args.url)

    for item in commit_list.items():
        print(f'{item[0]} {item[1]}')
