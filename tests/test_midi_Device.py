import pytest
import supriya.midi
import uqbar.strings
from supriya import Bindable, bind
from unittest import mock


def test___init___01():
    device = supriya.midi.Device('Test')
    assert device.root_view._debug() == uqbar.strings.normalize(
        """
        <V name=root is_mutex=false visible=true>
            <LC name=fader_1 mode=continuous pc=track_level_1 value=0.0>
            <LC name=fader_2 mode=continuous pc=track_level_2 value=0.0>
            <LC name=fader_3 mode=continuous pc=master_level value=0.0>
            <LC name=clip_launch_1x1 mode=toggle pc=clip_launch_1x1 value=0.0>
            <LC name=clip_launch_1x2 mode=toggle pc=clip_launch_1x2 value=0.0>
            <LC name=clip_launch_2x1 mode=toggle pc=clip_launch_2x1 value=0.0>
            <LC name=clip_launch_2x2 mode=toggle pc=clip_launch_2x2 value=0.0>
            <V name=outer_mutex is_mutex=true visible=true>
                <LC name=0 mode=toggle pc=clip_stop_a value=1.0>
                <LC name=1 mode=toggle pc=clip_stop_b value=0.0>
            <V name=outer_modal is_mutex=false visible=true>
                <V name=0 is_mutex=false visible=true>
                    <V name=inner_mutex is_mutex=true visible=true>
                        <LC name=0 mode=toggle pc=device_left value=1.0>
                        <LC name=1 mode=toggle pc=device_right value=0.0>
                    <V name=knobs is_mutex=false visible=true>
                        <V name=0 is_mutex=false visible=true>
                            <LC name=knob_1 mode=continuous pc=device_control_1 value=0.0>
                            <LC name=knob_2 mode=continuous pc=device_control_2 value=0.0>
                            <LC name=knob_3 mode=continuous pc=device_control_3 value=0.0>
                        <V name=1 is_mutex=false visible=false>
                            <LC name=knob_1 mode=continuous pc=device_control_1 value=0.0>
                            <LC name=knob_2 mode=continuous pc=device_control_2 value=0.0>
                            <LC name=knob_3 mode=continuous pc=device_control_3 value=0.0>
                <V name=1 is_mutex=false visible=false>
                    <V name=inner_mutex is_mutex=true visible=true>
                        <LC name=0 mode=toggle pc=device_left value=1.0>
                        <LC name=1 mode=toggle pc=device_right value=0.0>
                    <V name=knobs is_mutex=false visible=true>
                        <V name=0 is_mutex=false visible=true>
                            <LC name=knob_1 mode=continuous pc=device_control_1 value=0.0>
                            <LC name=knob_2 mode=continuous pc=device_control_2 value=0.0>
                            <LC name=knob_3 mode=continuous pc=device_control_3 value=0.0>
                        <V name=1 is_mutex=false visible=false>
                            <LC name=knob_1 mode=continuous pc=device_control_1 value=0.0>
                            <LC name=knob_2 mode=continuous pc=device_control_2 value=0.0>
                            <LC name=knob_3 mode=continuous pc=device_control_3 value=0.0>
        """
    )
    assert device.root_view._debug(only_visible=True) == uqbar.strings.normalize(
        """
        <V name=root is_mutex=false visible=true>
            <LC name=fader_1 mode=continuous pc=track_level_1 value=0.0>
            <LC name=fader_2 mode=continuous pc=track_level_2 value=0.0>
            <LC name=fader_3 mode=continuous pc=master_level value=0.0>
            <LC name=clip_launch_1x1 mode=toggle pc=clip_launch_1x1 value=0.0>
            <LC name=clip_launch_1x2 mode=toggle pc=clip_launch_1x2 value=0.0>
            <LC name=clip_launch_2x1 mode=toggle pc=clip_launch_2x1 value=0.0>
            <LC name=clip_launch_2x2 mode=toggle pc=clip_launch_2x2 value=0.0>
            <V name=outer_mutex is_mutex=true visible=true>
                <LC name=0 mode=toggle pc=clip_stop_a value=1.0>
                <LC name=1 mode=toggle pc=clip_stop_b value=0.0>
            <V name=outer_modal is_mutex=false visible=true>
                <V name=0 is_mutex=false visible=true>
                    <V name=inner_mutex is_mutex=true visible=true>
                        <LC name=0 mode=toggle pc=device_left value=1.0>
                        <LC name=1 mode=toggle pc=device_right value=0.0>
                    <V name=knobs is_mutex=false visible=true>
                        <V name=0 is_mutex=false visible=true>
                            <LC name=knob_1 mode=continuous pc=device_control_1 value=0.0>
                            <LC name=knob_2 mode=continuous pc=device_control_2 value=0.0>
                            <LC name=knob_3 mode=continuous pc=device_control_3 value=0.0>
        """
    )


