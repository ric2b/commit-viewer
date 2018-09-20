#!/usr/bin/python3.7
from urllib.parse import urlparse
import logging

from input import git_cli, github_api


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Fetch a github repo's commit list.")
    parser.add_argument(dest='url', type=str, help='the url of the github repo')
    parser.add_argument('--log', type=str, default='WARNING', help='logger level')
    parser.add_argument('--timeout', type=int, default=120, help='request timeout (sec)')
    args = parser.parse_args()

    logging.basicConfig(level=args.log.upper())

    url_parts = urlparse(args.url)
    if not all([url_parts.scheme, url_parts.netloc, url_parts.path]):
        raise ValueError('Invalid url, please double check it.')

    try:
        logging.info('Fetching via GitHub API')
        commit_list = github_api.get_commit_list(url_parts, args.timeout)
    except Exception as e:
        logging.info('Failed to fetch from GitHub API, trying git CLI')
        commit_list = git_cli.get_commit_list(args.url)

    for item in commit_list.items():
        print(f'{item[0]} {item[1]}')
