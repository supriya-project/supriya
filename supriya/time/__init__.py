"""
Tools for modeling overlapping time structures with timespans.
"""
from .Interval import Interval  # noqa
from .IntervalTree import IntervalTree  # noqa
from .IntervalTreeDriver import IntervalTreeDriver  # noqa
from .Moment import Moment  # noqa

try:
    from .IntervalTreeDriverEx import IntervalTreeDriverEx  # noqa
except ModuleNotFoundError:
    pass
