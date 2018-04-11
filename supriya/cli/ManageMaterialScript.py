from supriya.cli.ProjectSectionScript import ProjectSectionScript


class ManageMaterialScript(ProjectSectionScript):
    '''
    Manages project package materials.

    ::

        sjv material --help

    '''

    ### CLASS VARIABLES ###

    alias = 'material'
    short_description = 'manage project package materials'

    ### PRIVATE PROPERTIES ###

    @property
    def _section_plural(self):
        return 'materials'

    @property
    def _section_singular(self):
        return 'material'
