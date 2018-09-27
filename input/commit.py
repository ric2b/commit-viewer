from dataclasses import dataclass, field
from typing import List


@dataclass
class Person:
    name: str
    email: str
    date: str


@dataclass
class Commit:
    sha: str
    tree: str
    author: Person
    committer: Person
    message: str

    parents: List[str] = field(default=list)
