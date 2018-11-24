import inspect

import uqbar.cli


class SupriyaScript(uqbar.cli.CLIAggregator):
    """`SupriyaScript` is the commandline entry-point to the Supriya
    developer scripts catalog.

    Can be accessed on the commandline via `ajv`:

    ::

        surpiya --help

    `supriya` supports subcommands similar to `svn`:

    ::

        supriya project --help

    """

    ### CLASS VARIABLES ###

    config_name = ".supriyarc"
    short_description = "Entry-point to Supriya developer scripts catalog."

    ### PUBLIC PROPERTIES ###

    @property
    def cli_classes(self):
        import supriya.cli

        classes = []
        for name in sorted(dir(supriya.cli)):
            obj = getattr(supriya.cli, name)
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
