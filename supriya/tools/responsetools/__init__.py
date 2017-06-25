"""
Tools for object-modeling OSC responses received from **scsynth**.
"""
from abjad.tools import systemtools


systemtools.ImportManager.import_structured_package(
    __path__[0],
    globals(),
    )
