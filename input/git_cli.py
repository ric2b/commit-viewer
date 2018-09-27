import os
import shutil
import subprocess
import uuid
from typing import Dict, Any, List

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

    @staticmethod
    def _parse_git_show(git_show_output: List[str]) -> Dict[str, str]:
        """
        Parses the output of git show (as a list of strings/lines) with 'fuller' format
        into a dictionary with the commit information and returns it.

        :param git_show_output: the output of git show, as a list of strings (the lines)
        :return: a dictionary with the commit information
        """
        if len(git_show_output) == 0:
            raise ValueError

        commit: Dict[str, str] = {}
        break_line = None
        for line_number, line in enumerate(git_show_output):
            if not line:
                break_line = line_number
                break

            line_parts = line.split(maxsplit=1)
            commit[line_parts[0].rstrip(':')] = line_parts[1]

        message_lines = [line.lstrip() for line in git_show_output[break_line + 1:]]
        commit['Message'] = '\n'.join(message_lines)

        return commit

    @classmethod
    def get_commit_list(cls, url: str, force_clone: bool=False) -> Dict[str, Dict[str, str]]:
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
        ).decode('utf-8').splitlines()

        commits = {}
        for line in git_log_output:
            if not line:
                continue

            # maxsplit=1 to avoid splitting on the message itself
            commit_hash, subject = line.split(maxsplit=1)

            git_show_output = subprocess.check_output(
                ['git', 'show', '-s', '--pretty=fuller', '--no-decorate', commit_hash],
                cwd=cls._repo_directory(url)
            ).decode('utf-8').splitlines()

            commits[commit_hash] = cls._parse_git_show(git_show_output)

        return commits
