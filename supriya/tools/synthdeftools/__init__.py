"""
Tools for constructing and compiling synthesizer definitions (SynthDefs).
"""
from abjad.tools import systemtools


systemtools.ImportManager.import_structured_package(
    __path__[0],
    globals(),
    )
