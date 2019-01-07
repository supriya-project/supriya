import collections
import copy
import pathlib

import uqbar.strings
import yaml


class ProjectSettings(collections.Mapping):

    ### CLASS VARIABLES ###

    __slots__ = ("_settings",)

    ### INITIALIZER ###

    def __init__(self, yaml_path="project-settings.yml"):
        try:
            with open(str(yaml_path), "r") as file_pointer:
                self._settings = yaml.load(file_pointer.read())
        except Exception:
            self._settings = {}

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        item = self._settings[item]
        return copy.deepcopy(item)

    def __iter__(self):
        for key in self._settings:
            yield key

    def __len__(self):
        return len(self._settings)

    ### PUBLIC METHODS ###

    @classmethod
    def from_dummy_data(cls):
        dummy_data = yaml.load(
            uqbar.strings.normalize(
                """
        composer:
            email: josiah.oberholtzer@gmail.com
            github: josiah-wolf-oberholtzer
            name: Josiah Wolf Oberholtzer
            website: https://www.josiahwolfoberholtzer.com
        server_options:
            audio_bus_channel_count: 128
            block_size: 64
            buffer_count: 1024
            control_bus_channel_count: 4096
            hardware_buffer_size: null
            initial_node_id: 1000
            input_bus_channel_count: 8
            input_device: null
            input_stream_mask: false
            load_synthdefs: true
            maximum_node_count: 1024
            maximum_synthdef_count: 1024
            memory_locking: false
            memory_size: 8192
            output_bus_channel_count: 8
            output_device: null
            output_stream_mask: false
            protocol: udp
            random_number_generator_count: 64
            remote_control_volume: false
            restricted_path: null
            sample_rate: null
            verbosity: 0
            wire_buffer_count: 64
            zero_configuration: false
        title: Test Project
        """
            )
        )
        project_settings = cls()
        project_settings._settings = dummy_data
        return project_settings

    @classmethod
    def from_python_module(cls, path):
        path = pathlib.Path(path).parent / "project-settings.yml"
        return cls(path)
