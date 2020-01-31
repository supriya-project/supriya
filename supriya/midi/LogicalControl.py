from supriya.midi.LogicalControlMode import LogicalControlMode


class LogicalControl:

    ### INITIALIZER ###

    def __init__(self, name, physical_control, device, mode=None):
        self.device = device
        self.mode = LogicalControlMode.from_expr(mode)
        self.name = name
        self.parent = None
        self.physical_control = physical_control
        self.previous_value = 0.0
        self.value = 0.0

    ### SPECIAL METHODS ###

    def __call__(self, value):
        value = float(value)
        if self.parent.is_mutex:
            if value:
                current_control = self.parent._get_active_child()
                if current_control is self:
                    return value
                old_mapping = set(self.device._visibility_mapping.values())
                for dependent in self.device.dependents.get(self, []):
                    dependent.visible = True
                current_control(0.0)
                new_mapping = set(self.device.rebuild_visibility_mapping().values())
                for logical_control in old_mapping - new_mapping:
                    logical_control._unmount()
                for logical_control in new_mapping - old_mapping:
                    logical_control._mount()
            else:
                for dependent in self.device.dependents.get(self, []):
                    dependent.visible = False
        self.value = value
        if self.is_visible and self.mode != LogicalControlMode.TRIGGER:
            self.physical_control.set_led(value * 127)
        return value

    def __repr__(self):
        return "<{} {} {}>".format(type(self).__name__, self.qualified_name, self.value)

    ### PRIVATE METHODS ###

    def _debug(self, only_visible=None):
        parts = [
            "LC",
            "name={}".format(self.name),
            "mode={}".format(self.mode.name.lower()),
            "pc={}".format(self.physical_control.name),
            "value={}".format(round(self.value, 6)),
        ]
        return "<{}>".format(" ".join(parts))

    def _mount(self):
        if self.mode in (LogicalControlMode.CONTINUOUS, LogicalControlMode.TOGGLE):
            self.physical_control.set_led(self.value * 127)
        else:
            self.physical_control.set_led(0)

    def _unmount(self):
        if (
            self.mode == LogicalControlMode.CONTINUOUS
            and self.physical_control.mode == self.physical_control.Mode.BOOLEAN
        ):
            self.previous_value = self.value
            self.value = 0.0

    ### PUBLIC PROPERTIES ###

    @property
    def is_visible(self):
        return self in self.device.visibility_mapping.values()

    @property
    def qualified_name(self):
        names = [self.name]
        node = self
        while node.parent is not None:
            node = node.parent
            names.append(node.name)
        return ":".join(str(_) for _ in reversed(names))
