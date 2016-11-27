# -*- encoding: utf-8 -*-
from supriya.tools.commandlinetools.ProjectPackageScript import ProjectPackageScript


class ManageCompositeScript(ProjectPackageScript):
    '''
    Manages project package composites.

    ..  shell::

        spv composite --help

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    alias = 'composite'
    short_description = 'manage project package composites'

    ### PRIVATE METHODS ###

    def _process_args(self, args):
        pass

    def _setup_argument_parser(self, parser):
        pass
