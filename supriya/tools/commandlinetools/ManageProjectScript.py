# -*- encoding: utf-8 -*-
from supriya.tools.commandlinetools.ProjectPackageScript import ProjectPackageScript


class ManageProjectScript(ProjectPackageScript):
    '''
    Manages project packages.

    ..  shell::

        spv project --help

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    alias = 'project'
    short_description = 'manage project packages'

    ### PRIVATE METHODS ###

    def _process_args(self, args):
        pass

    def _setup_argument_parser(self, parser):
        pass
