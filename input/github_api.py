import logging
from typing import Dict
from urllib.parse import urlparse

import requests

from input.commit import Commit, Person
from input.input_base_class import CommitViewerInput

API_URL = 'https://api.github.com/repos'


class GitHubInput(CommitViewerInput):
    @classmethod
    def get_commit_list(cls, url: str, timeout: int=120) -> Dict[str, Commit]:
        """
        Fetches a repo's commit list via the GitHub API

        The domain isn't checked to allow usage on other (future?) valid github domains.
        ("Be liberal in what you accept from others (...)")

        :param url: a url of a GitHub repo
        :param timeout: optional argument for the timeout on each request
        :return: a dictionary with commit hashes as keys and Commit objects as values
        """
        url_parts = urlparse(url)

        commits = {}
        next_page = f'{API_URL}{url_parts.path}/commits'
        while next_page:
            logging.debug(f'Fetching page {next_page}')
            response = requests.get(next_page, params={'per_page': 100}, timeout=timeout)

            if response.status_code == 403:
                raise LookupError(f'Likely rate limited. Message: {response.text}')

            for entry in response.json():
                logging.debug(f"Parsing commit {entry['sha']}")

                commit = Commit(
                    sha=entry['sha'],
                    tree=entry['commit']['tree']['sha'],
                    author=Person(
                        name=entry['commit']['author']['name'],
                        email=entry['commit']['author']['email'],
                        date=entry['commit']['author']['date'],
                    ),
                    committer=Person(
                        name=entry['commit']['committer']['name'],
                        email=entry['commit']['committer']['email'],
                        date=entry['commit']['committer']['date'],
                    ),
                    message=entry['commit']['message'],
                    parents=[parent['sha'] for parent in entry['parents']],
                )

                commits[commit.sha] = commit

            if 'next' in response.links:
                next_page = response.links['next']['url']
            else:
                break

        return commits
