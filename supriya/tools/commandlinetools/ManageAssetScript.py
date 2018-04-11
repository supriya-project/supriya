from supriya.tools.commandlinetools.ProjectPackageScript import ProjectPackageScript


class ManageAssetScript(ProjectPackageScript):
    '''
    Manages project package assets.

    ::

        sjv asset --help

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    alias = 'asset'
    short_description = 'manage project package assets'

    ### PRIVATE METHODS ###

    def _process_args(self, args):
        pass

    def _setup_argument_parser(self, parser):
        pass
