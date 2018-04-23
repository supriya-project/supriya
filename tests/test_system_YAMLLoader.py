import yaml
import pathlib
import supriya
import uqbar.strings


base_path = pathlib.Path(supriya.__path__[0]) / 'assets' / 'devices'


def test_01():
    path = base_path / 'Test.yml'
    manifest = supriya.system.YAMLLoader.load(path)
    assert yaml.dump(
        manifest,
        default_flow_style=False,
        indent=4
        ) == uqbar.strings.normalize("""
        device:
            defaults:
                channel: 0
            logical_controls:
            -   name: fader
                physical_control:
                - track_level
                - master_level
            -   mode: toggle
                physical_control: clip_launch
            -   children:
                -   children:
                    -   name: knob
                        physical_control: device_control
                    modal: outer_modal:inner_mutex
                    name: knobs
                -   children:
                    - device_left
                    - device_right
                    mode: mutex
                    name: inner_mutex
                modal: outer_mutex
                name: outer_modal
            -   children:
                - clip_stop_a
                - clip_stop_b
                mode: mutex
                name: outer_mutex
            on_startup:
            -   - 1
                - 2
                - 3
                - 4
                - 5
                - 6
                - 7
                - 8
            physical_controls:
            -   channel:
                - 0
                - 1
                has_led: true
                mode: boolean
                name: clip_launch
                note:
                - 1
                - 2
            -   boolean_polarity:
                - 0
                - 127
                channel: 0
                has_led: true
                mode: boolean
                name: clip_stop_a
                note: 3
            -   boolean_polarity:
                - 0
                - 127
                channel: 1
                has_led: true
                mode: boolean
                name: clip_stop_b
                note: 3
            -   controller:
                - 16
                - 17
                - 18
                has_led: true
                mode: continuous
                name: device_control
            -   mode: boolean
                name: device_left
                note: 5
            -   mode: boolean
                name: device_right
                note: 6
            -   channel:
                - 0
                - 1
                controller: 32
                mode: continuous
                name: track_level
            -   controller: 48
                mode: continuous
                name: master_level
            port: Test Device
        """) + '\n'


def test_02():
    path = base_path / 'Test-Physical.yml'
    manifest = supriya.system.YAMLLoader.load(path)
    assert yaml.dump(
        manifest,
        default_flow_style=False,
        indent=4,
        ) == uqbar.strings.normalize("""
        device:
            defaults:
                channel: 0
            on_startup:
            -   - 1
                - 2
                - 3
                - 4
                - 5
                - 6
                - 7
                - 8
            physical_controls:
            -   channel:
                - 0
                - 1
                has_led: true
                mode: boolean
                name: clip_launch
                note:
                - 1
                - 2
            -   boolean_polarity:
                - 0
                - 127
                channel: 0
                has_led: true
                mode: boolean
                name: clip_stop_a
                note: 3
            -   boolean_polarity:
                - 0
                - 127
                channel: 1
                has_led: true
                mode: boolean
                name: clip_stop_b
                note: 3
            -   controller:
                - 16
                - 17
                - 18
                has_led: true
                mode: continuous
                name: device_control
            -   mode: boolean
                name: device_left
                note: 5
            -   mode: boolean
                name: device_right
                note: 6
            -   channel:
                - 0
                - 1
                controller: 32
                mode: continuous
                name: track_level
            -   controller: 48
                mode: continuous
                name: master_level
            port: Test Device
        """) + '\n'


def test_03():
    path = base_path / 'Test-Logical.yml'
    manifest = supriya.system.YAMLLoader.load(path)
    assert yaml.dump(
        manifest,
        default_flow_style=False,
        indent=4,
        ) == uqbar.strings.normalize("""
        device:
            defaults:
                channel: 0
            logical_controls:
            -   children:
                -   name: fader
                    physical_control: track_level_1
                -   children:
                    -   name: null
                        physical_control: clip_launch_1x1
                    -   name: null
                        physical_control: clip_launch_2x1
                    name: slot
                name: track_1
            -   children:
                -   name: fader
                    physical_control: track_level_2
                -   children:
                    -   name: null
                        physical_control: clip_launch_1x2
                    -   name: null
                        physical_control: clip_launch_2x2
                    name: slot
                name: track_2
            -   name: master_fader
                physical_control: master_level
            -   children:
                -   children:
                    -   name: knob
                        physical_control: device_control
                    modal: outer_modal:inner_mutex
                    name: knobs
                -   children:
                    - device_left
                    - device_right
                    mode: mutex
                    name: inner_mutex
                modal: outer_mutex
                name: outer_modal
            -   children:
                - clip_stop_a
                - clip_stop_b
                mode: mutex
                name: outer_mutex
            on_startup:
            -   - 1
                - 2
                - 3
                - 4
                - 5
                - 6
                - 7
                - 8
            physical_controls:
            -   channel:
                - 0
                - 1
                has_led: true
                mode: boolean
                name: clip_launch
                note:
                - 1
                - 2
            -   boolean_polarity:
                - 0
                - 127
                channel: 0
                has_led: true
                mode: boolean
                name: clip_stop_a
                note: 3
            -   boolean_polarity:
                - 0
                - 127
                channel: 1
                has_led: true
                mode: boolean
                name: clip_stop_b
                note: 3
            -   controller:
                - 16
                - 17
                - 18
                has_led: true
                mode: continuous
                name: device_control
            -   mode: boolean
                name: device_left
                note: 5
            -   mode: boolean
                name: device_right
                note: 6
            -   channel:
                - 0
                - 1
                controller: 32
                mode: continuous
                name: track_level
            -   controller: 48
                mode: continuous
                name: master_level
            port: Test Device
        extends: Test-Physical.yml
        templates:
            track:
                children:
                -   name: fader
                    physical_control: track_level_{{ index }}
                -   children:
                    -   name: null
                        physical_control: clip_launch_1x{{ index }}
                    -   name: null
                        physical_control: clip_launch_2x{{ index }}
                    name: slot
                name: track_{{ index }}
        """) + '\n'
