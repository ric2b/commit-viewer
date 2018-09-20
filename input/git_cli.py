import os
import shutil
import subprocess
import uuid
from typing import Dict

from input.input_base_class import CommitViewerInput

BASE_REPO_DIR = '.commit_viewer/repos'

# todo: The persistence method used (local bare repo's) isn't safe for concurrency.
# A lockfile is a possible solution if running multiple instances at a time is required.


class GitCliInput(CommitViewerInput):
    @staticmethod
    def _url_uuid(url: str) -> uuid.UUID:
        return uuid.uuid5(uuid.NAMESPACE_URL, url)

    @classmethod
    def _repo_directory(cls, url: str) -> str:
        return f'{BASE_REPO_DIR}/{cls._url_uuid(url)}'

    @classmethod
    def _fetch_repo(cls, url: str, clean_dir: bool=False):
        """
        Fetched a repo at the given url to a local directory via git clone --bare.
        :param url: the url of the repo on the remote
        """
        if clean_dir:
            shutil.rmtree(cls._repo_directory(url))

        subprocess.run(['git', 'clone', '--bare', url, cls._repo_directory(url)],
                       stderr=subprocess.DEVNULL, check=True)

    @classmethod
    def get_commit_list(cls, url: str, force_clone: bool=False) -> Dict[str, str]:
        """
        Gets a commit list from git log.
        If a local copy doesn't yet exist, it is fetched via git clone --bare.
        :param url: the url of the repo on the remote
        :param force_clone: forces the
        :return: a dictionary with commit hashes as keys and messages as values
        """
        if force_clone or not os.path.isdir(cls._repo_directory(url)):
            cls._fetch_repo(url)

        git_log_output = subprocess.check_output(
            ['git', 'log', '--full-history', '--no-decorate', '--oneline'],
            cwd=cls._repo_directory(url)
        ).decode('utf-8').split('\n')

        commits = {}
        for line in git_log_output:
            if line:
                # maxsplit=1 to avoid splitting on the message itself
                commit_hash, subject = line.split(maxsplit=1)
                commits[commit_hash] = subject

        return commits
