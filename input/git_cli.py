import logging
import os
import shutil
import subprocess
import uuid
from typing import Dict, List

from input.commit import Commit, Person
from input.input_base_class import CommitViewerInput

BASE_REPO_DIR = '.commit_viewer/repos'

# Note: The persistence method used (local bare repo's) isn't safe for concurrency.
# A lockfile is a possible solution if running multiple instances at a time is required.

SHOW_FORMAT = 'sha %H%ntree %T%n' \
              'author_name %an%nauthor_email %ae%nauthor_date %ad%n' \
              'committer_name %cn%ncommitter_email %ce%ncommitter_date %cd%n' \
              'parents %P%n%n%B'


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
    def _parse_git_show(git_show_output: List[str]) -> Commit:
        """
        Parses the output of git show (as a list of strings/lines) with 'fuller' format
        into a dictionary with the commit information and returns it.

        :param git_show_output: the output of git show, as a list of strings (the lines)
        :return: a Commit object
        """
        if len(git_show_output) == 0:
            raise ValueError

        commit_data: Dict[str, str] = {}
        break_line = None
        for line_number, line in enumerate(git_show_output):
            if not line:
                break_line = line_number
                break

            line_parts = line.split(maxsplit=1)
            commit_data[line_parts[0]] = line_parts[1] if len(line_parts) > 1 else ''

        message_lines = [line.lstrip() for line in git_show_output[break_line + 1:]]
        commit_data['message'] = '\n'.join(message_lines)

        commit = Commit(
            sha=commit_data['sha'],
            tree=commit_data['tree'],
            author=Person(
                name=commit_data['author_name'],
                email=commit_data['author_email'],
                date=commit_data['author_date'],
            ),
            committer=Person(
                name=commit_data['committer_name'],
                email=commit_data['committer_email'],
                date=commit_data['committer_date'],
            ),
            message=commit_data['message'],
            parents=commit_data['parents'].split() if commit_data['parents'] else None,
        )

        return commit

    @classmethod
    def get_commit_list(cls, url: str, force_clone: bool=False) -> Dict[str, Commit]:
        """
        Gets a commit list from git log.
        If a local copy doesn't yet exist, it is fetched via git clone --bare.

        :param url: the url of the repo on the remote
        :param force_clone: forces the
        :return: a dictionary with commit hashes as keys and Commit objects as values
        """
        if force_clone or not os.path.isdir(cls._repo_directory(url)):
            cls._fetch_repo(url)

        logging.debug('Getting list of commits from git log')
        git_log_output = subprocess.check_output(
            ['git', 'log', '--full-history', '--no-decorate', '--oneline'],
            cwd=cls._repo_directory(url),
        ).decode('utf-8').splitlines()

        commits = {}
        for line in git_log_output:
            if not line:
                continue

            sha, subject = line.split(maxsplit=1)

            # have to use git show because I didn't find a way to reliably split the
            # output of git log by commit
            git_show_output = subprocess.check_output(
                ['git', 'show', '-s', f'--pretty={SHOW_FORMAT}', '--no-decorate', sha],
                cwd=cls._repo_directory(url),
            ).decode('utf-8').splitlines()

            logging.debug(f'Parsing commit {sha}')
            commits[sha] = cls._parse_git_show(git_show_output)

        return commits
