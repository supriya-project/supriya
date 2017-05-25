# -*- encoding: utf-8 -*-
from supriya.tools.commandlinetools.ProjectPackageScript import ProjectPackageScript


class ManageSynthDefScript(ProjectPackageScript):
    '''
    Manages project package synthdefs.

    ..  shell::

        sjv synthdef --help

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    alias = 'synthdef'
    short_description = 'manage project package synthdefs'

    ### PRIVATE METHODS ###

    def _process_args(self, args):
        pass

    def _setup_argument_parser(self, parser):
        pass