def test___init___02():
    device_one = supriya.midi.Device('Test')
    manifest = device_one._device_manifest.copy()
    manifest['device'].pop('logical_controls')
    device_two = supriya.midi.Device(manifest)
    assert device_two.root_view._debug() == uqbar.strings.normalize(
        """
        <V name=root is_mutex=false visible=true>
            <LC name=clip_launch_1x1 mode=continuous pc=clip_launch_1x1 value=0.0>
            <LC name=clip_launch_1x2 mode=continuous pc=clip_launch_1x2 value=0.0>
            <LC name=clip_launch_2x1 mode=continuous pc=clip_launch_2x1 value=0.0>
            <LC name=clip_launch_2x2 mode=continuous pc=clip_launch_2x2 value=0.0>
            <LC name=clip_stop_a mode=continuous pc=clip_stop_a value=0.0>
            <LC name=clip_stop_b mode=continuous pc=clip_stop_b value=0.0>
            <LC name=device_control_1 mode=continuous pc=device_control_1 value=0.0>
            <LC name=device_control_2 mode=continuous pc=device_control_2 value=0.0>
            <LC name=device_control_3 mode=continuous pc=device_control_3 value=0.0>
            <LC name=device_left mode=continuous pc=device_left value=0.0>
            <LC name=device_right mode=continuous pc=device_right value=0.0>
            <LC name=track_level_1 mode=continuous pc=track_level_1 value=0.0>
            <LC name=track_level_2 mode=continuous pc=track_level_2 value=0.0>
            <LC name=master_level mode=continuous pc=master_level value=0.0>
        """
    )
    assert device_two.root_view._debug(only_visible=True) == uqbar.strings.normalize(
        """
        <V name=root is_mutex=false visible=true>
            <LC name=clip_launch_1x1 mode=continuous pc=clip_launch_1x1 value=0.0>
            <LC name=clip_launch_1x2 mode=continuous pc=clip_launch_1x2 value=0.0>
            <LC name=clip_launch_2x1 mode=continuous pc=clip_launch_2x1 value=0.0>
            <LC name=clip_launch_2x2 mode=continuous pc=clip_launch_2x2 value=0.0>
            <LC name=clip_stop_a mode=continuous pc=clip_stop_a value=0.0>
            <LC name=clip_stop_b mode=continuous pc=clip_stop_b value=0.0>
            <LC name=device_control_1 mode=continuous pc=device_control_1 value=0.0>
            <LC name=device_control_2 mode=continuous pc=device_control_2 value=0.0>
            <LC name=device_control_3 mode=continuous pc=device_control_3 value=0.0>
            <LC name=device_left mode=continuous pc=device_left value=0.0>
            <LC name=device_right mode=continuous pc=device_right value=0.0>
            <LC name=track_level_1 mode=continuous pc=track_level_1 value=0.0>
            <LC name=track_level_2 mode=continuous pc=track_level_2 value=0.0>
            <LC name=master_level mode=continuous pc=master_level value=0.0>
        """
    )


def test_process_physical_control_01():
    device = supriya.midi.Device('Test')
    message = [0x80, 0x01, 0x7F]
    physical_control, value = device._process_physical_control(message, 0.0)
    assert physical_control.boolean_polarity is None
    assert physical_control.name == 'clip_launch_1x1'
    assert value == 1.0


def test_process_physical_control_02():
    device = supriya.midi.Device('Test')
    message = [0x81, 0x03, 0x00]
    physical_control, value = device._process_physical_control(message, 0.0)
    assert physical_control.boolean_polarity == [0, 127]
    assert physical_control.name == 'clip_stop_b'
    assert value == 1.0


