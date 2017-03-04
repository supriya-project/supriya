# -*- encoding: utf-8 -*-

"""
Tools for modeling overlapping time structures with timespans.
"""

from abjad.tools import systemtools
from supriya.tools.timetools.TimespanCollectionDriverEx import TimespanCollectionDriverEx

systemtools.ImportManager.import_structured_package(
    __path__[0],
    globals(),
    )
