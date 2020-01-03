import abc
from typing import Optional, Set, Union
from uuid import UUID, uuid4

from supriya.enums import AddAction, CalculationRate
from supriya.provider import NodeProxy
from supriya.typing import Default

from .bases import Allocatable, ApplicationObject
from .synthdefs import build_patch_synthdef

# Send SynthDef creation is universal
# Let's generalize it to support all inter-object comms


class SendObject(Allocatable):

    ### INITIALIZER ###

    def __init__(self, name=None, uuid=None):
        self._gain = 0.0
        self._uuid = uuid or uuid4()
        Allocatable.__init__(self, name=name)

    ### SPECIAL METHODS ###

    def __str__(self):
        node_proxy_id = int(self.node_proxy) if self.node_proxy is not None else "?"
        obj_name = type(self).__name__
        return "\n".join(
            [
                f"<{obj_name} [{node_proxy_id}] {self.uuid}>",
                *(f"    {line}" for child in self for line in str(child).splitlines()),
            ]
        )

    ### PRIVATE METHODS ###

    def _reallocate(self, difference):
        Allocatable._reallocate(self, difference)
        node_proxy = self._node_proxies.pop("node")
        self._allocate(
            self.provider, target_node=node_proxy, add_action=AddAction.ADD_AFTER
        )
        node_proxy.free()

    ### PUBLIC METHODS ###

    @classmethod
    def build_synthdef(
        cls,
        source_channel_count,
        target_channel_count,
        *,
        feedback=False,
        calculation_rate=CalculationRate.AUDIO,
    ):
        return build_patch_synthdef(
            source_channel_count,
            target_channel_count,
            feedback=feedback,
            calculation_rate=calculation_rate,
        )

    def set_gain(self, gain):
        pass

    ### PUBLIC PROPERTIES ###

    @property
    def gain(self):
        return self._gain

    @property
    def uuid(self) -> UUID:
        return self._uuid


