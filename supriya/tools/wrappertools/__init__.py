# -*- encoding: utf-8 -*-

"""
Third-party command-line wrappers.
"""

from abjad.tools import systemtools

systemtools.ImportManager.import_structured_package(
    __path__[0],
    globals(),
    )
