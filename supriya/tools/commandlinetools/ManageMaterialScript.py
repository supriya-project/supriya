# -*- encoding: utf-8 -*-
from supriya.tools.commandlinetools.ProjectPackageScript import ProjectPackageScript


class ManageMaterialScript(ProjectPackageScript):
    '''
    Manages project package materials.

    ..  shell::

        spv material --help

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    alias = 'material'
    short_description = 'manage project package materials'

    ### PRIVATE METHODS ###

    def _process_args(self, args):
        pass

    def _setup_argument_parser(self, parser):
        pass
