import io
import pytest
import supriya.cli
import uqbar.io
import uqbar.strings


def test():
    string_io = io.StringIO()
    script = supriya.cli.SupriyaScript()
    command = ["--help"]
    with uqbar.io.RedirectedStreams(stdout=string_io), pytest.raises(
        SystemExit
    ) as exception_info:
        script(command)
    assert exception_info.value.code == 0
    pytest.helpers.compare_strings(
        """
        usage: supriya-script [-h] [--version]
                              {help,list,asset,material,project,session,synthdef} ...

        Entry-point to Supriya developer scripts catalog.

        optional arguments:
          -h, --help            show this help message and exit
          --version             show program's version number and exit

        subcommands:
          {help,list,asset,material,project,session,synthdef}
            help                print subcommand help
            list                list subcommands
            asset               manage project package assets
            material            manage project package materials
            project             manage project packages
            session             manage project package sessions
            synthdef            manage project package synthdefs
        """,
        string_io.getvalue(),
    )
