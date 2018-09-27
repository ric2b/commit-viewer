from dataclasses import dataclass, field, asdict
from typing import List


@dataclass(frozen=True)
class Person:
    name: str
    email: str
    date: str

    def __repr__(self):
        return asdict(self).__repr__()


@dataclass(frozen=True)
class Commit:
    sha: str
    tree: str
    author: Person
    committer: Person
    message: str

    parents: List[str] = field(default_factory=list)