def test_mutex_01():
    device = supriya.midi.Device('Test')
    assert device.root_view._debug(only_visible=True) == uqbar.strings.normalize(
        """
        <V name=root is_mutex=false visible=true>
            <LC name=fader_1 mode=continuous pc=track_level_1 value=0.0>
            <LC name=fader_2 mode=continuous pc=track_level_2 value=0.0>
            <LC name=fader_3 mode=continuous pc=master_level value=0.0>
            <LC name=clip_launch_1x1 mode=toggle pc=clip_launch_1x1 value=0.0>
            <LC name=clip_launch_1x2 mode=toggle pc=clip_launch_1x2 value=0.0>
            <LC name=clip_launch_2x1 mode=toggle pc=clip_launch_2x1 value=0.0>
            <LC name=clip_launch_2x2 mode=toggle pc=clip_launch_2x2 value=0.0>
            <V name=outer_mutex is_mutex=true visible=true>
                <LC name=0 mode=toggle pc=clip_stop_a value=1.0>
                <LC name=1 mode=toggle pc=clip_stop_b value=0.0>
            <V name=outer_modal is_mutex=false visible=true>
                <V name=0 is_mutex=false visible=true>
                    <V name=inner_mutex is_mutex=true visible=true>
                        <LC name=0 mode=toggle pc=device_left value=1.0>
                        <LC name=1 mode=toggle pc=device_right value=0.0>
                    <V name=knobs is_mutex=false visible=true>
                        <V name=0 is_mutex=false visible=true>
                            <LC name=knob_1 mode=continuous pc=device_control_1 value=0.0>
                            <LC name=knob_2 mode=continuous pc=device_control_2 value=0.0>
                            <LC name=knob_3 mode=continuous pc=device_control_3 value=0.0>
        """
    )
    with mock.patch.object(device, 'send_message') as send_mock:
        device([0xB0, 0x10, 0x22], 0)
        device([0xB0, 0x11, 0x44], 0)
        device([0xB0, 0x12, 0x66], 0)
    assert sorted(_[0][0] for _ in send_mock.call_args_list) == [
        [0xB0, 0x10, 0x22],
        [0xB0, 0x11, 0x44],
        [0xB0, 0x12, 0x66],
    ]
    assert device.root_view._debug(only_visible=True) == uqbar.strings.normalize(
        """
        <V name=root is_mutex=false visible=true>
            <LC name=fader_1 mode=continuous pc=track_level_1 value=0.0>
            <LC name=fader_2 mode=continuous pc=track_level_2 value=0.0>
            <LC name=fader_3 mode=continuous pc=master_level value=0.0>
            <LC name=clip_launch_1x1 mode=toggle pc=clip_launch_1x1 value=0.0>
            <LC name=clip_launch_1x2 mode=toggle pc=clip_launch_1x2 value=0.0>
            <LC name=clip_launch_2x1 mode=toggle pc=clip_launch_2x1 value=0.0>
            <LC name=clip_launch_2x2 mode=toggle pc=clip_launch_2x2 value=0.0>
            <V name=outer_mutex is_mutex=true visible=true>
                <LC name=0 mode=toggle pc=clip_stop_a value=1.0>
                <LC name=1 mode=toggle pc=clip_stop_b value=0.0>
            <V name=outer_modal is_mutex=false visible=true>
                <V name=0 is_mutex=false visible=true>
                    <V name=inner_mutex is_mutex=true visible=true>
                        <LC name=0 mode=toggle pc=device_left value=1.0>
                        <LC name=1 mode=toggle pc=device_right value=0.0>
                    <V name=knobs is_mutex=false visible=true>
                        <V name=0 is_mutex=false visible=true>
                            <LC name=knob_1 mode=continuous pc=device_control_1 value=0.267717>
                            <LC name=knob_2 mode=continuous pc=device_control_2 value=0.535433>
                            <LC name=knob_3 mode=continuous pc=device_control_3 value=0.80315>
        """
    )
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
    assert device.root_view._debug(only_visible=True) == uqbar.strings.normalize(
        """
        <V name=root is_mutex=false visible=true>
            <LC name=fader_1 mode=continuous pc=track_level_1 value=0.0>
            <LC name=fader_2 mode=continuous pc=track_level_2 value=0.0>
            <LC name=fader_3 mode=continuous pc=master_level value=0.0>
            <LC name=clip_launch_1x1 mode=toggle pc=clip_launch_1x1 value=0.0>
            <LC name=clip_launch_1x2 mode=toggle pc=clip_launch_1x2 value=0.0>
            <LC name=clip_launch_2x1 mode=toggle pc=clip_launch_2x1 value=0.0>
            <LC name=clip_launch_2x2 mode=toggle pc=clip_launch_2x2 value=0.0>
            <V name=outer_mutex is_mutex=true visible=true>
                <LC name=0 mode=toggle pc=clip_stop_a value=0.0>
                <LC name=1 mode=toggle pc=clip_stop_b value=1.0>
            <V name=outer_modal is_mutex=false visible=true>
                <V name=1 is_mutex=false visible=true>
                    <V name=inner_mutex is_mutex=true visible=true>
                        <LC name=0 mode=toggle pc=device_left value=1.0>
                        <LC name=1 mode=toggle pc=device_right value=0.0>
                    <V name=knobs is_mutex=false visible=true>
                        <V name=0 is_mutex=false visible=true>
                            <LC name=knob_1 mode=continuous pc=device_control_1 value=0.0>
                            <LC name=knob_2 mode=continuous pc=device_control_2 value=0.0>
                            <LC name=knob_3 mode=continuous pc=device_control_3 value=0.0>
        """
    )
    with mock.patch.object(device, 'send_message') as send_mock:
        device([0xB0, 0x10, 0x55], 0)
        device([0xB0, 0x11, 0x33], 0)
        device([0xB0, 0x12, 0x11], 0)
    assert sorted(_[0][0] for _ in send_mock.call_args_list) == [
        [0xB0, 0x10, 0x55],
        [0xB0, 0x11, 0x33],
        [0xB0, 0x12, 0x11],
    ]
    assert device.root_view._debug(only_visible=True) == uqbar.strings.normalize(
        """
        <V name=root is_mutex=false visible=true>
            <LC name=fader_1 mode=continuous pc=track_level_1 value=0.0>
            <LC name=fader_2 mode=continuous pc=track_level_2 value=0.0>
            <LC name=fader_3 mode=continuous pc=master_level value=0.0>
            <LC name=clip_launch_1x1 mode=toggle pc=clip_launch_1x1 value=0.0>
            <LC name=clip_launch_1x2 mode=toggle pc=clip_launch_1x2 value=0.0>
            <LC name=clip_launch_2x1 mode=toggle pc=clip_launch_2x1 value=0.0>
            <LC name=clip_launch_2x2 mode=toggle pc=clip_launch_2x2 value=0.0>
            <V name=outer_mutex is_mutex=true visible=true>
                <LC name=0 mode=toggle pc=clip_stop_a value=0.0>
                <LC name=1 mode=toggle pc=clip_stop_b value=1.0>
            <V name=outer_modal is_mutex=false visible=true>
                <V name=1 is_mutex=false visible=true>
                    <V name=inner_mutex is_mutex=true visible=true>
                        <LC name=0 mode=toggle pc=device_left value=1.0>
                        <LC name=1 mode=toggle pc=device_right value=0.0>
                    <V name=knobs is_mutex=false visible=true>
                        <V name=0 is_mutex=false visible=true>
                            <LC name=knob_1 mode=continuous pc=device_control_1 value=0.669291>
                            <LC name=knob_2 mode=continuous pc=device_control_2 value=0.401575>
                            <LC name=knob_3 mode=continuous pc=device_control_3 value=0.133858>
        """
    )
    with mock.patch.object(device, 'send_message') as send_mock:
        device([0x80, 0x06, 0x7F], 0)
    assert sorted(_[0][0] for _ in send_mock.call_args_list) == [
        [0x80, 0x05, 0x00],
        [0x90, 0x06, 0x7F],
        [0xB0, 0x10, 0x00],
        [0xB0, 0x11, 0x00],
        [0xB0, 0x12, 0x00],
    ]
    assert device.root_view._debug(only_visible=True) == uqbar.strings.normalize(
        """
        <V name=root is_mutex=false visible=true>
            <LC name=fader_1 mode=continuous pc=track_level_1 value=0.0>
            <LC name=fader_2 mode=continuous pc=track_level_2 value=0.0>
            <LC name=fader_3 mode=continuous pc=master_level value=0.0>
            <LC name=clip_launch_1x1 mode=toggle pc=clip_launch_1x1 value=0.0>
            <LC name=clip_launch_1x2 mode=toggle pc=clip_launch_1x2 value=0.0>
            <LC name=clip_launch_2x1 mode=toggle pc=clip_launch_2x1 value=0.0>
            <LC name=clip_launch_2x2 mode=toggle pc=clip_launch_2x2 value=0.0>
            <V name=outer_mutex is_mutex=true visible=true>
                <LC name=0 mode=toggle pc=clip_stop_a value=0.0>
                <LC name=1 mode=toggle pc=clip_stop_b value=1.0>
            <V name=outer_modal is_mutex=false visible=true>
                <V name=1 is_mutex=false visible=true>
                    <V name=inner_mutex is_mutex=true visible=true>
                        <LC name=0 mode=toggle pc=device_left value=0.0>
                        <LC name=1 mode=toggle pc=device_right value=1.0>
                    <V name=knobs is_mutex=false visible=true>
                        <V name=1 is_mutex=false visible=true>
                            <LC name=knob_1 mode=continuous pc=device_control_1 value=0.0>
                            <LC name=knob_2 mode=continuous pc=device_control_2 value=0.0>
                            <LC name=knob_3 mode=continuous pc=device_control_3 value=0.0>
        """
    )
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
    assert device.root_view._debug(only_visible=True) == uqbar.strings.normalize(
        """
        <V name=root is_mutex=false visible=true>
            <LC name=fader_1 mode=continuous pc=track_level_1 value=0.0>
            <LC name=fader_2 mode=continuous pc=track_level_2 value=0.0>
            <LC name=fader_3 mode=continuous pc=master_level value=0.0>
            <LC name=clip_launch_1x1 mode=toggle pc=clip_launch_1x1 value=0.0>
            <LC name=clip_launch_1x2 mode=toggle pc=clip_launch_1x2 value=0.0>
            <LC name=clip_launch_2x1 mode=toggle pc=clip_launch_2x1 value=0.0>
            <LC name=clip_launch_2x2 mode=toggle pc=clip_launch_2x2 value=0.0>
            <V name=outer_mutex is_mutex=true visible=true>
                <LC name=0 mode=toggle pc=clip_stop_a value=1.0>
                <LC name=1 mode=toggle pc=clip_stop_b value=0.0>
            <V name=outer_modal is_mutex=false visible=true>
                <V name=0 is_mutex=false visible=true>
                    <V name=inner_mutex is_mutex=true visible=true>
                        <LC name=0 mode=toggle pc=device_left value=1.0>
                        <LC name=1 mode=toggle pc=device_right value=0.0>
                    <V name=knobs is_mutex=false visible=true>
                        <V name=0 is_mutex=false visible=true>
                            <LC name=knob_1 mode=continuous pc=device_control_1 value=0.267717>
                            <LC name=knob_2 mode=continuous pc=device_control_2 value=0.535433>
                            <LC name=knob_3 mode=continuous pc=device_control_3 value=0.80315>
        """
    )


@pytest.mark.skip
def test_bind_01():
    class TestClass:
        def __init__(self):
            self.value = 0

        def __call__(self, value):  # noqa
            self.value = value
            return value

    class_ = TestClass()
    device = supriya.midi.Device('Test')
    control = device['clip_launch_1x1']
    bind(control, class_)
    control(1)
    assert control.value == 1.0
    assert class_.value == 1.0
    control(0)
    assert control.value == 0.0
    assert class_.value == 0.0
    class_(1)
    assert control.value == 0.0
    assert class_.value == 1.0


def test_bind_02():
    class TestClass:
        def __init__(self):
            self.value = 0

        @Bindable(rebroadcast=True)  # noqa
        def __call__(self, value):
            self.value = value
            return value

    class_ = TestClass()
    device = supriya.midi.Device('Test')
    control = device['clip_launch_1x1']
    bind(control, class_)
    control(1)
    assert control.value == 1.0
    assert class_.value == 1.0
    control(0)
    assert control.value == 0.0
    assert class_.value == 0.0
    class_(1)
    assert control.value == 1.0
    assert class_.value == 1.0
