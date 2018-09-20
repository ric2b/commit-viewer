from typing import Dict
from urllib.parse import ParseResult

import requests

API_URL = 'https://api.github.com/repos'


def get_commit_list(url_parts: ParseResult, timeout: int) -> Dict[str, str]:
    """
    Fetches a repo's commit list via the GitHub API

    The url domain isn't checked to allow usage on other (future?) valid github domains.
    ("Be liberal in what you accept from others (...)")

    :param url_parts: a parsed url of a GitHub repo
    :param timeout: optional argument for the timeout on each request
    :return: a dictionary with commit hashes as keys and messages as values
    """
    commits = {}
    next_page = f'{API_URL}{url_parts.path}/commits'
    while next_page:
        response = requests.get(next_page, params={'per_page': 100}, timeout=timeout)
        if response.status_code == 403:
            raise LookupError(f'Likely rate limited. Message: {response.text}')

        for commit in response.json():
            commits[commit['sha']] = commit['commit']['message']

        if 'next' in response.links:
            next_page = response.links['next']['url']
        else:
            break

    return commits
