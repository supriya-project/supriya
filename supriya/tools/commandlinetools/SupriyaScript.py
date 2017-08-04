import inspect
from abjad.tools.commandlinetools import AbjDevScript


class SupriyaScript(AbjDevScript):
    '''`SupriyaScript` is the commandline entry-point to the Supriya
    developer scripts catalog.

    Can be accessed on the commandline via `ajv`:

    ..  shell::

        surpiya --help

    `supriya` supports subcommands similar to `svn`:

    ..  shell::

        supriya project --help

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    short_description = 'Entry-point to Supriya developer scripts catalog.'

    ### PUBLIC PROPERTIES ###

    @property
    def commandline_script_classes(self):
        from abjad.tools import commandlinetools as abjad_commandlinetools
        from supriya.tools import commandlinetools
        classes = []
        for name in sorted(dir(commandlinetools)):
            obj = getattr(commandlinetools, name)
            if not isinstance(obj, type):
                continue
            elif not issubclass(obj, abjad_commandlinetools.CommandlineScript):
                continue
            elif issubclass(obj, type(self)):
                continue
            elif inspect.isabstract(obj):
                continue
            classes.append(obj)
        classes.sort(key=lambda x: x.__name__)
        return classes
