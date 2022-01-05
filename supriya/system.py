import abc
import fnmatch
import os
from typing import List, Union

import uqbar.objects

import supriya


def _search(pattern: str, root_path: str):
    search_path, pattern = os.path.split(pattern)
    search_path = os.path.expanduser(search_path)
    if not search_path:
        search_path = os.path.join(root_path, "assets")
    elif not os.path.isabs(search_path):
        search_path = os.path.join(root_path, "assets", search_path)
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


class SupriyaObject(metaclass=abc.ABCMeta):
    """
    Abstract base class from which many custom classes inherit.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __repr__(self):
        return uqbar.objects.get_repr(self, multiline=True)


class SupriyaValueObject(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        return uqbar.objects.new(self)

    def __eq__(self, expr):
        self_values = type(self), uqbar.objects.get_vars(self)
        try:
            expr_values = type(expr), uqbar.objects.get_vars(expr)
        except AttributeError:
            expr_values = type(expr), expr
        return self_values == expr_values

    def __hash__(self):
        args, var_args, kwargs = uqbar.objects.get_vars(self)
        hash_values = [type(self)]
        hash_values.append(tuple(args.items()))
        hash_values.append(tuple(var_args))
        hash_values.append(tuple(sorted(kwargs.items())))
        return hash(tuple(hash_values))
