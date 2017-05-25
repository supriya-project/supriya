# -*- encoding: utf-8 -*-
from supriya.tools.commandlinetools.ProjectPackageScript import ProjectPackageScript


class ManageSessionScript(ProjectPackageScript):
    '''
    Manages project package sessions.

    ..  shell::

        sjv session --help

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    alias = 'session'
    short_description = 'manage project package sessions'

    ### PRIVATE METHODS ###

    def _process_args(self, args):
        pass

    def _setup_argument_parser(self, parser):
        pass