class Patch(SendObject):

    ### INITIALIZER ###

    def __init__(self, *, name=None, uuid=None):
        SendObject.__init__(self, name=name, uuid=uuid)

    ### PRIVATE METHODS ###

    def _allocate(self, provider, target_node, add_action):
        # TODO: Primary node proxy should be a dedicated group
        Allocatable._allocate(self, provider, target_node, add_action)
        self._allocate_synths(self.parent.node_proxy, AddAction.ADD_TO_HEAD)

    def _allocate_synths(self, target_node, add_action):
        self._node_proxies["node"] = self.provider.add_synth(
            active=self.is_active,
            add_action=add_action,
            in_=self.cached_state["source_bus"],
            out=self.cached_state["target_bus"],
            name=self.label,
            synthdef=self.build_synthdef(
                self.cached_state["source_channel_count"],
                self.cached_state["target_channel_count"],
                feedback=self.cached_state["feedback"],
            ),
            target_node=target_node,
        )

    def _get_state(self):
        return dict(
            application=self.application,
            feedback=self.feedback,
            index=self.parent.index(self) if self.parent else None,
            parent=self.parent,
            source=self.effective_source,
            source_anchor=self.source_anchor,
            source_bus=self.source_bus,
            source_channel_count=self.source_channel_count,
            source_provider=self.source_provider,
            target=self.effective_target,
            target_anchor=self.target_anchor,
            target_bus=self.target_bus,
            target_channel_count=self.target_channel_count,
            target_provider=self.target_provider,
        )

    def _reconcile(
        self,
        target_node: Optional[NodeProxy] = None,
        add_action: Optional[int] = None,
        dispose_only: bool = False,
        **kwargs,
    ):
        difference = self._get_state_difference()
        if "application" in difference:
            old_application, new_application = difference.pop("application")
            if old_application:
                self._deapplicate(old_application)
            if new_application:
                self._applicate(new_application)
        if "source_anchor" in difference:
            old_anchor, new_anchor = difference.pop("source_anchor")
            if old_anchor is not None and hasattr(old_anchor, "_dependencies"):
                old_anchor._dependencies.remove(self)
            if new_anchor is not None and hasattr(new_anchor, "_dependencies"):
                new_anchor._dependencies.add(self)
        if "target_anchor" in difference:
            old_anchor, new_anchor = difference.pop("target_anchor")
            if old_anchor is not None and hasattr(old_anchor, "_dependencies"):
                old_anchor._dependencies.remove(self)
            if new_anchor is not None and hasattr(new_anchor, "_dependencies"):
                new_anchor._dependencies.add(self)
        if "source_provider" in difference or "target_provider" in difference:
            source, target = self.effective_source, self.effective_target
            old_source_provider, new_source_provider = difference.pop(
                "source_provider",
                (source.provider, source.provider) if source else (None, None),
            )
            old_target_provider, new_target_provider = difference.pop(
                "target_provider",
                (target.provider, target.provider) if target else (None, None),
            )
            if old_source_provider and (old_source_provider is old_target_provider):
                self._deallocate(old_source_provider, dispose_only=dispose_only)
            if new_source_provider and (new_source_provider is new_target_provider):
                self._allocate(new_source_provider, target_node, add_action)
        elif self.provider and any(
            [
                "feedback" in difference,
                "source_bus" in difference,
                "source_channel_count" in difference,
                "target_bus" in difference,
                "target_channel_count" in difference,
            ]
        ):
            self._reallocate(difference)

    ### PUBLIC METHODS ###

    def serialize(self):
        serialized = super().serialize()
        if isinstance(self.target, Default):
            target = "default"
        else:
            target = str(self.effective_target.uuid)
        serialized["spec"]["target"] = target
        for mapping in [serialized["meta"], serialized.get("spec", {}), serialized]:
            for key in tuple(mapping):
                if not mapping[key]:
                    mapping.pop(key)
        return serialized

    ### PUBLIC PROPERTIES ###

    @property
    def effective_source(self):
        return self.source

    @property
    def effective_target(self):
        return self.target

    @property
    def feedback(self):
        source_anchor = self.source_anchor
        target_anchor = self.target_anchor
        if source_anchor is not None and target_anchor is not None:
            return target_anchor.graph_order < source_anchor.graph_order
        return None

    @property
    @abc.abstractmethod
    def source(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def source_anchor(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def source_bus(self):
        raise NotImplementedError

    @property
    def source_channel_count(self):
        effective_source = self.effective_source
        if effective_source:
            return effective_source.effective_channel_count
        return None

    @property
    def source_provider(self):
        effective_source = self.effective_source
        if effective_source:
            return effective_source.provider
        return None

    @property
    @abc.abstractmethod
    def target(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def target_anchor(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def target_bus(self):
        raise NotImplementedError

    @property
    def target_channel_count(self):
        effective_target = self.effective_target
        if effective_target:
            return effective_target.effective_channel_count
        return None

    @property
    def target_provider(self):
        effective_target = self.effective_target
        if effective_target:
            return effective_target.provider
        return None


class Send(Patch):

    ### INITIALIZER ###

    def __init__(self, target: Union[Allocatable, Default], *, name=None, uuid=None):
        if not isinstance(target, Default):
            if not hasattr(target, "send_target"):
                raise ValueError
        self._target = target
        Patch.__init__(self, name=name, uuid=uuid)

    ### PUBLIC METHODS ###

    @classmethod
    def build_synthdef(
        cls,
        source_channel_count,
        target_channel_count,
        *,
        feedback=False,
        calculation_rate=CalculationRate.AUDIO,
    ):
        return build_patch_synthdef(
            source_channel_count,
            target_channel_count,
            feedback=feedback,
            gain=True,
            calculation_rate=calculation_rate,
        )

    ### PUBLIC PROPERTIES ###

    @property
    def effective_source(self):
        return self.source

    @property
    def effective_target(self):
        if not isinstance(self.target, Default):
            return self.target
        for parent in self.parentage[1:]:
            if hasattr(parent, "default_send_target"):
                return parent.default_send_target
        return None

    @property
    def source(self):
        if self.parent and self.parent.parent:
            return self.parent.parent
        return None

    @property
    def source_anchor(self):
        return self

    @property
    def source_bus(self):
        source = self.effective_source
        if source:
            return source.audio_bus_proxies.get("output")
        return None

    @property
    def target(self):
        return self._target

    @property
    def target_anchor(self):
        effective_target = self.effective_target
        return effective_target.send_target if effective_target else None

    @property
    def target_bus(self):
        target = self.effective_target
        if not target:
            return None
        if self.feedback:
            return target.audio_bus_proxies.get("input")
        return target.audio_bus_proxies.get("output")


class Receive(Patch):

    ### INITIALIZER ###

    def __init__(self, source: Union[Allocatable, Default], *, name=None, uuid=None):
        if not isinstance(source, Default):
            if not hasattr(source, "receive_target"):
                raise ValueError
        self._source = source
        Patch.__init__(self, name=name, uuid=uuid)

    ### PUBLIC PROPERTIES ###

    @property
    def effective_source(self):
        if not isinstance(self.source, Default):
            return self.source
        for parent in self.parentage[1:]:
            if hasattr(parent, "default_receive_target"):
                return parent.default_receive_target
        return None

    @property
    def effective_target(self):
        return self.target

    @property
    def source(self):
        return self._source

    @property
    def source_anchor(self):
        effective_source = self.effective_source
        return effective_source.receive_target if effective_source else None

    @property
    def source_bus(self):
        source = self.effective_source
        if not source:
            return None
        return source.audio_bus_proxies.get("output")

    @property
    def target(self):
        if self.parent and self.parent.parent:
            return self.parent.parent
        return None

    @property
    def target_anchor(self):
        return self

    @property
    def target_bus(self):
        target = self.effective_target
        if target:
            return target.audio_bus_proxies.get("output")
        return None


class DirectIn(SendObject):

    ### INITIALIZER ###

    def __init__(
        self, source_bus_id: int, source_channel_count: int, *, name=None, uuid=None
    ):
        self._source_bus_id = int(source_bus_id)
        self._source_channel_count = int(source_channel_count)
        SendObject.__init__(self, name=name, uuid=uuid)

    ### PRIVATE METHODS ###

    def _allocate(self, provider, target_node, add_action):
        Allocatable._allocate(self, provider, target_node, add_action)
        self._node_proxies["node"] = provider.add_synth(
            in_=self.source_bus_id,
            out=self.parent.parent.audio_bus_proxies["output"],
            synthdef=self.build_synthdef(
                self.source_channel_count, self.effective_channel_count
            ),
            name=self.label,
            target_node=self.parent.node_proxy,
        )

    ### PUBLIC PROPERTIES ###

    @property
    def source_bus_id(self):
        return self._source_bus_id

    @property
    def source_channel_count(self):
        return self._source_channel_count


class DirectOut(SendObject):

    ### INITIALIZER ###

    def __init__(
        self, target_bus_id: int, target_channel_count: int, *, name=None, uuid=None
    ):
        self._target_bus_id = int(target_bus_id)
        self._target_channel_count = int(target_channel_count)
        SendObject.__init__(self, name=name, uuid=uuid)

    ### PRIVATE METHODS ###

    def _allocate(self, provider, target_node, add_action):
        Allocatable._allocate(self, provider, target_node, add_action)
        self._node_proxies["node"] = provider.add_synth(
            active=self.is_active,
            in_=self.parent.parent.audio_bus_proxies["output"],
            out=self.target_bus_id,
            synthdef=self.build_synthdef(
                self.effective_channel_count, self.target_channel_count
            ),
            name=self.label,
            target_node=self.parent.node_proxy,
        )

    def _reallocate(self, difference):
        Allocatable._reallocate(self, difference)
        node_proxy = self._node_proxies.pop("node")
        self._allocate(
            self.provider, target_node=node_proxy, add_action=AddAction.ADD_AFTER
        )
        node_proxy.free()

    ### PUBLIC METHODS ###

    def serialize(self):
        serialized = super().serialize()
        serialized["spec"].update(
            target_bus_id=self.target_bus_id,
            target_channel_count=self.target_channel_count,
        )
        for mapping in [serialized["meta"], serialized.get("spec", {}), serialized]:
            for key in tuple(mapping):
                value = mapping[key]
                if (isinstance(value, list) and not value) or value is None:
                    mapping.pop(key)
        return serialized

    ### PUBLIC PROPERTIES ###

    @property
    def target_bus_id(self):
        return self._target_bus_id

    @property
    def target_channel_count(self):
        return self._target_channel_count


class Target(ApplicationObject):

    ### INITIALIZER ###

    def __init__(self, *, label=None):
        ApplicationObject.__init__(self)
        self._dependencies: Set[Send] = set()
        self._label = label

    ### SPECIAL METHODS ###

    def __str__(self):
        return f"<{self.label} ({len(self._dependencies)})>"

    ### PUBLIC PROPERTIES ###

    @property
    def label(self):
        return self._label or type(self).__name__
