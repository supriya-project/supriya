# -*- encoding: utf-8 -*-
from abjad.tools import systemtools


systemtools.ImportManager.import_nominative_modules(
    __path__[0],
    globals(),
    )

from supriya.synthdefs.system_synthdefs import *
