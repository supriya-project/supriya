from uuid import UUID, uuid4

from supriya.enums import AddAction

from .bases import Allocatable, AllocatableContainer, ApplicationObject


class ParameterSpec:
    pass


class Boolean(ParameterSpec):

    ### INITIALIZER ###

    def __init__(self, default=True):
        self.default = bool(default)

    ### SPECIAL METHODS ###

    def __call__(self, value):
        return bool(value)


class Float(ParameterSpec):

    ### INITIALIZER ###

    def __init__(self, default: int = 0.0, minimum: float = 0.0, maximum: float = 1.0):
        self.minimum, self.maximum = sorted(float(_) for _ in [minimum, maximum])
        self.default = self(default)

    ### SPECIAL METHODS ###

    def __call__(self, value):
        value = float(value)
        if value < self.minimum:
            return self.minimum
        if value > self.maximum:
            return self.maximum
        return value


class Integer(ParameterSpec):

    ### INITIALIZER ###

    def __init__(self, default: int = 0, minimum: int = 0, maximum: int = 1):
        self.minimum, self.maximum = sorted(int(_) for _ in [minimum, maximum])
        self.default = self(default)

    ### SPECIAL METHODS ###

    def __call__(self, value):
        value = int(value)
        if value < self.minimum:
            return self.minimum
        if value > self.maximum:
            return self.maximum
        return value


class Action(ApplicationObject):

    ### INITIALIZER ###

    def __init__(self, name, callback=None):
        if not name:
            raise ValueError(name)
        ApplicationObject.__init__(self, name=name)
        if callback is not None and not callable(callback):
            raise ValueError(callback)
        self._callback = callback
        self._client = None

    ### SPECIAL METHODS ###

    def __call__(self):
        if self.application is None:
            return
        self.callback(self.client)

    def __str__(self):
        obj_name = type(self).__name__
        return "\n".join([
            f'<{obj_name} "{self.name}">',
            *(f"    {line}" for child in self for line in str(child).splitlines()),
        ])

    ### PRIVATE METHODS ###

    def _applicate(self, new_application):
        Allocatable._applicate(self, new_application)
        self._client = self.parent.parent

    def _deapplicate(self, old_application):
        Allocatable._deapplicate(self, old_application)
        self._client = None

    def _preallocate(self, provider, client):
        pass

    ### PUBLIC PROPERTIES ###

    @property
    def callback(self):
        return self._callback

    @property
    def client(self) -> ApplicationObject:
        return self._client


class Parameter(Allocatable):

    ### INITIALIZER ###

    def __init__(
        self, name, spec, *, callback=None, has_bus=False, uuid=None
    ):
        if not name:
            raise ValueError(name)
        Allocatable.__init__(self, channel_count=1, name=name)
        if not isinstance(spec, ParameterSpec):
            raise ValueError(spec)
        if callback is not None and not callable(callback):
            raise ValueError(callback)
        self._callback = callback
        self._client = None
        self._has_bus = bool(has_bus)
        self._spec = spec
        self._value = self.spec.default
        self._uuid = uuid or uuid4()

    ### SPECIAL METHODS ###

    def __str__(self):
        if self.has_bus:
            bus_proxy_id = int(self.bus_proxy) if self.bus_proxy is not None else "..."
            node_proxy_id = int(self.node_proxy) if self.node_proxy is not None else "..."
        else:
            bus_proxy_id, node_proxy_id = "-", "-"
        obj_name = type(self).__name__
        return "\n".join([
            f'<{obj_name} "{self.name}" {self.value} [{node_proxy_id}] [{bus_proxy_id}] {self.uuid}>',
            *(f"    {line}" for child in self for line in str(child).splitlines()),
        ])

    ### PRIVATE METHODS ###

    def _allocate(self, provider, target_node, add_action):
        Allocatable._allocate(self, provider, target_node, add_action)
        if not self.has_bus:
            return
        self._node_proxies["node"] = provider.add_group(
            target_node=target_node, add_action=add_action, name=self.label
        )

    def _applicate(self, new_application):
        Allocatable._applicate(self, new_application)
        self._client = self.parent.parent

    def _deapplicate(self, old_application):
        Allocatable._deapplicate(self, old_application)
        self._client = None

    def _preallocate(self, provider, client):
        self._debug_tree(self, "Pre-Allocating", suffix=f"{hex(id(provider))}")
        if not self.has_bus:
            return
        self._control_bus_proxies["bus"] = provider.add_bus("control")
        self._control_bus_proxies["bus"].set_(self.spec.default)

    ### PUBLIC METHODS ###

    def get(self):
        pass

    def modulate(self):
        pass

    def ramp(self, from_value, to_value, total_time, *, initial_time=0, moment=None):
        with self.lock([self], seconds=moment.seconds if moment is not None else None):
            pass

    def set_(self, value, *, moment=None):
        with self.lock([self], seconds=moment.seconds if moment is not None else None):
            if self.application is None:
                return
            self._value = self.spec(value)
            if self.bus_proxy is not None:
                self.bus_proxy.set_(self._value)
            if self.callback is not None:
                self.callback(self.client, self._value)

    ### PUBLIC PROPERTIES ###

    @property
    def bus_proxy(self):
        return self._control_bus_proxies.get("bus")

    @property
    def callback(self):
        return self._callback

    @property
    def client(self) -> ApplicationObject:
        return self._client

    @property
    def has_bus(self):
        return self._has_bus

    @property
    def spec(self) -> ParameterSpec:
        return self._spec

    @property
    def uuid(self) -> UUID:
        return self._uuid

    @property
    def value(self):
        return self._value


class ParameterGroup(AllocatableContainer):
    def __init__(self):
        AllocatableContainer.__init__(
            self,
            target_node_name="node",
            add_action=AddAction.ADD_TO_HEAD,
            label="Parameters",
        )

    def _allocate(self, provider, target_node, add_action):
        Allocatable._allocate(self, provider, target_node, add_action)
        target_node = self.parent.node_proxies[self.target_node_name]
        if any(x.has_bus for x in self):
            self._node_proxies["node"] = provider.add_group(
                target_node=target_node, add_action=self.add_action, name=self.label
            )
