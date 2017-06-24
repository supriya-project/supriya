import logging
import pathlib
import rtmidi
import threading
import yaml
from supriya.tools.miditools.View import View
from supriya.tools.miditools.LogicalControl import LogicalControl
from supriya.tools.miditools.LogicalManifest import LogicalManifest
from supriya.tools.miditools.PhysicalManifest import PhysicalManifest


logging.basicConfig(
    format='%(asctime)s [%(name)s] [%(levelname)s] %(message)s',
    level='DEBUG',
    )


class Device:

    def __init__(self, manifest_path, logger=None):
        import supriya
        self._logger = logger or logging.getLogger(type(self).__name__)
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

    def __call__(self, message, timestamp=None):
        if timestamp is None:
            message, timestamp = message
        self.logger.debug('MIDI I: 0x{}'.format(bytearray(message).hex()))
        with self._lock:
            physical_control, value = self._process_one(message, timestamp)
            self._process_two(physical_control, value)

    ### PRIVATE METHODS ###

    def _process_one(self, message, timestamp):
        from supriya.tools import miditools
        if timestamp is None:
            message, timestamp = message
        status_byte, data = message[0], message[1:]
        message_type = status_byte >> 4
        channel = status_byte & 0x0f
        if message_type == 8:
            message_class = miditools.NoteOnMessage
            message_number, value = data
        elif message_type == 9:
            message_class = miditools.NoteOnMessage
            message_number, value = data[0], 0
        elif message_type == 11:
            message_class = miditools.ControllerChangeMessage
            message_number, value = data
        else:
            raise Exception(message)
        key = (message_class, channel, message_number)
        control = self._physical_manifest._controls_by_command[key]
        value = control.handle_incoming_value(value)
        return control, value

    def _process_two(self, physical_control, value):
        logical_control = self.logical_manifest.visibility_mapping.get(
            physical_control)
        if not logical_control:
            return
        if logical_control.parent.mode == View.Mode.MUTEX and value:
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
                if control.value == 1.0
                ][0]
            if old_logical_control is new_logical_control:
                return

            lm = self.logical_manifest

            old_mapping = set(lm.rebuild_visibility_mapping().values())
            for dependent in self.logical_manifest.dependents.get(
                old_logical_control, []):
                dependent.visible = False
            old_logical_control.value = 0.0

            new_logical_control.value = 1.0
            for dependent in self.logical_manifest.dependents.get(
                logical_control, []):
                dependent.visible = True
            new_mapping = set(lm.rebuild_visibility_mapping().values())

            for logical_control in old_mapping - new_mapping:
                logical_control.unmount()

            for logical_control in new_mapping - old_mapping:
                logical_control.mount()

        elif logical_control.mode == LogicalControl.Mode.TOGGLE and value:
            value = 1 - logical_control.value
            logical_control.value = value
            logical_control.physical_control.set_led(value * 127)

        elif logical_control.mode == LogicalControl.Mode.TRIGGER and value:
            logical_control.physical_control.set_led(value * 127)
            value = None

        elif logical_control.mode == LogicalControl.Mode.CONTINUOUS:
            logical_control.physical_control.set_led(value * 127)
            logical_control.value = value

    ### PUBLIC METHODS ###

    def close_port(self):
        self._midi_in.close_port()
        self._midi_out.close_port()
        self.logger.info('Closed port.')
        return self

    def get_ports(self):
        return self._midi_in.get_ports()

    def get_port_count(self):
        return self._midi_in.get_port_count()

    def get_port_name(self, port_number):
        return self._midi_in.get_port_name()

    def open_port(self, port=None, virtual=False):
        self.logger.info('Opening port {}'.format(port))
        if virtual:
            self._midi_in.open_virtual_port()
            self._midi_out.open_virtual_port()
        else:
            if port is None:
                port_names = self.get_ports()
                akai_name = 'Akai APC40'
                assert akai_name in port_names
                port = port_names.index(akai_name)
            self._midi_in.open_port(port)
            self._midi_out.open_port(port)
        self._midi_in.ignore_types(
            active_sense=True,
            sysex=True,
            timing=True,
            )
        self._midi_in.set_callback(self.__call__)
        for message in self._device_manifest['device'].get('on_startup', []):
            self.send_message(message)
        mapping = self.logical_manifest.rebuild_visibility_mapping()
        for logical_control in mapping.values():
            logical_control.mount()
        return self

    def send_message(self, message):
        self._midi_out.send_message(message)
        self.logger.debug('MIDI O: 0x{}'.format(bytearray(message).hex()))

    ### PUBLIC PROPERTIES ###

    @property
    def logger(self):
        return self._logger

    @property
    def logical_manifest(self):
        return self._logical_manifest

    @property
    def physical_manifest(self):
        return self._physical_manifest

    @property
    def root_view(self):
        return self._logical_manifest.root_view
