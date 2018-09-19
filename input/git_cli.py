import shutil
import subprocess
import uuid
from typing import Dict

BASE_REPO_DIR = 'tmp'


def get_commit_list(url: str, timeout=120) -> Dict[str, str]:
    git_directory = f'{BASE_REPO_DIR}/{uuid.uuid5(uuid.NAMESPACE_URL, url)}'
    try:
        subprocess.run(['git', 'clone', '--bare', url, git_directory],
                       stderr=subprocess.DEVNULL, text=True, check=True)
        git_log_output = subprocess.check_output(
            ['git', 'log', '--full-history', '--no-decorate', '--oneline'],
            text=True, cwd=git_directory)
    except:
        exit()  # Abort on any error problem with git
    finally:
        shutil.rmtree(git_directory)

    commits = {}
    for line in git_log_output.split('\n'):
        if line:
            commit_hash, subject = line.split(maxsplit=1)
            commits[commit_hash] = subject

    return commits
