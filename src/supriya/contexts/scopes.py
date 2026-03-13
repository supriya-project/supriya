from threading import Lock
from typing import TYPE_CHECKING, Literal, cast

from ..enums import AddAction, CalculationRate, ServerLifecycleEvent
from ..exceptions import ServerOffline
from ..typing import AddActionLike
from ..ugens import SynthDef
from ..ugens.system import AMPLITUDE_SCOPE_SYNTHDEFS, FREQUENCY_SCOPE_SYNTHDEFS
from .entities import Bus, BusGroup, Node, ScopeBuffer, Synth

if TYPE_CHECKING:
    from .realtime import BaseServer, ServerLifecycleCallback


class BaseScope:
    """
    Base class for scopes.
    """

    def __init__(
        self,
        *,
        add_action: AddActionLike = AddAction.ADD_TO_TAIL,
        bus: Bus | BusGroup,
        context: "BaseServer",
        target_node: Node | None = None,
    ) -> None:
        if bus.context is not context:
            raise ValueError(bus, context)
        elif target_node and target_node.context is not context:
            raise ValueError(target_node, context)
        self.add_action = AddAction.from_expr(add_action)
        self.bus = bus
        self.channel_count = 0
        self.context = context
        self.lifecycle_callback: ServerLifecycleCallback | None = None
        self.lock = Lock()
        self.max_frames = 0
        self.scope_buffer: ScopeBuffer | None = None
        self.status: Literal["online", "offline"] = "offline"
        self.synth: Synth | None = None
        self.target_node: Node = target_node or self.context.root_node

    def _add_synth(self, scope_buffer: ScopeBuffer, synthdef: SynthDef) -> Synth:
        raise NotImplementedError

    def _get_synthdef(self) -> SynthDef:
        raise NotImplementedError

    def play(self) -> None:
        """
        Start the scope.
        """
        from .realtime import Server

        with self.lock:
            if self.status == "online":
                return
            if self.context._shared_memory is None:
                raise ValueError
            self.scope_buffer = self.context.add_scope_buffer()
            synthdef = self._get_synthdef()
            with self.context.at():
                with self.context.add_synthdefs(synthdef):
                    self.synth = self._add_synth(self.scope_buffer, synthdef)
            self.lifecycle_callback = cast(
                Server, self.context
            ).register_lifecycle_callback(
                event=[
                    ServerLifecycleEvent.OSC_PANICKED,
                    ServerLifecycleEvent.PROCESS_PANICKED,
                    ServerLifecycleEvent.QUITTING,
                ],
                once=True,
                procedure=lambda event: self.stop(),
            )
            self.status = "online"

    def read(self) -> tuple[int, list[float]]:
        """
        Read latest data from an online scope.
        """
        if not self.status == "online":
            raise ValueError
        elif self.context._shared_memory is None:
            raise ValueError
        elif self.scope_buffer is None:
            raise ValueError
        self.channel_count, self.max_frames = (
            self.context._shared_memory.describe_scope_buffer(int(self.scope_buffer))
        )
        return self.context._shared_memory.read_scope_buffer(int(self.scope_buffer))

    def stop(self) -> None:
        """
        Stop the scope.
        """
        with self.lock:
            if self.status == "offline":
                return
            if self.synth:
                try:
                    self.synth.free()
                except ServerOffline:
                    pass
                self.synth = None
            if self.scope_buffer:
                try:
                    self.scope_buffer.free()
                except ServerOffline:
                    pass
                self.scope_buffer = None
            if self.lifecycle_callback:
                self.context.unregister_lifecycle_callback(self.lifecycle_callback)
                self.lifecycle_callback = None
            self.status = "offline"


class AmplitudeScope(BaseScope):
    """
    An amplitude scope.
    """

    def _add_synth(self, scope_buffer: ScopeBuffer, synthdef: SynthDef) -> Synth:
        return self.context.add_synth(
            add_action=self.add_action,
            in_=int(self.bus),
            scope_id=int(scope_buffer),
            synthdef=synthdef,
            target_node=self.target_node,
        )

    def _get_synthdef(self) -> SynthDef:
        token = self.bus.calculation_rate.token
        if (
            channel_count := len(self.bus) if isinstance(self.bus, BusGroup) else 1
        ) > 16:
            raise ValueError(self.bus)
        return AMPLITUDE_SCOPE_SYNTHDEFS[f"supriya:amp-scope-{token}:{channel_count}"]


class FrequencyScope(BaseScope):
    """
    A frequency scope.
    """

    def __init__(
        self,
        *,
        add_action: AddActionLike = AddAction.ADD_TO_TAIL,
        bus: Bus | BusGroup,
        context: "BaseServer",
        fft_size: int = 4096,
        frequency_mode: Literal["linear", "logarithmic"] = "linear",
        rate: int = 4,
        target_node: Node | None = None,
    ) -> None:
        super().__init__(
            add_action=add_action,
            bus=bus,
            context=context,
            target_node=target_node,
        )
        if frequency_mode not in ("linear", "logarithmic"):
            raise ValueError(frequency_mode)
        elif self.bus.calculation_rate != CalculationRate.AUDIO:
            raise ValueError(bus.calculation_rate)
        elif fft_size < 256 or fft_size > 8192:
            raise ValueError(fft_size)
        self.fft_size = fft_size
        self.frequency_mode = frequency_mode
        self.rate = rate

    def _add_synth(self, scope_buffer: ScopeBuffer, synthdef: SynthDef) -> Synth:
        return self.context.add_synth(
            add_action=self.add_action,
            fft_buffer_size=self.fft_size,
            in_=int(self.bus),
            rate=self.rate,
            scope_id=int(scope_buffer),
            synthdef=synthdef,
            target_node=self.target_node,
        )

    def _get_synthdef(self) -> SynthDef:
        return FREQUENCY_SCOPE_SYNTHDEFS[
            f"supriya:freq-scope-{self.frequency_mode[:3]}-shm:1"
        ]
