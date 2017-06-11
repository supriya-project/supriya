from supriya.tools.miditools.PhysicalControl import PhysicalControl


class PhysicalManifest:

    ### INITIALIZER ###

    def __init__(self, device):
        self._device = device
        self._message_handlers = {
            8: self._handle_note_on_message,
            9: self._handle_note_off_message,
            11: self._handle_controller_change_message,
            }
        self._controls = {}
        self._controls_by_group = {}
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
                    key = (channel, message_value)
                    if message_type == 'note':
                        self._controls_by_note_number[key] = control
                    elif message_type == 'controller':
                        self._controls_by_controller_number[key] = control

    ### SPECIAL METHODS ###

    def __call__(self, message, timestamp):
        from supriya.tools import miditools
        if timestamp is None:
            message, timestamp = message
        status_byte, data = message[0], message[1:]
        message_type = status_byte >> 4
        channel_number = status_byte & 0x0f
        handler = self._message_handlers.get(message_type)
        if not handler:
            raise ValueError(message)
        message = handler(channel_number, data, timestamp)
        if isinstance(message, miditools.ControllerChangeMessage):
            value = message.controller_value
            control = self._controls_by_controller_number[
                (message.channel_number, message.controller_number)]
        elif isinstance(message, miditools.NoteOnMessage):
            value = message.velocity
            control = self._controls_by_note_number[
                (message.channel_number, message.note_number)]
        else:
            raise Exception(message)
        value = control.handle_incoming_value(value)
        return control, value

    ### PRIVATE METHODS ###

    def _handle_controller_change_message(self, channel_number, data, timestamp):
        from supriya.tools import miditools
        controller_number, controller_value = data
        message = miditools.ControllerChangeMessage(
            channel_number=channel_number,
            controller_number=controller_number,
            controller_value=controller_value,
            timestamp=timestamp,
            )
        return message

    def _handle_note_off_message(self, channel_number, data, timestamp):
        from supriya.tools import miditools
        note_number, velocity = data
        message = miditools.NoteOnMessage(
            channel_number=channel_number,
            note_number=note_number,
            timestamp=timestamp,
            velocity=0,
            )
        return message

    def _handle_note_on_message(self, channel_number, data, timestamp):
        from supriya.tools import miditools
        note_number, velocity = data
        message = miditools.NoteOnMessage(
            channel_number=channel_number,
            note_number=note_number,
            timestamp=timestamp,
            velocity=velocity,
            )
        return message

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
