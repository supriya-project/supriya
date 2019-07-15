"""
Tools for modeling overlapping time structures with timespans.
"""
from .IntervalTree import IntervalTree  # noqa
from .IntervalTreeDriver import IntervalTreeDriver  # noqa
from .TimespanSimultaneity import TimespanSimultaneity  # noqa

try:
    from .IntervalTreeDriverEx import IntervalTreeDriverEx  # noqa
except ModuleNotFoundError:
    pass
