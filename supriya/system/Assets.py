import abc
import fnmatch
import os
import supriya
from typing import List, Union


def _search(pattern: str, root_path: str):
    search_path, pattern = os.path.split(pattern)
    search_path = os.path.expanduser(search_path)
    if not search_path:
        search_path = os.path.join(root_path, 'assets')
    elif not os.path.isabs(search_path):
        search_path = os.path.join(root_path, 'assets', search_path)
    result: List[str] = []
    result = os.listdir(search_path)
    result = fnmatch.filter(result, pattern)
    result = [os.path.join(search_path, _) for _ in result]
    if len(result) == 1:
        return result[0]
    return result


class _AssetsMeta(abc.ABCMeta):

    root_path: str = supriya.__path__[0]  # type: ignore

    def __getitem__(self, pattern) -> Union[str, List[str]]:
        return _search(pattern, self.root_path)


class Assets(metaclass=_AssetsMeta):
    def __init__(self, root_path: str) -> None:
        self.root_path = root_path

    def __getitem__(self, pattern) -> Union[str, List[str]]:
        return _search(pattern, self.root_path)
