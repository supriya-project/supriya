# -*- encoding: utf-8 -*-

r"""
Tools for interacting with supriya via a web browser.
"""

from abjad.tools import systemtools

systemtools.ImportManager.import_structured_package(
    __path__[0],
    globals(),
    )
