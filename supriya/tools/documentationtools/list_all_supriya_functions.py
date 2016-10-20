# -*- encoding: utf-8 -*-
from abjad.tools import documentationtools


def list_all_supriya_functions():
    """
    Lists all supriya functions.
    """
    functions = documentationtools.list_all_functions(modules='supriya.tools')
    functions = sorted(functions, key=lambda x: x.__module__)
    functions = tuple(functions)
    return functions
