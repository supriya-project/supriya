"""
Tools for modeling overlapping time structures with timespans.
"""
from .Interval import Interval
from .IntervalTree import IntervalTree
from .IntervalTreeDriver import IntervalTreeDriver  # noqa
from .Moment import Moment

try:
    from .IntervalTreeDriverEx import IntervalTreeDriverEx  # noqa
except ModuleNotFoundError:
    pass

__all__ = ["Interval", "IntervalTree", "Moment"]
