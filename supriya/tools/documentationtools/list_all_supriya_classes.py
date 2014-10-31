# -*- encoding: utf-8 -*-
import os
from abjad.tools import documentationtools


def list_all_supriya_classes():
    r'''Lists all supriya classes.
    '''
    import supriya
    root_path = os.path.join(
        supriya.__path__[0],
        'tools',
        )
    class_crawler = documentationtools.ClassCrawler(
        code_root=root_path,
        root_package_name='supriya',
        )
    classes = class_crawler()
    return classes
