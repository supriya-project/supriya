# -*- coding: utf-8 -*-
from abjad.tools import systemtools

systemtools.ImportManager.import_material_packages(
    __path__[0],
    globals(),
    )
