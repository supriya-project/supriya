from supriya import system

system.ImportManager.import_structured_package(
    __path__[0],
    globals(),
    )
