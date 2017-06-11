import pathlib
import rtmidi
import threading
import yaml
from supriya.tools.miditools.View import View
from supriya.tools.miditools.LogicalControl import LogicalControl
from supriya.tools.miditools.LogicalManifest import LogicalManifest
from supriya.tools.miditools.PhysicalManifest import PhysicalManifest


class Device:

    # TODO: integrate logging

    def __init__(self, manifest_path):
        import supriya
        manifest_path = pathlib.Path(manifest_path)
        if not manifest_path.suffix:
            manifest_path = manifest_path.with_suffix('.yml')
        if not manifest_path.is_absolute():
            manifest_path = (
                pathlib.Path(supriya.__path__[0]) /
                'assets' /
                'devices' /
                manifest_path
                )
        self._lock = threading.RLock()
        self._midi_in = rtmidi.MidiIn()
        self._midi_out = rtmidi.MidiOut()
        with open(str(manifest_path)) as file_pointer:
            self._device_manifest = yaml.load(file_pointer)
        self._physical_manifest = PhysicalManifest(self)
        self._logical_manifest = LogicalManifest(self)

    ### SPECIAL METHODS ###

    def __call__(self, message, timestamp):
        with self._lock:
            physical_control, value = self.physical_manifest(message, timestamp)
            print('P', physical_control.name, value)
            # Is there a logical control?
            logical_control = self.logical_manifest.visibility_mapping.get(
                physical_control)
            if not logical_control:
                return
            if logical_control.parent.mode == View.Mode.MUTEX and value:
                print('L', 'MUTEX', logical_control.name)
                new_logical_control = logical_control
                mutex_controls = tuple(
                    logical_control.parent.children.values()
                    )
                for control in mutex_controls:
                    if control is new_logical_control:
                        control.physical_control.set_led(127)
                    else:
                        control.physical_control.set_led(0)
                old_logical_control = [
                    control for control in mutex_controls
                    if control.value == 1
                    ][0]
                if old_logical_control is new_logical_control:
                    return

                #old_mapping = self.logical_manifest.rebuild_visibility_mapping()
                #for dependent in self.logical_manifest.dependents.get(
                #    old_logical_control, []):
                #    dependent.visible = False
                old_logical_control.value = 0

                new_logical_control.value = 1
                #for dependent in self.logical_manifest.dependents.get(
                #    logical_control, []):
                #    dependent.visible = True
                #new_mapping = self.logical_manifest.rebuild_visibility_mapping()

                #for logical_control in old_mapping - new_mapping:
                #    logical_control.unmount()

                #for logical_control in new_mapping - old_mapping:
                #    logical_control.mount()

                # - transmit value
            elif logical_control.mode == LogicalControl.Mode.TOGGLE and value:
                print('L', 'TOGGLE', logical_control.name)
                value = 1 - logical_control.value
                logical_control.value = value
                logical_control.physical_control.set_led(value * 127)
            elif logical_control.mode == LogicalControl.Mode.TRIGGER and value:
                print('L', 'TRIGGER', logical_control.name)
                logical_control.physical_control.set_led(value * 127)
                value = None
            elif logical_control.mode == LogicalControl.Mode.CONTINUOUS:
                print('L', 'CONTINUOUS', logical_control.name)
                logical_control.physical_control.set_led(value * 127)
                logical_control.value = value

    ### PRIVATE METHODS ###

    def _choose_mode(self, mode):
        # TODO: use manifest['on_startup'] instead
        assert mode in (0, 1, 2)
        modes = [0x40, 0x41, 0x42]
        message = [
            0xF0, 0x47, 0x1, 0x73, 0x60, 0x0,
            0x4, modes[mode], 0x1, 0x1, 0x1, 0xF7,
            ]
        self._midi_out.send_message(message)

    ### PUBLIC METHODS ###

    def close_port(self):
        self._midi_in.close_port()
        self._midi_out.close_port()
        return self

    def get_ports(self):
        return self._midi_in.get_ports()

    def get_port_count(self):
        return self._midi_in.get_port_count()

    def get_port_name(self, port_number):
        return self._midi_in.get_port_name()

    def open_port(self, port=None, virtual=False):
        if port is None:
            port_names = self.get_ports()
            akai_name = 'Akai APC40'
            assert akai_name in port_names
            port = port_names.index(akai_name)
        if virtual:
            self._midi_in.open_virtual_port()
            self._midi_out.open_virtual_port()
        else:
            self._midi_in.open_port(port)
            self._midi_out.open_port(port)
        self._midi_in.ignore_types(
            active_sense=True,
            sysex=True,
            timing=True,
            )
        self._midi_in.set_callback(self.__call__)
        self._choose_mode(1)
        # TODO: mount logical controls in order to set LEDs
        #self._logical_manifest = LogicalManifest(self)
        mapping = self.logical_manifest.rebuild_visibility_mapping()
        for logical_control in mapping.values():
            logical_control.mount()
        return self

    def send_message(self, message):
        self._midi_out.send_message(message)

    ### PUBLIC PROPERTIES ###

    @property
    def logical_manifest(self):
        return self._logical_manifest

    @property
    def physical_manifest(self):
        return self._physical_manifest
