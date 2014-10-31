# -*- encoding: utf-8 -*-
import os
from abjad.tools import documentationtools


def list_all_supriya_classes(bases=None):
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
    if bases:
        classes = tuple(_ for _ in classes if issubclass(_, bases))
    classes = sorted(classes, key=lambda x: x.__module__)
    classes = tuple(classes)
    return classes