# -*- encoding: utf-8 -*-


def run_sjv():
    r'''Entry point for setuptools.

    One-line wrapper around SupriyaDevScript.
    '''
    from supriya.tools import commandlinetools
    commandlinetools.SupriyaDevScript()()
