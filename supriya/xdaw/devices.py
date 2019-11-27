from collections import deque
from typing import (
    Callable,
    Deque,
    Generator,
    List,
    Optional,
    Sequence,
    Tuple,
    Union,
)
from uuid import UUID, uuid4

import supriya.daw  # noqa
from supriya.commands.Request import Request
from supriya.enums import AddAction, CalculationRate
from supriya.midi import MidiMessage
from supriya.synthdefs import SynthDef, SynthDefFactory

from .bases import Allocatable
from .sends import Patch
from .synthdefs import build_patch_synthdef


class DeviceIn(Patch):

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
            calculation_rate=calculation_rate,
            replace_out=True,
        )

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        return self.parent.track_object if self.parent is not None else None

    @property
    def source_anchor(self):
        return self.source

    @property
    def source_bus(self):
        source = self.effective_source
        return source.audio_bus_proxies.get("output") if source is not None else None

    @property
    def target_bus(self):
        target = self.effective_target
        if target is not None:
            return target.audio_bus_proxies.get("output")
        return None

    @property
    def target(self):
        return self.parent

    @property
    def target_anchor(self):
        return self.target


class DeviceOut(Patch):

    ### PRIVATE METHODS ###

    def _allocate(self, provider, target_node, add_action):
        Allocatable._allocate(self, provider, target_node, add_action)
        self._allocate_synths(self.parent.node_proxy, AddAction.ADD_TO_TAIL)

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
            calculation_rate=calculation_rate,
            mix_out=True,
            hard_gate=True,
        )

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        return self.parent

    @property
    def source_anchor(self):
        return self.source

    @property
    def source_bus(self):
        source = self.effective_source
        if source is not None:
            return source.audio_bus_proxies.get("output")
        return None

    @property
    def target(self):
        return self.parent.track_object if self.parent is not None else None

    @property
    def target_anchor(self):
        return self.target

    @property
    def target_bus(self):
        target = self.effective_target
        return target.audio_bus_proxies.get("output") if target is not None else None


class DeviceObject(Allocatable):

    ### INITIALIZER ###

    def __init__(self, *, channel_count=None, name=None, uuid=None):
        Allocatable.__init__(self, channel_count=channel_count, name=name)
        self._uuid = uuid or uuid4()
        self._is_active = True
        self._ready = False
        self._event_handlers = {}

    ### SPECIAL METHODS ###

    def __str__(self):
        line = f"<{type(self).__name__} [...] {self.uuid}>"
        if self.node_proxy is not None:
            line = f"<{type(self).__name__} [{int(self.node_proxy)}] {self.uuid}>"
        lines = [line]
        for child in self:
            for line in str(child).splitlines():
                lines.append(f"    {line}")
        return "\n".join(lines)

    ### PRIVATE METHODS ###

    def _filter_in_midi_messages(self, in_midi_messages) -> Sequence[MidiMessage]:
        return []

    def _filter_out_midi_messages(self, out_midi_messages) -> Sequence[MidiMessage]:
        return []

    def _next_performer(self) -> Optional[Callable]:
        if self.parent is None:
            return None
        index = self.parent.index(self)
        if index < len(self.parent) - 1:
            return self.parent[index + 1]._perform
        for parent in self.parentage[1:]:
            if hasattr(parent, "_perform_output"):
                return parent._perform_output
        return None

    def _perform(
        self, moment, in_midi_messages
    ) -> Generator[
        Tuple[Optional[Callable], Sequence[MidiMessage], Sequence[Request]], None, None
    ]:
        next_performer = self._next_performer()
        if not self.ready:
            yield next_performer, in_midi_messages, ()
        out_midi_messages: List[MidiMessage] = []
        out_requests: List[Request] = []
        for message in self._filter_in_midi_messages(in_midi_messages):
            self._update_captures(moment, message, "I")
            event_handler = self._event_handlers.get(type(message))
            if not event_handler:
                out_midi_messages.append(message)
                continue
            messages, requests = event_handler(message)
            out_midi_messages.extend(messages)
            out_requests.extend(requests)
        for message in self._filter_out_midi_messages(out_midi_messages):
            self._update_captures(moment, message, "O")
        yield next_performer, out_midi_messages, out_requests

    @classmethod
    def _perform_loop(cls, moment, performer, midi_messages) -> Sequence[Request]:
        requests: List[Request] = []
        stack: Deque = deque()
        stack.append((performer, midi_messages))
        while stack:
            in_performer, in_messages = stack.popleft()
            for out_performer, out_messages, out_requests in in_performer(
                moment, in_messages
            ):
                requests.extend(out_requests)
                if out_messages and out_performer:
                    stack.append((out_performer, out_messages))
        return requests

    def _update_captures(self, moment, message, label):
        pass

    #    @abc.abstractmethod
    #    def _reallocate(self, difference):
    #        raise NotImplementedError

    ### PUBLIC METHODS ###

    def activate(self):
        with self.lock([self]):
            self._is_active = True

    def deactivate(self):
        with self.lock([self]):
            self._is_active = False

    def delete(self):
        with self.lock([self]):
            if self.parent is None:
                raise ValueError
            self.parent._remove(self)

    def duplicate(self):
        pass

    @classmethod
    def group(cls, devices):
        with cls.lock(devices):
            pass

    def move(self, container, position):
        with self.lock([self, container]):
            container.devices._mutate(slice(position, position), [self])

    ### PUBLIC PROPERTIES ###

    @property
    def is_active(self):
        return self._is_active

    @property
    def ready(self):
        return self._ready

    @property
    def track_object(self):
        from .tracks import TrackObject

        for parent in self.parentage[1:]:
            if isinstance(parent, TrackObject):
                return parent
        return None

    @property
    def uuid(self) -> UUID:
        return self._uuid


