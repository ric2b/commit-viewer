from abc import ABC, abstractmethod


class CommitViewerInput(ABC):
    @classmethod
    @abstractmethod
    def get_commit_list(cls, url):
        raise NotImplementedError
