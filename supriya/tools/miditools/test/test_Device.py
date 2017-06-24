from unittest import mock
from abjad.tools import systemtools
from supriya.tools import miditools


class TestCase(systemtools.TestCase):

    def test_init(self):
        device = miditools.Device('Test')
        self.compare_strings(
            device.root_view.debug(),
            """
            <V name=root mode=non_mutex visible=true>
                <LC name=fader_1 mode=continuous pc=track_level_1 value=0.0>
                <LC name=fader_2 mode=continuous pc=track_level_2 value=0.0>
                <LC name=fader_3 mode=continuous pc=master_level value=0.0>
                <LC name=clip_launch_1x1 mode=toggle pc=clip_launch_1x1 value=0.0>
                <LC name=clip_launch_1x2 mode=toggle pc=clip_launch_1x2 value=0.0>
                <LC name=clip_launch_2x1 mode=toggle pc=clip_launch_2x1 value=0.0>
                <LC name=clip_launch_2x2 mode=toggle pc=clip_launch_2x2 value=0.0>
                <V name=outer_mutex mode=mutex visible=true>
                    <LC name=0 mode=toggle pc=clip_stop_a value=1.0>
                    <LC name=1 mode=toggle pc=clip_stop_b value=0.0>
                <V name=outer_modal mode=non_mutex visible=true>
                    <V name=0 mode=non_mutex visible=true>
                        <V name=inner_mutex mode=mutex visible=true>
                            <LC name=0 mode=toggle pc=device_left value=1.0>
                            <LC name=1 mode=toggle pc=device_right value=0.0>
                        <V name=knobs mode=non_mutex visible=true>
                            <V name=0 mode=non_mutex visible=true>
                                <LC name=knob_1 mode=continuous pc=device_control_1 value=0.0>
                                <LC name=knob_2 mode=continuous pc=device_control_2 value=0.0>
                                <LC name=knob_3 mode=continuous pc=device_control_3 value=0.0>
                            <V name=1 mode=non_mutex visible=false>
                                <LC name=knob_1 mode=continuous pc=device_control_1 value=0.0>
                                <LC name=knob_2 mode=continuous pc=device_control_2 value=0.0>
                                <LC name=knob_3 mode=continuous pc=device_control_3 value=0.0>
                    <V name=1 mode=non_mutex visible=false>
                        <V name=inner_mutex mode=mutex visible=true>
                            <LC name=0 mode=toggle pc=device_left value=1.0>
                            <LC name=1 mode=toggle pc=device_right value=0.0>
                        <V name=knobs mode=non_mutex visible=true>
                            <V name=0 mode=non_mutex visible=true>
                                <LC name=knob_1 mode=continuous pc=device_control_1 value=0.0>
                                <LC name=knob_2 mode=continuous pc=device_control_2 value=0.0>
                                <LC name=knob_3 mode=continuous pc=device_control_3 value=0.0>
                            <V name=1 mode=non_mutex visible=false>
                                <LC name=knob_1 mode=continuous pc=device_control_1 value=0.0>
                                <LC name=knob_2 mode=continuous pc=device_control_2 value=0.0>
                                <LC name=knob_3 mode=continuous pc=device_control_3 value=0.0>
            """)
        self.compare_strings(
            device.root_view.debug(only_visible=True),
            """
            <V name=root mode=non_mutex visible=true>
                <LC name=fader_1 mode=continuous pc=track_level_1 value=0.0>
                <LC name=fader_2 mode=continuous pc=track_level_2 value=0.0>
                <LC name=fader_3 mode=continuous pc=master_level value=0.0>
                <LC name=clip_launch_1x1 mode=toggle pc=clip_launch_1x1 value=0.0>
                <LC name=clip_launch_1x2 mode=toggle pc=clip_launch_1x2 value=0.0>
                <LC name=clip_launch_2x1 mode=toggle pc=clip_launch_2x1 value=0.0>
                <LC name=clip_launch_2x2 mode=toggle pc=clip_launch_2x2 value=0.0>
                <V name=outer_mutex mode=mutex visible=true>
                    <LC name=0 mode=toggle pc=clip_stop_a value=1.0>
                    <LC name=1 mode=toggle pc=clip_stop_b value=0.0>
                <V name=outer_modal mode=non_mutex visible=true>
                    <V name=0 mode=non_mutex visible=true>
                        <V name=inner_mutex mode=mutex visible=true>
                            <LC name=0 mode=toggle pc=device_left value=1.0>
                            <LC name=1 mode=toggle pc=device_right value=0.0>
                        <V name=knobs mode=non_mutex visible=true>
                            <V name=0 mode=non_mutex visible=true>
                                <LC name=knob_1 mode=continuous pc=device_control_1 value=0.0>
                                <LC name=knob_2 mode=continuous pc=device_control_2 value=0.0>
                                <LC name=knob_3 mode=continuous pc=device_control_3 value=0.0>
            """)

    def test_physical_manifest_01(self):
        device = miditools.Device('Test')
        message = [0x80, 0x01, 0x7F]
        physical_control, value = device._process_one(message, 0.0)
        assert physical_control.boolean_polarity is None
        assert physical_control.name == 'clip_launch_1x1'
        assert value == 1.0

    def test_physical_manifest_02(self):
        device = miditools.Device('Test')
        message = [0x81, 0x03, 0x00]
        physical_control, value = device._process_one(message, 0.0)
        assert physical_control.boolean_polarity == [0, 127]
        assert physical_control.name == 'clip_stop_b'
        assert value == 1.0

    def test_mutex_01(self):
        device = miditools.Device('Test')
        self.compare_strings(
            device.root_view.debug(only_visible=True),
            """
            <V name=root mode=non_mutex visible=true>
                <LC name=fader_1 mode=continuous pc=track_level_1 value=0.0>
                <LC name=fader_2 mode=continuous pc=track_level_2 value=0.0>
                <LC name=fader_3 mode=continuous pc=master_level value=0.0>
                <LC name=clip_launch_1x1 mode=toggle pc=clip_launch_1x1 value=0.0>
                <LC name=clip_launch_1x2 mode=toggle pc=clip_launch_1x2 value=0.0>
                <LC name=clip_launch_2x1 mode=toggle pc=clip_launch_2x1 value=0.0>
                <LC name=clip_launch_2x2 mode=toggle pc=clip_launch_2x2 value=0.0>
                <V name=outer_mutex mode=mutex visible=true>
                    <LC name=0 mode=toggle pc=clip_stop_a value=1.0>
                    <LC name=1 mode=toggle pc=clip_stop_b value=0.0>
                <V name=outer_modal mode=non_mutex visible=true>
                    <V name=0 mode=non_mutex visible=true>
                        <V name=inner_mutex mode=mutex visible=true>
                            <LC name=0 mode=toggle pc=device_left value=1.0>
                            <LC name=1 mode=toggle pc=device_right value=0.0>
                        <V name=knobs mode=non_mutex visible=true>
                            <V name=0 mode=non_mutex visible=true>
                                <LC name=knob_1 mode=continuous pc=device_control_1 value=0.0>
                                <LC name=knob_2 mode=continuous pc=device_control_2 value=0.0>
                                <LC name=knob_3 mode=continuous pc=device_control_3 value=0.0>
            """)
        with mock.patch.object(device, 'send_message') as send_mock:
            device([0xB0, 0x10, 0x22], 0)
            device([0xB0, 0x11, 0x44], 0)
            device([0xB0, 0x12, 0x66], 0)
        assert sorted(_[0][0] for _ in send_mock.call_args_list) == [
            [0xB0, 0x10, 0x22],
            [0xB0, 0x11, 0x44],
            [0xB0, 0x12, 0x66],
            ]
        self.compare_strings(
            device.root_view.debug(only_visible=True),
            """
            <V name=root mode=non_mutex visible=true>
                <LC name=fader_1 mode=continuous pc=track_level_1 value=0.0>
                <LC name=fader_2 mode=continuous pc=track_level_2 value=0.0>
                <LC name=fader_3 mode=continuous pc=master_level value=0.0>
                <LC name=clip_launch_1x1 mode=toggle pc=clip_launch_1x1 value=0.0>
                <LC name=clip_launch_1x2 mode=toggle pc=clip_launch_1x2 value=0.0>
                <LC name=clip_launch_2x1 mode=toggle pc=clip_launch_2x1 value=0.0>
                <LC name=clip_launch_2x2 mode=toggle pc=clip_launch_2x2 value=0.0>
                <V name=outer_mutex mode=mutex visible=true>
                    <LC name=0 mode=toggle pc=clip_stop_a value=1.0>
                    <LC name=1 mode=toggle pc=clip_stop_b value=0.0>
                <V name=outer_modal mode=non_mutex visible=true>
                    <V name=0 mode=non_mutex visible=true>
                        <V name=inner_mutex mode=mutex visible=true>
                            <LC name=0 mode=toggle pc=device_left value=1.0>
                            <LC name=1 mode=toggle pc=device_right value=0.0>
                        <V name=knobs mode=non_mutex visible=true>
                            <V name=0 mode=non_mutex visible=true>
                                <LC name=knob_1 mode=continuous pc=device_control_1 value=0.267717>
                                <LC name=knob_2 mode=continuous pc=device_control_2 value=0.535433>
                                <LC name=knob_3 mode=continuous pc=device_control_3 value=0.80315>
            """)
        with mock.patch.object(device, 'send_message') as send_mock:
            device([0x81, 0x03, 0x00], 0)
        assert sorted(_[0][0] for _ in send_mock.call_args_list) == [
            [0x80, 0x03, 0x00],
            [0x80, 0x06, 0x00],
            [0x90, 0x05, 0x7F],
            [0x91, 0x03, 0x7F],
            [0xB0, 0x10, 0x00],
            [0xB0, 0x11, 0x00],
            [0xB0, 0x12, 0x00],
            ]
        self.compare_strings(
            device.root_view.debug(only_visible=True),
            """
            <V name=root mode=non_mutex visible=true>
                <LC name=fader_1 mode=continuous pc=track_level_1 value=0.0>
                <LC name=fader_2 mode=continuous pc=track_level_2 value=0.0>
                <LC name=fader_3 mode=continuous pc=master_level value=0.0>
                <LC name=clip_launch_1x1 mode=toggle pc=clip_launch_1x1 value=0.0>
                <LC name=clip_launch_1x2 mode=toggle pc=clip_launch_1x2 value=0.0>
                <LC name=clip_launch_2x1 mode=toggle pc=clip_launch_2x1 value=0.0>
                <LC name=clip_launch_2x2 mode=toggle pc=clip_launch_2x2 value=0.0>
                <V name=outer_mutex mode=mutex visible=true>
                    <LC name=0 mode=toggle pc=clip_stop_a value=0.0>
                    <LC name=1 mode=toggle pc=clip_stop_b value=1.0>
                <V name=outer_modal mode=non_mutex visible=true>
                    <V name=1 mode=non_mutex visible=true>
                        <V name=inner_mutex mode=mutex visible=true>
                            <LC name=0 mode=toggle pc=device_left value=1.0>
                            <LC name=1 mode=toggle pc=device_right value=0.0>
                        <V name=knobs mode=non_mutex visible=true>
                            <V name=0 mode=non_mutex visible=true>
                                <LC name=knob_1 mode=continuous pc=device_control_1 value=0.0>
                                <LC name=knob_2 mode=continuous pc=device_control_2 value=0.0>
                                <LC name=knob_3 mode=continuous pc=device_control_3 value=0.0>
            """)
        with mock.patch.object(device, 'send_message') as send_mock:
            device([0xB0, 0x10, 0x55], 0)
            device([0xB0, 0x11, 0x33], 0)
            device([0xB0, 0x12, 0x11], 0)
        assert sorted(_[0][0] for _ in send_mock.call_args_list) == [
            [0xB0, 0x10, 0x55],
            [0xB0, 0x11, 0x33],
            [0xB0, 0x12, 0x11],
            ]
        self.compare_strings(
            device.root_view.debug(only_visible=True),
            """
            <V name=root mode=non_mutex visible=true>
                <LC name=fader_1 mode=continuous pc=track_level_1 value=0.0>
                <LC name=fader_2 mode=continuous pc=track_level_2 value=0.0>
                <LC name=fader_3 mode=continuous pc=master_level value=0.0>
                <LC name=clip_launch_1x1 mode=toggle pc=clip_launch_1x1 value=0.0>
                <LC name=clip_launch_1x2 mode=toggle pc=clip_launch_1x2 value=0.0>
                <LC name=clip_launch_2x1 mode=toggle pc=clip_launch_2x1 value=0.0>
                <LC name=clip_launch_2x2 mode=toggle pc=clip_launch_2x2 value=0.0>
                <V name=outer_mutex mode=mutex visible=true>
                    <LC name=0 mode=toggle pc=clip_stop_a value=0.0>
                    <LC name=1 mode=toggle pc=clip_stop_b value=1.0>
                <V name=outer_modal mode=non_mutex visible=true>
                    <V name=1 mode=non_mutex visible=true>
                        <V name=inner_mutex mode=mutex visible=true>
                            <LC name=0 mode=toggle pc=device_left value=1.0>
                            <LC name=1 mode=toggle pc=device_right value=0.0>
                        <V name=knobs mode=non_mutex visible=true>
                            <V name=0 mode=non_mutex visible=true>
                                <LC name=knob_1 mode=continuous pc=device_control_1 value=0.669291>
                                <LC name=knob_2 mode=continuous pc=device_control_2 value=0.401575>
                                <LC name=knob_3 mode=continuous pc=device_control_3 value=0.133858>
            """)
        with mock.patch.object(device, 'send_message') as send_mock:
            device([0x80, 0x06, 0x7F], 0)
        assert sorted(_[0][0] for _ in send_mock.call_args_list) == [
            [0x80, 0x05, 0x00],
            [0x90, 0x06, 0x7F],
            [0xB0, 0x10, 0x00],
            [0xB0, 0x11, 0x00],
            [0xB0, 0x12, 0x00]
            ]
        self.compare_strings(
            device.root_view.debug(only_visible=True),
            """
            <V name=root mode=non_mutex visible=true>
                <LC name=fader_1 mode=continuous pc=track_level_1 value=0.0>
                <LC name=fader_2 mode=continuous pc=track_level_2 value=0.0>
                <LC name=fader_3 mode=continuous pc=master_level value=0.0>
                <LC name=clip_launch_1x1 mode=toggle pc=clip_launch_1x1 value=0.0>
                <LC name=clip_launch_1x2 mode=toggle pc=clip_launch_1x2 value=0.0>
                <LC name=clip_launch_2x1 mode=toggle pc=clip_launch_2x1 value=0.0>
                <LC name=clip_launch_2x2 mode=toggle pc=clip_launch_2x2 value=0.0>
                <V name=outer_mutex mode=mutex visible=true>
                    <LC name=0 mode=toggle pc=clip_stop_a value=0.0>
                    <LC name=1 mode=toggle pc=clip_stop_b value=1.0>
                <V name=outer_modal mode=non_mutex visible=true>
                    <V name=1 mode=non_mutex visible=true>
                        <V name=inner_mutex mode=mutex visible=true>
                            <LC name=0 mode=toggle pc=device_left value=0.0>
                            <LC name=1 mode=toggle pc=device_right value=1.0>
                        <V name=knobs mode=non_mutex visible=true>
                            <V name=1 mode=non_mutex visible=true>
                                <LC name=knob_1 mode=continuous pc=device_control_1 value=0.0>
                                <LC name=knob_2 mode=continuous pc=device_control_2 value=0.0>
                                <LC name=knob_3 mode=continuous pc=device_control_3 value=0.0>
            """)
        with mock.patch.object(device, 'send_message') as send_mock:
            device([0x80, 0x03, 0x00], 0)
        assert sorted(_[0][0] for _ in send_mock.call_args_list) == [
            [0x80, 0x06, 0x00],
            [0x81, 0x03, 0x00],
            [0x90, 0x03, 0x7F],
            [0x90, 0x05, 0x7F],
            [0xB0, 0x10, 0x22],
            [0xB0, 0x11, 0x44],
            [0xB0, 0x12, 0x66],
            ]
        self.compare_strings(
            device.root_view.debug(only_visible=True),
            """
            <V name=root mode=non_mutex visible=true>
                <LC name=fader_1 mode=continuous pc=track_level_1 value=0.0>
                <LC name=fader_2 mode=continuous pc=track_level_2 value=0.0>
                <LC name=fader_3 mode=continuous pc=master_level value=0.0>
                <LC name=clip_launch_1x1 mode=toggle pc=clip_launch_1x1 value=0.0>
                <LC name=clip_launch_1x2 mode=toggle pc=clip_launch_1x2 value=0.0>
                <LC name=clip_launch_2x1 mode=toggle pc=clip_launch_2x1 value=0.0>
                <LC name=clip_launch_2x2 mode=toggle pc=clip_launch_2x2 value=0.0>
                <V name=outer_mutex mode=mutex visible=true>
                    <LC name=0 mode=toggle pc=clip_stop_a value=1.0>
                    <LC name=1 mode=toggle pc=clip_stop_b value=0.0>
                <V name=outer_modal mode=non_mutex visible=true>
                    <V name=0 mode=non_mutex visible=true>
                        <V name=inner_mutex mode=mutex visible=true>
                            <LC name=0 mode=toggle pc=device_left value=1.0>
                            <LC name=1 mode=toggle pc=device_right value=0.0>
                        <V name=knobs mode=non_mutex visible=true>
                            <V name=0 mode=non_mutex visible=true>
                                <LC name=knob_1 mode=continuous pc=device_control_1 value=0.267717>
                                <LC name=knob_2 mode=continuous pc=device_control_2 value=0.535433>
                                <LC name=knob_3 mode=continuous pc=device_control_3 value=0.80315>
            """)
