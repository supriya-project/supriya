from abjad.tools import systemtools as abjad_systemtools


abjad_systemtools.ImportManager.import_structured_package(
    __path__[0],
    globals(),
    delete_systemtools=False,
    )
del(abjad_systemtools)
