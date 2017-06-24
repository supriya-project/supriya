from supriya.tools.miditools.PhysicalControl import PhysicalControl


class PhysicalManifest:

    ### INITIALIZER ###

    def __init__(self, device):
        from supriya.tools import miditools
        self._device = device
        self._controls = {}
        self._controls_by_group = {}
        self._controls_by_command = {}
        self._controls_by_note_number = {}
        self._controls_by_controller_number = {}
        device_manifest = self._device._device_manifest['device']
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
                    control = PhysicalControl(
                        self.device,
                        control_name,
                        message_type,
                        message_value,
                        automatable=spec.get('automatable', False),
                        boolean_led_polarity=spec.get('boolean_led_polarity'),
                        boolean_polarity=spec.get('boolean_polarity'),
                        channel=channel,
                        group_name=spec['name'],
                        has_led=spec.get('has_led', False),
                        mode=spec['mode'],
                        )
                    self._controls[control_name] = control
                    self._controls_by_group.setdefault(
                        spec['name'], []).append(control)
                    if message_type == 'note':
                        message_class = miditools.NoteOnMessage
                    elif message_type == 'controller':
                        message_class = miditools.ControllerChangeMessage
                    else:
                        raise Exception
                    key = (message_class, channel, message_value)
                    self._controls_by_command[key] = control

    ### PUBLIC METHODS ###

    def get_controls_by_name(self, name):
        if name in self.controls_by_group:
            return self.controls_by_group[name]
        elif name in self.controls:
            return [self.controls[name]]
        raise KeyError

    ### PUBLIC PROPERTIES ###

    @property
    def device(self):
        return self._device

    @property
    def controls(self):
        return self._controls

    @property
    def controls_by_group(self):
        return self._controls_by_group

    @property
    def controls_by_note_number(self):
        return self._controls_by_note_number

    @property
    def controls_by_controller_number(self):
        return self._controls_by_controller_number
