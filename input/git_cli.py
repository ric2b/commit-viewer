import os
import subprocess
import uuid
from typing import Dict

BASE_REPO_DIR = '.commit_viewer/repos'


def _url_uuid(url: str) -> uuid.UUID:
    return uuid.uuid5(uuid.NAMESPACE_URL, url)


def _repo_directory(url: str) -> str:
    return f'{BASE_REPO_DIR}/{_url_uuid(url)}'


def _fetch_repo(url: str):
    """
    Fetched a repo at the given url to a local directory via git clone --bare.
    :param url: the url of the repo on the remote
    """
    subprocess.run(['git', 'clone', '--bare', url, _repo_directory(url)],
                   stderr=subprocess.DEVNULL, check=True)


def get_commit_list(url: str) -> Dict[str, str]:
    """
    Gets a commit list from git log.
    If a local copy doesn't yet exist, it is fetched via git clone --bare.
    :param url: the url of the repo on the remote
    :return: a dictionary with commit hashes as keys and messages as values
    """
    if not os.path.isdir(_repo_directory(url)):
        _fetch_repo(url)

    git_log_output = subprocess.check_output(
        ['git', 'log', '--full-history', '--no-decorate', '--oneline'],
        cwd=_repo_directory(url)
    ).decode('utf-8').split('\n')

    commits = {}
    for line in git_log_output:
        if line:
            # maxsplit=1 to avoid splitting on the message itself
            commit_hash, subject = line.split(maxsplit=1)
            commits[commit_hash] = subject

    return commits
