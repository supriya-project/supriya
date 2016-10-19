# -*- encoding: utf-8 -*-

r"""
Tools for modeling overlapping time structures with timespans.
"""

from abjad.tools import systemtools

systemtools.ImportManager.import_structured_package(
    __path__[0],
    globals(),
    )
