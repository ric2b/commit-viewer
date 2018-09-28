from dataclasses import dataclass, field
from typing import List


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