class AudioEffect(DeviceObject):

    ### INITIALIZER ###

    def __init__(
        self,
        synthdef: Union[SynthDef, SynthDefFactory],
        *,
        name=None,
        synthdef_kwargs=None,
        synthdef_parameters=None,
        uuid=None,
    ):
        DeviceObject.__init__(self, name=name, uuid=uuid)
        self._synthdef = synthdef
        self._synthdef_kwargs = dict(synthdef_kwargs or {})
        self._parameters.update(**(synthdef_parameters or {}))
        self._device_in = DeviceIn()
        self._device_out = DeviceOut()
        self._mutate(slice(None), [self._device_in, self._device_out])

    ### PRIVATE METHODS ###

    def _allocate(self, provider, target_node, add_action):
        Allocatable._allocate(self, provider, target_node, add_action)
        channel_count = self.effective_channel_count
        self._node_proxies["node"] = provider.add_group(
            target_node=target_node, add_action=add_action, name=self.label
        )
        self._node_proxies["parameters"] = provider.add_group(
            target_node=self.node_proxy,
            add_action=AddAction.ADD_TO_HEAD,
            name="Parameters",
        )
        self._node_proxies["body"] = provider.add_group(
            target_node=self.node_proxy, add_action=AddAction.ADD_TO_TAIL, name="Body"
        )
        self._allocate_audio_buses(provider, channel_count)
        self._allocate_synths(
            provider,
            self.effective_channel_count,
            synth_pair=(self.node_proxies["body"], AddAction.ADD_TO_HEAD),
        )

    def _allocate_audio_buses(self, provider, channel_count):
        self._audio_bus_proxies["output"] = provider.add_bus_group(
            calculation_rate=CalculationRate.AUDIO, channel_count=channel_count
        )

    def _allocate_synths(self, provider, channel_count, *, synth_pair=None):
        synthdef = self.synthdef
        if isinstance(synthdef, SynthDefFactory):
            synthdef = synthdef.build(channel_count=self.effective_channel_count)
        synth_target, synth_action = synth_pair
        self._node_proxies["synth"] = provider.add_synth(
            add_action=synth_action,
            synthdef=synthdef,
            target_node=synth_target,
            out=self.audio_bus_proxies["output"],
            **self.synthdef_kwargs,
        )

    def _free_audio_buses(self):
        self._audio_bus_proxies.pop("output").free()

    def _reallocate(self, difference):
        channel_count = self.effective_channel_count
        synth_synth = self._node_proxies.pop("synth")
        self._free_audio_buses()
        self._allocate_audio_buses(self.provider, channel_count)
        self._allocate_synths(
            self.provider,
            self.effective_channel_count,
            synth_pair=(synth_synth, AddAction.ADD_AFTER),
        )
        synth_synth.free()

    ### PUBLIC METHODS ###

    def set_channel_count(self, channel_count: Optional[int]):
        with self.lock([self]):
            if channel_count is not None:
                assert 1 <= channel_count <= 8
                channel_count = int(channel_count)
            self._set(channel_count=channel_count)

    ### PUBLIC PROPERTIES ###

    @property
    def device_in(self):
        return self._device_in

    @property
    def device_out(self):
        return self._device_out

    @property
    def synthdef(self) -> Union[SynthDef, SynthDefFactory]:
        return self._synthdef

    @property
    def synthdef_kwargs(self):
        return self._synthdef_kwargs


class Instrument(DeviceObject):

    ### INITIALIZER ###

    def __init__(
        self, synthdef: Union[SynthDef, SynthDefFactory], *, name=None, uuid=None
    ):
        # TODO: Polyphony Limit
        # TODO: Polyphony Mode
        DeviceObject.__init__(self, name=name, uuid=uuid)
        self._synthdef = synthdef

    ### PUBLIC METHODS ###

    def set_channel_count(self, channel_count: Optional[int]):
        with self.lock([self]):
            if channel_count is not None:
                assert 1 <= channel_count <= 8
                channel_count = int(channel_count)
            self._set(channel_count=channel_count)

    ### PRIVATE METHODS ###

    def _allocate(self, provider, target_node, add_action):
        Allocatable._allocate(self, provider, target_node, add_action)
        self._node_proxies["node"] = provider.add_group(
            target_node=target_node, add_action=add_action, name=self.label
        )
        self._node_proxies["parameters"] = provider.add_group(
            target_node=self.node_proxy,
            add_action=AddAction.ADD_TO_HEAD,
            name="Parameters",
        )
        self._node_proxies["body"] = provider.add_group(
            target_node=self.node_proxy, add_action=AddAction.ADD_TO_TAIL, name="Body"
        )

    ### PUBLIC PROPERTIES ###

    @property
    def synthdef(self) -> Union[SynthDef, SynthDefFactory]:
        return self._synthdef
