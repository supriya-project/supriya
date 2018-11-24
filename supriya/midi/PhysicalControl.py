from uqbar.enums import IntEnumeration


class PhysicalControl:
    class Mode(IntEnumeration):
        CONTINUOUS = 0
        BOOLEAN = 1

    def __init__(
        self,
        device,
        name,
        message_type,
        message_value,
        automatable=False,
        boolean_led_polarity=None,
        boolean_polarity=None,
        channel=0,
        group_name=None,
        has_led=False,
        mode='continuous',
    ):
        self.device = device
        self.name = name
        self.message_type = message_type
        self.message_value = int(message_value)
        self.automatable = bool(automatable)
        self.boolean_led_polarity = boolean_led_polarity
        self.boolean_polarity = boolean_polarity
        self.channel = int(channel)
        self.group_name = group_name or name
        self.has_led = bool(has_led)
        self.mode = self.Mode.from_expr(mode)

    def set_led(self, value):
        value = int(value)
        if self.message_type == 'note':
            if value:
                message = 0x90 | self.channel
            else:
                message = 0x80 | self.channel
        elif self.message_type == 'controller':
            message = 0xB0 | self.channel
        message = [message, self.message_value, value]
        self.device.send_message(message)

    def handle_incoming_value(self, value):
        if self.mode == self.Mode.BOOLEAN:
            if self.boolean_polarity:
                if value == 127:
                    value = self.boolean_polarity[0]
                else:
                    value = self.boolean_polarity[1]
            value = float(value == 127)
        elif self.mode == self.Mode.CONTINUOUS:
            value /= 127
        else:
            raise Exception(value)
        assert 0.0 <= value <= 1.0
        return value
