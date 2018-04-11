import supriya.cli
import supriya.nonrealtime
from nonrealtimetools_testbase import TestCase


class TestCase(TestCase):

    def test_01(self):
        project_settings = supriya.cli.ProjectSettings.from_dummy_data()
        assert project_settings['server_options']['input_bus_channel_count'] == 8
        assert project_settings['server_options']['output_bus_channel_count'] == 8
        session = supriya.nonrealtime.Session.from_project_settings(project_settings)
        assert session.options.input_bus_channel_count == 8
        assert session.options.output_bus_channel_count == 8

    def test_02(self):
        project_settings = supriya.cli.ProjectSettings.from_dummy_data()
        project_settings._settings['server_options'].update(
            input_bus_channel_count=0,
            output_bus_channel_count=2,
            )
        session = supriya.nonrealtime.Session.from_project_settings(project_settings)
        assert session.options.input_bus_channel_count == 0
        assert session.options.output_bus_channel_count == 2
