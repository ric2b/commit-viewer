from typing import Dict
from urllib.parse import ParseResult

import requests

TIMEOUT = 120  # seconds
API_URL = 'https://api.github.com/repos'


def get_commit_list(url_parts: ParseResult) -> Dict[str, str]:
    commits = {}
    next_page = f'{API_URL}{url_parts.path}/commits'
    while next_page:
        response = requests.get(next_page, params={'per_page': 100}, timeout=TIMEOUT)

        if response.status_code == 403:
            raise LookupError(f'Likely rate limited. Message: {response.text}')

        for commit in response.json():
            commits[commit['sha']] = commit['message']

        if 'next' in response.links:
            next_page = response.links['next']['url']
        else:
            break

    return commits
