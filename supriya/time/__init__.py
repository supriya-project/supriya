"""
Tools for modeling overlapping time structures with timespans.
"""
from .TimespanCollection import TimespanCollection  # noqa
from .TimespanCollectionDriver import TimespanCollectionDriver  # noqa
from .TimespanSimultaneity import TimespanSimultaneity  # noqa

try:
    from .TimespanCollectionDriverEx import TimespanCollectionDriverEx  # noqa
except ModuleNotFoundError:
    pass
