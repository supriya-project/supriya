import collections
import logging
import pathlib
import rtmidi
import threading
import yaml
from supriya.tools import systemtools
from supriya.tools.miditools.View import View
from supriya.tools.miditools.LogicalControl import LogicalControl
from supriya.tools.miditools.PhysicalControl import PhysicalControl


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
        self._physical_controls = {}
        self._physical_controls_by_group = {}
        self._physical_controls_by_command = {}
        self._initialize_physical_controls()
        self._initialize_logical_controls()

    ### SPECIAL METHODS ###

    def __call__(self, message, timestamp=None):
        if timestamp is None:
            message, timestamp = message
        self.logger.debug('MIDI I: 0x{}'.format(bytearray(message).hex()))
        with self._lock:
            physical_control, value = self._process_one(message, timestamp)
            self._process_two(physical_control, value)

    ### PRIVATE METHODS ###

    def _build_modal_view(self, node_template, parents):
        nodes = []
        toggle_id = 'root:{}'.format(node_template['modal'])
        all_toggles = self._node_instances[toggle_id]
        for parent, toggles in zip(parents, all_toggles):
            modal_view = View(name=node_template['name'], visible=True)
            parent.add_child(modal_view)
            for i, toggle in enumerate(toggles.children.values()):
                view = View(
                    name=i,
                    visible=i == 0,
                    )
                nodes.append(view)
                modal_view.add_child(view)
                self._dependents.setdefault(toggle, []).append(view)
        return nodes

    def _build_mutex_view(self, node_template, parents):
        nodes = []
        physical_controls = []
        physical_control_ids = node_template['children']
        for physical_control_id in physical_control_ids:
            physical_controls.extend(
                self._get_controls_by_name(
                    physical_control_id))
        for parent in parents:
            view = View(name=node_template['name'], mode='mutex')
            nodes.append(view)
            parent.add_child(view)
            for i, physical_control in enumerate(physical_controls):
                control = LogicalControl(
                    name=i,
                    mode='toggle',
                    physical_control=physical_control,
                    )
                if i == 0:
                    control.value = 1.0
                view.add_child(control)
        return nodes

    def _build_view(self, node_template, parents):
        pass

    def _build_physical_controls(self, node_template, parents):
        nodes = []
        physical_controls = []
        physical_control_ids = node_template['physical_control']
        if isinstance(physical_control_ids, str):
            physical_control_ids = [physical_control_ids]
        for physical_control_id in physical_control_ids:
            physical_controls.extend(
                self._get_controls_by_name(
                    physical_control_id))
        for parent in parents:
            for i, physical_control in enumerate(physical_controls, 1):
                if 'name' in node_template:
                    if node_template['name']:
                        name = node_template['name']
                        if len(physical_controls) > 1:
                            name = '{}_{}'.format(name, i)
                    else:
                        name = i - 1
                else:
                    name = physical_control.name
                mode = node_template.get('mode')
                logical_control = LogicalControl(
                    mode=mode,
                    name=name,
                    physical_control=physical_control,
                    )
                nodes.append(logical_control)
                parent.add_child(logical_control)
        return nodes

    def _get_controls_by_name(self, name):
        if name in self.physical_controls_by_group:
            return self.physical_controls_by_group[name]
        elif name in self.physical_controls:
            return [self.physical_controls[name]]
        raise KeyError

    def _initialize_logical_controls(self):
        device_manifest = self._device_manifest['device']
        manifest = device_manifest['logical_controls']
        self._node_templates = self._linearize_manifest(manifest)
        self._node_instances = {}
        self._node_instances['root'] = [View(name='root')]
        self._dependents = {}
        for parentage_string, node_template in self._node_templates.items():
            parents = self._node_instances[parentage_string.rpartition(':')[0]]
            if 'children' in node_template:
                if 'modal' in node_template:
                    nodes = self._build_modal_view(node_template, parents)
                elif node_template.get('mode') == 'mutex':
                    nodes = self._build_mutex_view(node_template, parents)
                else:
                    nodes = self._build_view(node_template, parents)
            elif 'physical_control' in node_template:
                nodes = self._build_physical_controls(node_template, parents)
            else:
                raise Exception(parentage_string, node_template)
            self._node_instances[parentage_string] = nodes
        self.rebuild_visibility_mapping()

    def _initialize_physical_controls(self):
        device_manifest = self._device_manifest['device']
        manifest = device_manifest['physical_controls']
        defaults = device_manifest.get('defaults', {})
        for spec in manifest:
            default_spec = defaults.copy()
            default_spec.update(spec)
            spec = default_spec
            if 'note' in spec:
                message_type = 'note'
                message_values = spec.get('note')
            elif 'controller' in spec:
                message_type = 'controller'
                message_values = spec.get('controller')
            else:
                raise ValueError('Missing message type in {}'.format(spec))
            channels = spec.get('channel', 0)
            if not isinstance(message_values, list):
                message_values = [message_values]
            if not isinstance(channels, list):
                channels = [channels]
            if len(channels) > 1 and len(message_values) > 1:
                template = '{control_group}_{value_index}x{channel_index}'
            elif len(channels) > 1:
                template = '{control_group}_{channel_index}'
            elif len(message_values) > 1:
                template = '{control_group}_{value_index}'
            else:
                template = '{control_group}'
            for value_index, message_value in enumerate(message_values, 1):
                for channel_index, channel in enumerate(channels, 1):
                    control_name = template.format(
                        control_group=spec['name'],
                        value_index=value_index,
                        channel_index=channel_index,
                        )
                    self._add_physical_control(
                        control_name,
                        message_type,
                        message_value,
                        boolean_led_polarity=spec.get('boolean_led_polarity'),
                        boolean_polarity=spec.get('boolean_polarity'),
                        channel=channel,
                        group_name=spec['name'],
                        has_led=spec.get('has_led', False),
                        mode=spec['mode'],
                        )

    def _add_physical_control(
        self,
        control_name,
        message_type,
        message_value,
        boolean_led_polarity=None,
        boolean_polarity=None,
        channel=None,
        group_name=None,
        has_led=None,
        mode=None,
        ):
        from supriya.tools import miditools
        assert control_name not in self._physical_controls
        physical_control = PhysicalControl(
            self,
            control_name,
            message_type,
            message_value,
            boolean_led_polarity=boolean_led_polarity,
            boolean_polarity=boolean_polarity,
            channel=channel,
            group_name=group_name,
            has_led=has_led,
            mode=mode,
            )
        self._physical_controls[control_name] = physical_control
        self._physical_controls_by_group.setdefault(
            group_name, []).append(physical_control)
        if message_type == 'note':
            message_class = miditools.NoteOnMessage
        elif message_type == 'controller':
            message_class = miditools.ControllerChangeMessage
        else:
            raise Exception
        key = (message_class, channel, message_value)
        self._physical_controls_by_command[key] = physical_control
        return physical_control

    def _linearize_manifest(self, manifest):
        trellis = systemtools.Trellis()
        entries_by_parentage = {}
        self._recurse_manifest(
            entries_by_parentage=entries_by_parentage,
            manifest=manifest,
            parentage=('root',),
            trellis=trellis,
            )
        templates = collections.OrderedDict()
        for parentage_string in trellis:
            if parentage_string == 'root':
                continue
            templates[parentage_string] = entries_by_parentage[parentage_string]
        return templates

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
        control = self._physical_controls_by_command[key]
        value = control.handle_incoming_value(value)
        return control, value

    def _process_two(self, physical_control, value):
        logical_control = self.visibility_mapping.get(
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
            old_mapping = set(self.rebuild_visibility_mapping().values())
            for dependent in self.dependents.get(
                old_logical_control, []):
                dependent.visible = False
            old_logical_control.value = 0.0
            new_logical_control.value = 1.0
            for dependent in self.dependents.get(
                logical_control, []):
                dependent.visible = True
            new_mapping = set(self.rebuild_visibility_mapping().values())
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

    def _recurse_manifest(
        self,
        entries_by_parentage,
        manifest,
        parentage,
        trellis,
        ):
        for entry in manifest:
            entry_name = entry.get('name') or entry.get('physical_control')
            assert entry_name
            entry_parentage = parentage + (entry_name,)
            entry_parentage_string = ':'.join(entry_parentage)
            assert entry_parentage_string not in entries_by_parentage
            entries_by_parentage[entry_parentage_string] = entry
            if parentage:
                parentage_string = ':'.join(parentage)
                trellis.add(
                    parentage_string,
                    entry_parentage_string,
                    )
            else:
                trellis.add(entry_parentage_string)
            if 'modal' in entry:
                trellis.add(
                    'root:{}'.format(entry.get('modal')),
                    entry_parentage_string,
                    )
            children = entry.get('children', [])
            if entry.get('mode') != 'mutex':
                self._recurse_manifest(
                    entries_by_parentage=entries_by_parentage,
                    manifest=children,
                    parentage=entry_parentage,
                    trellis=trellis,
                    )

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
        mapping = self.rebuild_visibility_mapping()
        for logical_control in mapping.values():
            logical_control.mount()
        return self

    def rebuild_visibility_mapping(self):
        mapping = collections.OrderedDict()
        for logical_control in self.root_view.yield_visible_controls():
            physical_control = logical_control.physical_control
            assert physical_control not in mapping
            mapping[physical_control] = logical_control
        self._visibility_mapping = mapping
        return mapping

    def send_message(self, message):
        self._midi_out.send_message(message)
        self.logger.debug('MIDI O: 0x{}'.format(bytearray(message).hex()))

    ### PUBLIC PROPERTIES ###

    @property
    def dependents(self):
        return self._dependents

    @property
    def physical_controls(self):
        return self._physical_controls

    @property
    def physical_controls_by_group(self):
        return self._physical_controls_by_group

    @property
    def physical_controls_by_command(self):
        return self._physical_controls_by_command

    @property
    def logger(self):
        return self._logger

    @property
    def root_view(self):
        return self._node_instances['root'][0]

    @property
    def visibility_mapping(self):
        return self._visibility_mapping
