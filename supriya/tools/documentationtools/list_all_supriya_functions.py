# -*- encoding: utf-8 -*-
import os
from abjad.tools import documentationtools


def list_all_supriya_functions():
    r'''Lists all supriya functions.
    '''
    import supriya
    root_path = os.path.join(
        supriya.__path__[0],
        'tools',
        )
    function_crawler = documentationtools.FunctionCrawler(
        code_root=root_path,
        root_package_name='supriya',
        )
    functions = function_crawler()
    functions = sorted(functions, key=lambda x: x.__module__)
    functions = tuple(functions)
    return functions