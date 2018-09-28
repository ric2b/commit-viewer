from abc import ABC, abstractmethod
from typing import Dict

from common.commit import Commit


class CommitViewerInput(ABC):
    @classmethod
    @abstractmethod
    def get_commit_list(cls, url) -> Dict[str, Commit]:
        raise NotImplementedError
