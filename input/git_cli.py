import os
import subprocess
import uuid
from typing import Dict

BASE_REPO_DIR = 'tmp'


def repo_uuid(url: str) -> uuid.UUID:
    return uuid.uuid5(uuid.NAMESPACE_URL, url)


def repo_directory(url: str) -> str:
    return f'{BASE_REPO_DIR}/{repo_uuid(url)}'


def fetch_repo(url: str):
    subprocess.run(['git', 'clone', '--bare', url, repo_directory(url)],
                   stderr=subprocess.DEVNULL, text=True, check=True)


def get_commit_list(url: str) -> Dict[str, str]:
    if not os.path.isdir(repo_directory(url)):
        fetch_repo(url)

    git_log_output = subprocess.check_output(
        ['git', 'log', '--full-history', '--no-decorate', '--oneline'],
        text=True, cwd=repo_directory(url))

    commits = {}
    for line in git_log_output.split('\n'):
        if line:
            commit_hash, subject = line.split(maxsplit=1)
            commits[commit_hash] = subject

    return commits
