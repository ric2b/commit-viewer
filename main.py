#!/usr/bin/python3.7
from urllib.parse import urlparse
import logging

from input.git_cli import GitCliInput
from input.github_api import GitHubInput

if __name__ == '__main__':
    import argparse

    # configuration of the CLI for the project
    parser = argparse.ArgumentParser(description="Fetch a github repo's commit list.")
    parser.add_argument(dest='url', type=str, help='the url of the github repo')
    parser.add_argument('--log', type=str, default='WARNING', help='logger level',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
    parser.add_argument('--timeout', type=int, default=120, help='request timeout (sec)')
    parser.add_argument('--input', type=str, help='force input', choices=['github', 'git'])
    args = parser.parse_args()

    logging.basicConfig(level=args.log)

    url_parts = urlparse(args.url)
    if not all([url_parts.scheme, url_parts.netloc, url_parts.path]):
        raise ValueError('Invalid url, please double check it.')

    if args.input == 'github':
        logging.info('Fetching via GitHub API')
        commit_list = GitHubInput.get_commit_list(url_parts, args.timeout)

    elif args.input == 'git':
        logging.info('Fetching via git CLI')
        commit_list = GitCliInput.get_commit_list(args.url)

    else:
        logging.info('Default input: Fetching via GitHub API and falling back to git CLI')
        try:
            commit_list = GitHubInput.get_commit_list(url_parts, args.timeout)
        except Exception as e:
            logging.warning('Failed to fetch from GitHub API, trying git CLI')
            commit_list = GitCliInput.get_commit_list(args.url)

    for item in commit_list.items():
        print(f'{item[0]} {item[1]}')
