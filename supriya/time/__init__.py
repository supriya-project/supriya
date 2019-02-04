"""
Tools for modeling overlapping time structures with timespans.
"""
from .TimespanCollection import TimespanCollection  # noqa
from .TimespanCollectionDriver import TimespanCollectionDriver  # noqa
try:
    from .TimespanCollectionDriverEx import TimespanCollectionDriverEx  # noqa, type: ignore
except ModuleNotFoundError:
    pass
from .TimespanSimultaneity import TimespanSimultaneity  # noqa
