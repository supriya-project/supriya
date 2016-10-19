# -*- encoding: utf-8 -*-
import sys


def run_supriya_web():
    r"""
    Runs Supriya with web-server.

    Returns none.
    """
    from abjad.tools import systemtools

    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = ''

    commands = (
        "from supriya import *;",
        "server = Server();",
        "server.debug_osc = True;",
        "server.boot();",
        "server.meters.allocate();",
        "web_server = webguitools.WebServer(server);",
        "web_server.start();",
        )
    commands = ' '.join(commands)

    command = r""" python -i {} -c '{}'"""
    command = command.format(file_name, commands)
    systemtools.IOManager.spawn_subprocess(command)
