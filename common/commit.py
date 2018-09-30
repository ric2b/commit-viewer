from dataclasses import dataclass, field, asdict
from pprint import pprint
from typing import List, Dict


@dataclass(frozen=True)
class Person:
    name: str
    email: str
    date: str


@dataclass(frozen=True)
class Commit:
    sha: str
    tree: str
    author: Person
    committer: Person
    message: str

    parents: List[str] = field(default_factory=list)


def pprint_commit_list(commit_list: Dict[str, Commit]):
    pprint({sha: asdict(commit) for sha, commit in commit_list.items()})
