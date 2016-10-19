# -*- encoding: utf-8 -*-

r"""
Tools for sending, receiving and responding to MIDI messages.
"""

from abjad.tools import systemtools

systemtools.ImportManager.import_structured_package(
    __path__[0],
    globals(),
    )
