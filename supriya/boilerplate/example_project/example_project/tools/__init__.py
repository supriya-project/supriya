# -*- coding: utf-8 -*-
from abjad.tools import systemtools

systemtools.ImportManager.import_structured_package(
    __path__[0],
    globals(),
    )
