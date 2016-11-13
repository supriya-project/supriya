# -*- encoding: utf-8 -*-
import os
import traceback
from abjad.tools.systemtools.Configuration import Configuration


class SupriyaConfiguration(Configuration):

    def __init__(self):
        Configuration.__init__(self)
        if not os.path.exists(self.output_directory):
            try:
                os.makedirs(self.output_directory)
            except (IOError, OSError):
                traceback.print_exc()

    ### PRIVATE METHODS ###

    def _get_option_definitions(self):
        options = {}
        return options

    ### PRIVATE PROPERTIES ###

    @property
    def _initial_comment(self):
        current_time = self._current_time
        return [
            'Supriya configuration file created on {}.'.format(current_time),
            ]

    ### PUBLIC PROPERTIES ###

    @property
    def configuration_directory_name(self):
        return '.supriya'

    @property
    def configuration_file_name(self):
        return 'supriya.cfg'

    @property
    def output_directory(self):
        return os.path.join(
            self.configuration_directory_path,
            'output'
            )

    @property
    def scsynth_path(self):
        from abjad.tools import systemtools
        scsynth_path = 'scsynth'
        if not systemtools.IOManager.find_executable('scsynth'):
            found_scsynth = False
            for path in (
                '/Applications/SuperCollider/SuperCollider.app/Contents/MacOS/scsynth',  # pre-7
                '/Applications/SuperCollider/SuperCollider.app/Contents/Resources/scsynth',  # post-7
                ):
                if os.path.exists(path):
                    scsynth_path = path
                    found_scsynth = True
            if not found_scsynth:
                raise Exception('Cannot find scsynth. Is it on your $PATH?')
        return scsynth_path
