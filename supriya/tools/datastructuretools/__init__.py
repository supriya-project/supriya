"""
Tools for working with generic datastructures.
"""
from abjad.tools import systemtools


systemtools.ImportManager.import_structured_package(
    __path__[0],
    globals(),
    )
