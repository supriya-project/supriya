# -*- encoding: utf-8 -*-
from abjad.tools import documentationtools


def list_all_supriya_classes(bases=None):
    """
    Lists all supriya classes.
    """
    classes = documentationtools.list_all_classes(modules='supriya.tools')
    if bases:
        classes = tuple(_ for _ in classes if issubclass(_, bases))
    classes = sorted(classes, key=lambda x: x.__module__)
    classes = tuple(classes)
    return classes
