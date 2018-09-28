import json
import os
from dataclasses import asdict
from typing import Dict

from common import helpers
from common.commit import Commit

CACHE_DIR = '.commit_viewer/cache'


def persist_commit_list(url: str, commit_list: Dict[str, Commit]):
    if not os.path.isdir(CACHE_DIR):
        os.mkdir(CACHE_DIR)

    with open(f'{CACHE_DIR}/{helpers.url_uuid(url)}.json', 'w') as file:
        # for unsupported classes, try to convert to dict
        json.dump(commit_list, file, default=lambda obj: asdict(obj))


def get_from_cache(url: str) -> Dict[str, Commit]:
    with open(f'{CACHE_DIR}/{helpers.url_uuid(url)}.json', 'r') as file:
        return json.load(file)
