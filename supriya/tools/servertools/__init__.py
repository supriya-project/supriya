"""
Tools for interacting with and modeling objects on the SuperCollider
**scsynth** synthesis server.
"""
from abjad.tools import systemtools


systemtools.ImportManager.import_structured_package(
    __path__[0],
    globals(),
    )
