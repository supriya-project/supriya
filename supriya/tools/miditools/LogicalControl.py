from supriya.tools.systemtools import Enumeration


class LogicalControl(object):

    class Mode(Enumeration):
        CONTINUOUS = 0
        TRIGGER = 1
        TOGGLE = 2

    def __init__(
        self,
        name,
        physical_control,
        mode=None,
        ):
        self.mode = self.Mode.from_expr(mode)
        self.name = name
        self.physical_control = physical_control
        self.parent = None
        self.value = 0.
        self.previous_value = 0.

    def debug(self, only_visible=None):
        parts = [
            'LC',
            'name={}'.format(self.name),
            'mode={}'.format(self.mode.name.lower()),
            'pc={}'.format(self.physical_control.name),
            'value={}'.format(self.value),
            ]
        return '<{}>'.format(' '.join(parts))

    def mount(self):
        if self.mode in (self.Mode.CONTINUOUS, self.Mode.TOGGLE):
            self.physical_control.set_led(self.value * 127)
        else:
            self.physical_control.set_led(0)

    def unmount(self):
        if (
            self.mode == self.Mode.CONTINUOUS and
            self.physical_control.mode == self.physical_control.Mode.BOOLEAN
            ):
            self.previous_value = self.value
            self.value = 0.

    @property
    def qualified_name(self):
        names = [self.name]
        node = self
        while node.parent is not None:
            node = node.parent
            names.append(node.name)
        return ':'.join(str(_) for _ in reversed(names))
