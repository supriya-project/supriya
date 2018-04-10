import inspect
import uqbar.cli


class SupriyaScript(uqbar.cli.CLIAggregator):
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

    config_name = '.supriyarc'
    short_description = 'Entry-point to Supriya developer scripts catalog.'

    ### PUBLIC PROPERTIES ###

    @property
    def cli_classes(self):
        from supriya.tools import commandlinetools
        classes = []
        for name in sorted(dir(commandlinetools)):
            obj = getattr(commandlinetools, name)
            if not isinstance(obj, type):
                continue
            elif not issubclass(obj, uqbar.cli.CLI):
                continue
            elif issubclass(obj, type(self)):
                continue
            elif inspect.isabstract(obj):
                continue
            classes.append(obj)
        classes.sort(key=lambda x: x.__name__)
        return classes
