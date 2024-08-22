"""
Tools for interacting with realtime execution contexts.
"""

import asyncio
import concurrent.futures
import enum
import logging
import warnings
from collections.abc import Sequence as SequenceABC
from typing import (
    TYPE_CHECKING,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Sequence,
    Set,
    SupportsInt,
    Type,
    Union,
    cast,
)

from uqbar.objects import new

from ..assets.synthdefs import system_synthdefs
from ..enums import CalculationRate
from ..exceptions import (
    OwnedServerShutdown,
    ServerCannotBoot,
    ServerOffline,
    ServerOnline,
    TooManyClients,
    UnownedServerShutdown,
)
from ..osc import (
    AsyncOscProtocol,
    HealthCheck,
    OscBundle,
    OscMessage,
    OscProtocol,
    OscProtocolOffline,
    ThreadedOscProtocol,
)
from ..scsynth import (
    AsyncProcessProtocol,
    Options,
    ProcessProtocol,
    SyncProcessProtocol,
)
from ..typing import FutureLike, SupportsOsc
from ..ugens import SynthDef
from .core import (
    BootStatus,
    Buffer,
    Bus,
    Context,
    ContextObject,
    Group,
    InvalidCalculationRate,
    Node,
    Synth,
)
from .requests import (
    DumpTree,
    GetBuffer,
    GetBufferRange,
    GetControlBus,
    GetControlBusRange,
    GetSynthControl,
    GetSynthControlRange,
    QueryBuffer,
    QueryNode,
    QueryStatus,
    QueryTree,
    QueryVersion,
    Quit,
    Sync,
    ToggleNotifications,
)
from .responses import (
    BufferInfo,
    DoneInfo,
    FailInfo,
    GetBufferInfo,
    GetBufferRangeInfo,
    GetControlBusInfo,
    GetControlBusRangeInfo,
    GetNodeControlInfo,
    GetNodeControlRangeInfo,
    NodeInfo,
    QueryTreeGroup,
    QueryTreeInfo,
    QueryTreeSynth,
    StatusInfo,
    VersionInfo,
)

if TYPE_CHECKING:
    from ..realtime.shm import ServerSHM

logger = logging.getLogger(__name__)


class FailWarning(Warning):
    pass


warnings.simplefilter("always", FailWarning)


DEFAULT_HEALTHCHECK = HealthCheck(
    active=False,
    backoff_factor=1.5,
    max_attempts=5,
    request_pattern=["/status"],
    response_pattern=["/status.reply"],
    timeout=1.0,
)


class ServerLifecycleEvent(enum.Enum):
    BOOTING = enum.auto()
    PROCESS_BOOTED = enum.auto()
    CONNECTING = enum.auto()
    OSC_CONNECTED = enum.auto()
    CONNECTED = enum.auto()
    BOOTED = enum.auto()
    OSC_PANICKED = enum.auto()
    PROCESS_PANICKED = enum.auto()
    QUITTING = enum.auto()
    DISCONNECTING = enum.auto()
    OSC_DISCONNECTED = enum.auto()
    DISCONNECTED = enum.auto()
    PROCESS_QUIT = enum.auto()
    QUIT = enum.auto()


class BaseServer(Context):
    """
    Base class for realtime execution contexts.

    :param options: The context's options.
    :param kwargs: Keyword arguments for options.
    """

    ### CLASS VARIABLES ###

    _contexts: Set["BaseServer"] = set()

    ### INITIALIZER ###

    def __init__(
        self,
        boot_future: FutureLike[bool],
        exit_future: FutureLike[bool],
        options: Optional[Options],
        osc_protocol: OscProtocol,
        process_protocol: ProcessProtocol,
        name: Optional[str] = None,
        **kwargs,
    ) -> None:
        super().__init__(options, name=name, **kwargs)
        self._boot_future = boot_future
        self._boot_status = BootStatus.OFFLINE
        self._buffers: Set[int] = set()
        self._exit_future = exit_future
        self._is_owner = False
        self._latency = 0.1
        self._lifecycle_event_callbacks: Dict[ServerLifecycleEvent, List[Callable]] = {}
        self._maximum_logins = 1
        self._node_active: Dict[int, bool] = {}
        self._node_children: Dict[int, List[int]] = {}
        self._node_parents: Dict[int, int] = {}
        self._osc_protocol = osc_protocol
        self._process_protocol = process_protocol
        self._setup_osc_callbacks()
        self._shm: Optional["ServerSHM"] = None
        self._status: Optional[StatusInfo] = None

    ### SPECIAL METHODS ###

    def __contains__(self, object_: ContextObject) -> bool:
        if object_.context is not self:
            return False
        if self.boot_status != BootStatus.ONLINE:
            return False
        if isinstance(object_, Node) and (
            object_.id_ in self._node_parents or object_.id_ == 0
        ):
            return True
        if isinstance(object_, Buffer) and object_.id_ in self._buffers:
            return True
        if isinstance(object_, Bus):
            if object_.calculation_rate == CalculationRate.AUDIO and (
                object_.id_ < self.options.control_bus_channel_count
            ):
                return True
            elif object_.calculation_rate == CalculationRate.CONTROL and (
                object_.id_ < self.options.audio_bus_channel_count
            ):
                return True
        return False

    ### PRIVATE METHODS ###

    def _add_node_to_children(
        self, id_: int, parent_id: int, previous_id: int, next_id: int
    ) -> None:
        self._node_parents[id_] = parent_id
        children = self._node_children[parent_id]
        if previous_id == -1:
            children.insert(0, id_)
        elif next_id == -1:
            children.append(id_)
        elif previous_id in children:
            children.insert(children.index(previous_id) + 1, id_)
        elif next_id in children:
            children.insert(children.index(next_id), id_)

    def _free_id(
        self,
        type_: Type[ContextObject],
        id_: int,
        calculation_rate: Optional[CalculationRate] = None,
    ) -> None:
        self._get_allocator(type_, calculation_rate).free(id_)

    def _handle_done_b_alloc(self, message: OscMessage) -> None:
        with self._lock:
            self._buffers.add(message.contents[1])

    def _handle_done_b_alloc_read(self, message: OscMessage) -> None:
        with self._lock:
            self._buffers.add(message.contents[1])

    def _handle_done_b_alloc_read_channel(self, message: OscMessage) -> None:
        with self._lock:
            self._buffers.add(message.contents[1])

    def _handle_done_b_free(self, message: OscMessage) -> None:
        with self._lock:
            if message.contents[1] in self._buffers:
                self._buffers.remove(message.contents[1])
            self._free_id(Buffer, message.contents[1])

    def _handle_done_quit(self, message: OscMessage):
        raise NotImplementedError

    def _handle_fail(self, message: OscMessage) -> None:
        warnings.warn(" ".join(str(x) for x in message.contents), FailWarning)

    def _handle_n_end(self, message: OscMessage) -> None:
        with self._lock:
            id_, parent_id, *_ = message.contents
            if parent_id == -1:
                parent_id = self._node_parents.get(id_)
            if parent_id is not None:
                self._remove_node_from_children(id_, parent_id)
            self._free_id(Node, id_)
            self._node_active.pop(id_, None)
            self._node_children.pop(id_, None)
            self._node_parents.pop(id_, None)

    def _handle_n_go(self, message: OscMessage) -> None:
        with self._lock:
            id_, parent_id, previous_id, next_id, is_group, *_ = message.contents
            self._node_parents[id_] = parent_id
            self._node_active[id_] = True
            if is_group:
                self._node_children[id_] = []
            self._add_node_to_children(id_, parent_id, previous_id, next_id)

    def _handle_n_move(self, message: OscMessage) -> None:
        with self._lock:
            id_, parent_id, previous_id, next_id, *_ = message.contents
            old_parent_id = self._node_parents[id_]
            self._remove_node_from_children(id_, old_parent_id)
            self._add_node_to_children(id_, parent_id, previous_id, next_id)

    def _handle_n_off(self, message: OscMessage) -> None:
        with self._lock:
            self._node_active[message.contents[0]] = False

    def _handle_n_on(self, message: OscMessage) -> None:
        with self._lock:
            self._node_active[message.contents[0]] = True

    def _handle_status_reply(self, message: OscMessage):
        with self._lock:
            self._status = cast(StatusInfo, StatusInfo.from_osc(message))

    def _on_lifecycle_event(self, event: ServerLifecycleEvent) -> None:
        for callback in self._lifecycle_event_callbacks.get(event, []):
            if asyncio.iscoroutine(result := callback(event)):
                asyncio.get_running_loop().create_task(result)

    def _remove_node_from_children(self, id_: int, parent_id: int) -> None:
        if not (children := self._node_children.get(parent_id, [])):
            return
        try:
            children.pop(children.index(id_))
        except ValueError:
            pass

    def _resolve_node(self, node: Union[Node, SupportsInt, None]) -> int:
        if node is None:
            return self._client_id + 1
        return int(node)

    def _setup_osc_callbacks(self) -> None:
        for pattern, procedure in [
            (["/done", "/b_alloc"], self._handle_done_b_alloc),
            (["/done", "/b_allocRead"], self._handle_done_b_alloc_read),
            (["/done", "/b_allocReadChannel"], self._handle_done_b_alloc_read_channel),
            (["/done", "/b_free"], self._handle_done_b_free),
            (["/done", "/quit"], self._handle_done_quit),
            (["/fail"], self._handle_fail),
            (["/n_end"], self._handle_n_end),
            (["/n_go"], self._handle_n_go),
            (["/n_move"], self._handle_n_move),
            (["/n_off"], self._handle_n_off),
            (["/n_on"], self._handle_n_on),
            (["/status.reply"], self._handle_status_reply),
        ]:
            self._osc_protocol.register(pattern=pattern, procedure=procedure)

    def _setup_shm(self) -> None:
        try:
            from ..realtime.shm import ServerSHM

            self._shm = ServerSHM(
                self._options.port, self._options.control_bus_channel_count
            )
        except (ImportError, ModuleNotFoundError):
            pass

    def _setup_system(self) -> None:
        self._node_children[0] = []
        with self.at():
            for i in range(self._maximum_logins):
                self.add_group(permanent=True, add_action="ADD_TO_TAIL", target_node=0)
        for name in dir(system_synthdefs):
            synthdef = getattr(system_synthdefs, name)
            if isinstance(synthdef, SynthDef):
                with self.at():
                    self.add_synthdefs(synthdef)

    def _teardown_shm(self) -> None:
        self._shm = None

    def _teardown_state(self) -> None:
        self._node_active.clear()
        self._node_children.clear()
        self._node_parents.clear()
        self._buffers.clear()

    def _validate_can_request(self) -> None:
        if self._boot_status not in (BootStatus.BOOTING, BootStatus.ONLINE):
            raise ServerOffline
        pass  # Otherwise always OK to request in RT

    def _validate_moment_timestamp(self, seconds: Optional[float]) -> None:
        pass  # Floats and None are OK in RT

    ### PUBLIC METHODS ###

    def on(
        self,
        event: Union[ServerLifecycleEvent, Iterable[ServerLifecycleEvent]],
        callback: Callable[[ServerLifecycleEvent], None],
    ) -> None:
        if isinstance(event, ServerLifecycleEvent):
            events_ = [event]
        else:
            events_ = list(set(event))
        for event_ in events_:
            if callback not in (
                callbacks := self._lifecycle_event_callbacks.setdefault(event_, [])
            ):
                callbacks.append(callback)

    def send(
        self, message: Union[OscMessage, OscBundle, SupportsOsc, SequenceABC, str]
    ) -> None:
        """
        Send a message to the execution context.

        :param message: The message to send.
        """
        if self._boot_status == BootStatus.OFFLINE:
            raise ServerOffline
        self._osc_protocol.send(
            message.to_osc() if isinstance(message, SupportsOsc) else message
        )

    def set_latency(self, latency: float) -> None:
        """
        Set the context's latency.

        :param latency: The latency in seconds.
        """
        self._latency = float(latency)

    ### PUBLIC PROPERTIES ###

    @property
    def boot_future(self) -> FutureLike[bool]:
        """
        Get the server's boot future.

        Only reference this _after_ booting or connecting, as the future is
        created when booting or connecting.
        """
        return self._boot_future

    @property
    def default_group(self) -> Group:
        """
        Get the server's default group.
        """
        return Group(context=self, id_=self._client_id + 1)

    @property
    def exit_future(self) -> FutureLike[bool]:
        """
        Get the server's exit future.

        Only reference this _after_ booting or connecting, as the future is
        created when booting or connecting.
        """
        return self._exit_future

    @property
    def is_owner(self) -> bool:
        """
        Get the server's ownership flag.
        """
        return self._is_owner

    @property
    def osc_protocol(self) -> OscProtocol:
        """
        Get the server's OSC protocol.
        """
        return self._osc_protocol

    @property
    def process_protocol(self) -> ProcessProtocol:
        """
        Get the server's process protocol.
        """
        return self._process_protocol

    @property
    def status(self) -> Optional[StatusInfo]:
        """
        Get the server's last received status.
        """
        return self._status


class Server(BaseServer):
    """
    A realtime execution context with :py:mod:`threading`-based OSC and process protocols.

    :param options: The context's options.
    :param kwargs: Keyword arguments for options.
    """

    ### INITIALIZER ###

    def __init__(
        self,
        options: Optional[Options] = None,
        name: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(
            boot_future=concurrent.futures.Future(),
            exit_future=concurrent.futures.Future(),
            name=name,
            options=options,
            osc_protocol=ThreadedOscProtocol(
                name=name,
                on_connect_callback=lambda: self._on_lifecycle_event(
                    ServerLifecycleEvent.OSC_CONNECTED,
                ),
                on_disconnect_callback=lambda: self._on_lifecycle_event(
                    ServerLifecycleEvent.OSC_DISCONNECTED,
                ),
                on_panic_callback=self._on_osc_panicked,
            ),
            process_protocol=SyncProcessProtocol(
                name=name,
                on_boot_callback=lambda: self._on_lifecycle_event(
                    ServerLifecycleEvent.PROCESS_BOOTED
                ),
                on_panic_callback=lambda: self._on_lifecycle_event(
                    ServerLifecycleEvent.PROCESS_PANICKED
                ),
                on_quit_callback=lambda: self._on_lifecycle_event(
                    ServerLifecycleEvent.PROCESS_QUIT
                ),
            ),
            **kwargs,
        )

    ### PRIVATE METHODS ###

    def _connect(self) -> None:
        logger.info(
            f"[{self._options.ip_address}:{self._options.port}/{self.name or hex(id(self))}] "
            "connecting ..."
        )
        self._on_lifecycle_event(ServerLifecycleEvent.CONNECTING)
        cast(ThreadedOscProtocol, self._osc_protocol).connect(
            ip_address=self._options.ip_address,
            port=self._options.port,
            healthcheck=DEFAULT_HEALTHCHECK,
        )
        self._setup_notifications()
        self._contexts.add(self)
        self._osc_protocol.activate_healthcheck()
        self._setup_allocators()
        if self._client_id == 0:
            self._setup_system()
            self.sync()
        self._osc_protocol.boot_future.result()
        logger.info(
            f"[{self._options.ip_address}:{self._options.port}/{self.name or hex(id(self))}] "
            "... connected!"
        )
        self._boot_status = BootStatus.ONLINE
        if not self.is_owner:
            self._boot_future.set_result(True)
        self._on_lifecycle_event(ServerLifecycleEvent.CONNECTED)

    def _disconnect(self) -> None:
        logger.info(
            f"[{self._options.ip_address}:{self._options.port}/{self.name or hex(id(self))}] "
            "disconnecting ..."
        )
        self._on_lifecycle_event(ServerLifecycleEvent.DISCONNECTING)
        self._osc_protocol.disconnect()
        self._teardown_shm()
        self._teardown_state()
        if self in self._contexts:
            self._contexts.remove(self)
        was_owner = self._is_owner = True
        self._is_owner = False
        logger.info(
            f"[{self._options.ip_address}:{self._options.port}/{self.name or hex(id(self))}] "
            "... disconnected!"
        )
        self._boot_status = BootStatus.OFFLINE
        self._on_lifecycle_event(ServerLifecycleEvent.DISCONNECTED)
        if not was_owner:
            if not self._boot_future.done():
                self._boot_future.set_result(True)
            if not self._exit_future.done():
                self._exit_future.set_result(True)

    def _handle_done_quit(self, message: OscMessage) -> None:
        logger.info(
            f"[{self._options.ip_address}:{self._options.port}/{self.name or hex(id(self))}] "
            f"handling {message.to_list()} ..."
        )
        if self._boot_status == BootStatus.ONLINE:
            self._shutdown()
        else:
            logger.info(
                f"[{self._options.ip_address}:{self._options.port}/{self.name or hex(id(self))}] "
                f"... already quitting!"
            )

    def _on_osc_panicked(self) -> None:
        self._on_lifecycle_event(ServerLifecycleEvent.OSC_PANICKED)
        self._shutdown()
        if not self._exit_future.done():
            self._exit_future.set_result(False)

    def _setup_notifications(self) -> None:
        logger.info(
            f"[{self._options.ip_address}:{self._options.port}/{self.name or hex(id(self))}] "
            "setting up notifications ..."
        )
        response = ToggleNotifications(True).communicate(server=self)
        if response is None or not isinstance(response, (DoneInfo, FailInfo)):
            raise RuntimeError
        if isinstance(response, FailInfo):
            self._shutdown()
            raise TooManyClients
        if len(response.other) == 1:  # supernova doesn't provide a max logins value
            self._client_id = int(response.other[0])
            self._maximum_logins = self._options.maximum_logins
        else:
            self._client_id = int(response.other[0])
            self._maximum_logins = int(response.other[1])

    def _shutdown(self):
        if self.is_owner:
            self.quit()
        else:
            self.disconnect()

    ### PUBLIC METHODS ###

    def boot(self, *, options: Optional[Options] = None, **kwargs) -> "Server":
        """
        Boot the server.

        :param options: The context's options.
        :param kwargs: Keyword arguments for options.
        """
        if self._boot_status != BootStatus.OFFLINE:
            raise ServerOnline
        logger.info(
            f"[{self._options.ip_address}:{self._options.port}/{self.name or hex(id(self))}] "
            "booting ..."
        )
        self._boot_future = concurrent.futures.Future()
        self._exit_future = concurrent.futures.Future()
        self._boot_status = BootStatus.BOOTING
        self._on_lifecycle_event(ServerLifecycleEvent.BOOTING)
        self._options = new(options or self._options, **kwargs)
        logger.debug(
            f"[{self._options.ip_address}:{self._options.port}/{self.name or hex(id(self))}] "
            f"options: {self._options}"
        )
        try:
            cast(SyncProcessProtocol, self._process_protocol).boot(self._options)
        except ServerCannotBoot:
            if not self._boot_future.done():
                self._boot_future.set_result(False)
                self._exit_future.set_result(False)
            self._boot_status = BootStatus.OFFLINE
            raise
        self._is_owner = True
        self._setup_shm()
        self._connect()
        logger.info(
            f"[{self._options.ip_address}:{self._options.port}/{self.name or hex(id(self))}] "
            "... booted!"
        )
        if self.is_owner:
            self._boot_future.set_result(True)
        self._on_lifecycle_event(ServerLifecycleEvent.BOOTED)
        return self

    def connect(self, *, options: Optional[Options] = None, **kwargs) -> "Server":
        """
        Connect to a running server.

        :param options: The context's options.
        :param kwargs: Keyword arguments for options.
        """
        if self._boot_status != BootStatus.OFFLINE:
            raise ServerOnline
        self._boot_future = concurrent.futures.Future()
        self._exit_future = concurrent.futures.Future()
        self._boot_status = BootStatus.BOOTING
        self._options = new(options or self._options, **kwargs)
        self._is_owner = False
        self._connect()
        return self

    def disconnect(self) -> "Server":
        """
        Disconnect from a running server.
        """
        if self._boot_status == BootStatus.OFFLINE:
            raise ServerOffline
        if self._is_owner:
            raise OwnedServerShutdown("Cannot disconnect from owned server.")
        self._boot_status = BootStatus.QUITTING
        self._disconnect()
        return self

    def dump_tree(
        self,
        group: Optional[Group] = None,
        include_controls: bool = True,
        sync: bool = True,
    ) -> Optional[QueryTreeGroup]:
        """
        Dump the server's node tree.

        Emit ``/g_dumpTree`` requests.

        :param group: The group whose tree to query. Defaults to the root node.
        :param include_controls: Flag for including synth control values.
        :param sync: If true, communicate the request immediately. Otherwise bundle it
            with the current request context.
        """
        self._validate_can_request()
        request = DumpTree(items=[(group or self.root_node, bool(include_controls))])
        if sync:
            with self.process_protocol.capture() as transcript:
                request.communicate(server=self)
                self.sync(timeout=10.0)
                return QueryTreeGroup.from_string("\n".join(transcript.lines))
        self._add_requests(request)
        return None

    def get_buffer(
        self, buffer: Buffer, *indices: int, sync: bool = True
    ) -> Optional[Dict[int, float]]:
        """
        Get a buffer sample.

        Emit ``/b_get`` requests.

        :param buffer: The buffer whose sample to get.
        :param indices: The sample indices to read.
        :param sync: If true, communicate the request immediately. Otherwise bundle it
            with the current request context.
        """
        request = GetBuffer(buffer_id=buffer, indices=indices)
        if sync:
            return dict(cast(GetBufferInfo, request.communicate(server=self)).items)
        self._add_requests(request)
        return None

    def get_buffer_range(
        self, buffer: Buffer, index: int, count: int, sync: bool = True
    ) -> Optional[Sequence[float]]:
        """
        Get a buffer sample range.

        Emit ``/b_getn`` requests.

        :param buffer: The buffer whose samples to get.
        :param index: The sample index to start reading at.
        :param count: The number of samples to read.
        :param sync: If true, communicate the request immediately. Otherwise bundle it
            with the current request context.
        """
        request = GetBufferRange(buffer_id=buffer, items=[(index, count)])
        if sync:
            return cast(GetBufferRangeInfo, request.communicate(server=self)).items[0][
                -1
            ]
        self._add_requests(request)
        return None

    def get_bus(self, bus: Bus, sync: bool = True) -> Optional[float]:
        """
        Get a control bus value.

        Emit ``/c_get`` requests.

        :param bus: The control bus whose value to get.
        :param sync: If true, communicate the request immediately. Otherwise bundle it
            with the current request context.
        """
        if bus.calculation_rate != CalculationRate.CONTROL:
            raise InvalidCalculationRate
        request = GetControlBus(bus_ids=[bus.id_])
        if sync:
            return cast(GetControlBusInfo, request.communicate(server=self)).items[0][
                -1
            ]
        self._add_requests(request)
        return None

    def get_bus_range(
        self, bus: Bus, count: int, sync: bool = True
    ) -> Optional[Sequence[float]]:
        """
        Get a range of control bus values.

        Emit ``/c_getn`` requests.

        :param bus: The control bus to start reading at.
        :param count: The number of contiguous buses whose values to get.
        :param sync: If true, communicate the request immediately. Otherwise bundle it
            with the current request context.
        """
        if bus.calculation_rate != CalculationRate.CONTROL:
            raise InvalidCalculationRate
        request = GetControlBusRange(items=[(bus.id_, count)])
        if sync:
            return cast(GetControlBusRangeInfo, request.communicate(server=self)).items[
                0
            ][-1]
        self._add_requests(request)
        return None

    def get_synth_controls(
        self, synth: Synth, *controls: Union[int, str], sync: bool = True
    ) -> Optional[Dict[Union[int, str], float]]:
        """
        Get a synth control.

        Emit ``/s_get`` requests.

        :param synth: The synth whose control to get.
        :param controls: The controls to get.
        :param sync: If true, communicate the request immediately. Otherwise bundle it
            with the current request context.
        """
        request = GetSynthControl(synth_id=synth, controls=controls)
        if sync:
            return dict(
                cast(GetNodeControlInfo, request.communicate(server=self)).items
            )
        self._add_requests(request)
        return None

    def get_synth_control_range(
        self, synth: Synth, control: Union[int, str], count: int, sync: bool = True
    ) -> Optional[Sequence[Union[float, str]]]:
        """
        Get a range of synth controls.

        Emit ``/s_getn`` requests.

        :param synth: The synth whose control to get.
        :param control: The control to start reading at.
        :param count: The number of contiguous controls to get.
        :param sync: If true, communicate the request immediately. Otherwise bundle it
            with the current request context.
        """
        request = GetSynthControlRange(synth_id=synth, items=[(control, count)])
        if sync:
            return cast(
                GetNodeControlRangeInfo, request.communicate(server=self)
            ).items[0][-1]
        self._add_requests(request)
        return None

    def query_buffer(self, buffer: Buffer, sync: bool = True) -> Optional[BufferInfo]:
        """
        Query a buffer.

        Emit ``/b_query`` requests.

        :param buffer: The buffer to query.
        :param sync: If true, communicate the request immediately. Otherwise bundle it
            with the current request context.
        """
        request = QueryBuffer(buffer_ids=[buffer.id_])
        if sync:
            return cast(BufferInfo, request.communicate(server=self))
        self._add_requests(request)
        return None

    def query_node(self, node: Node, sync: bool = True) -> Optional[NodeInfo]:
        """
        Query a node.

        Emit ``/n_query`` requests.

        :param node: The node to query.
        :param sync: If true, communicate the request immediately. Otherwise bundle it
            with the current request context.
        """
        request = QueryNode(node_ids=[node.id_])
        if sync:
            return cast(NodeInfo, request.communicate(server=self))
        self._add_requests(request)
        return None

    def query_status(self, sync: bool = True) -> Optional[StatusInfo]:
        """
        Query the server's status.

        Emit ``/status`` requests.

        :param sync: If true, communicate the request immediately. Otherwise bundle it
            with the current request context.
        """
        request = QueryStatus()
        if sync:
            return cast(StatusInfo, request.communicate(server=self))
        self._add_requests(request)
        return None

    def query_tree(
        self,
        group: Optional[Group] = None,
        include_controls: bool = True,
        sync: bool = True,
    ) -> Optional[Union[QueryTreeGroup, QueryTreeSynth]]:
        """
        Query the server's node tree.

        Emit ``/g_queryTree`` requests.

        :param group: The group whose tree to query. Defaults to the root node.
        :param include_controls: Flag for including synth control values.
        :param sync: If true, communicate the request immediately. Otherwise bundle it
            with the current request context.
        """
        request = QueryTree(items=[(group or 0, include_controls)])
        if sync:
            return QueryTreeGroup.from_query_tree_info(
                cast(QueryTreeInfo, request.communicate(server=self))
            )
        self._add_requests(request)
        return None

    def query_version(self, sync: bool = True) -> Optional[VersionInfo]:
        """
        Query the server's version.

        Emit ``/version`` requests.

        :param sync: If true, communicate the request immediately. Otherwise bundle it
            with the current request context.
        """
        request = QueryVersion()
        if sync:
            return cast(VersionInfo, request.communicate(server=self))
        self._add_requests(request)
        return None

    def quit(self, force: bool = False) -> "Server":
        """
        Quit the server.

        Emit ``/quit`` requests.

        :param force: Force the server to quit, even if this client doesn't own the
            process.
        """
        if self._boot_status != BootStatus.ONLINE:
            return self
        if not self._is_owner and not force:
            raise UnownedServerShutdown(
                "Cannot quit unowned server without force flag."
            )
        logger.info(
            f"[{self._options.ip_address}:{self._options.port}/{self.name or hex(id(self))}] "
            "quitting ..."
        )
        self._boot_status = BootStatus.QUITTING
        self._on_lifecycle_event(ServerLifecycleEvent.QUITTING)
        try:
            Quit().communicate(server=self)
        except OscProtocolOffline:
            pass
        self._disconnect()
        cast(SyncProcessProtocol, self._process_protocol).quit()
        logger.info(
            f"[{self._options.ip_address}:{self._options.port}/{self.name or hex(id(self))}] "
            "... quit!"
        )
        self._on_lifecycle_event(ServerLifecycleEvent.QUIT)
        if not self._boot_future.done():
            self._boot_future.set_result(True)
        if not self._exit_future.done():
            self._exit_future.set_result(True)
        return self

    def reboot(self) -> "Server":
        """
        Reboot the server.
        """
        self.quit()
        self.boot()
        return self

    def reset(self) -> "Server":
        """
        Reset the server's state without quitting.
        """
        with self.at():
            self.clear_schedule()
            self.free_group_children(self.root_node)
            self.free_all_synthdefs()
        self.sync()
        self._teardown_state()
        self._setup_allocators()
        self._setup_system()
        self.sync()
        return self

    def sync(self, sync_id: Optional[int] = None, timeout: float = 1.0) -> "Server":
        """
        Sync the server.

        Emit ``/sync`` requests.

        :param sync_id: The sync ID to wait on.
        """
        if self._boot_status not in (BootStatus.BOOTING, BootStatus.ONLINE):
            raise ServerOffline
        Sync(
            sync_id=sync_id if sync_id is not None else self._get_next_sync_id()
        ).communicate(server=self, timeout=timeout)
        return self


class AsyncServer(BaseServer):
    """
    A realtime execution context with :py:mod:`asyncio`-based OSC and process protocols.

    :param options: The context's options.
    :param kwargs: Keyword arguments for options.
    """

    ### INITIALIZER ###

    def __init__(
        self, options: Optional[Options] = None, name: Optional[str] = None, **kwargs
    ):
        super().__init__(
            boot_future=asyncio.Future(),
            exit_future=asyncio.Future(),
            name=name,
            options=options,
            osc_protocol=AsyncOscProtocol(
                name=name,
                on_connect_callback=lambda: self._on_lifecycle_event(
                    ServerLifecycleEvent.OSC_CONNECTED,
                ),
                on_disconnect_callback=lambda: self._on_lifecycle_event(
                    ServerLifecycleEvent.OSC_DISCONNECTED,
                ),
                on_panic_callback=self._on_osc_panicked,
            ),
            process_protocol=AsyncProcessProtocol(
                name=name,
                on_boot_callback=lambda: self._on_lifecycle_event(
                    ServerLifecycleEvent.PROCESS_BOOTED
                ),
                on_panic_callback=lambda: self._on_lifecycle_event(
                    ServerLifecycleEvent.PROCESS_PANICKED
                ),
                on_quit_callback=lambda: self._on_lifecycle_event(
                    ServerLifecycleEvent.PROCESS_QUIT
                ),
            ),
            **kwargs,
        )

    ### PRIVATE METHODS ###

    async def _connect(self) -> None:
        logger.info(
            f"[{self._options.ip_address}:{self._options.port}/{self.name or hex(id(self))}] "
            "connecting ..."
        )
        self._on_lifecycle_event(ServerLifecycleEvent.CONNECTING)
        await cast(AsyncOscProtocol, self._osc_protocol).connect(
            ip_address=self._options.ip_address,
            port=self._options.port,
            healthcheck=DEFAULT_HEALTHCHECK,
        )
        await self._setup_notifications()
        self._contexts.add(self)
        self._osc_protocol.activate_healthcheck()
        self._setup_allocators()
        if self._client_id == 0:
            self._setup_system()
            await self.sync()
        await cast(asyncio.Future, self._osc_protocol.boot_future)
        logger.info(
            f"[{self._options.ip_address}:{self._options.port}/{self.name or hex(id(self))}] "
            "... connected!"
        )
        self._boot_status = BootStatus.ONLINE
        if not self.is_owner:
            self._boot_future.set_result(True)
        self._on_lifecycle_event(ServerLifecycleEvent.CONNECTED)

    async def _disconnect(self) -> None:
        logger.info(
            f"[{self._options.ip_address}:{self._options.port}/{self.name or hex(id(self))}] "
            "disconnecting ..."
        )
        self._on_lifecycle_event(ServerLifecycleEvent.DISCONNECTING)
        await cast(AsyncOscProtocol, self._osc_protocol).disconnect()
        self._teardown_shm()
        self._teardown_state()
        if self in self._contexts:
            self._contexts.remove(self)
        was_owner = self._is_owner = True
        self._is_owner = False
        logger.info(
            f"[{self._options.ip_address}:{self._options.port}/{self.name or hex(id(self))}] "
            "... disconnected!"
        )
        self._boot_status = BootStatus.OFFLINE
        self._on_lifecycle_event(ServerLifecycleEvent.DISCONNECTED)
        if not was_owner:
            if not self._boot_future.done():
                self._boot_future.set_result(True)
            if not self._exit_future.done():
                self._exit_future.set_result(True)

    async def _handle_done_quit(self, message: OscMessage) -> None:
        logger.info(
            f"[{self._options.ip_address}:{self._options.port}/{self.name or hex(id(self))}] "
            f"handling {message.to_list()} ..."
        )
        if self._boot_status == BootStatus.ONLINE:
            await self._shutdown()
        else:
            logger.info(
                f"[{self._options.ip_address}:{self._options.port}/{self.name or hex(id(self))}] "
                f"... already quitting!"
            )

    async def _on_osc_panicked(self) -> None:
        self._on_lifecycle_event(ServerLifecycleEvent.OSC_PANICKED)
        await self._shutdown()
        if not self._exit_future.done():
            self._exit_future.set_result(False)

    async def _setup_notifications(self) -> None:
        logger.info(
            f"[{self._options.ip_address}:{self._options.port}/{self.name or hex(id(self))}] "
            "setting up notifications ..."
        )
        response = await ToggleNotifications(True).communicate_async(server=self)
        if response is None or not isinstance(response, (DoneInfo, FailInfo)):
            raise RuntimeError
        if isinstance(response, FailInfo):
            await self._shutdown()
            raise TooManyClients
        if len(response.other) == 1:  # supernova doesn't provide a max logins value
            self._client_id = int(response.other[0])
            self._maximum_logins = self._options.maximum_logins
        else:
            self._client_id = int(response.other[0])
            self._maximum_logins = int(response.other[1])

    async def _shutdown(self):
        if self.is_owner:
            await self.quit()
        else:
            await self.disconnect()

    ### PUBLIC METHODS ###

    async def boot(
        self, *, options: Optional[Options] = None, **kwargs
    ) -> "AsyncServer":
        """
        Boot the server.

        :param options: The context's options.
        :param kwargs: Keyword arguments for options.
        """
        if self._boot_status != BootStatus.OFFLINE:
            raise ServerOnline
        logger.info(
            f"[{self._options.ip_address}:{self._options.port}/{self.name or hex(id(self))}] "
            "booting ..."
        )
        loop = asyncio.get_running_loop()
        self._boot_future = loop.create_future()
        self._exit_future = loop.create_future()
        self._boot_status = BootStatus.BOOTING
        self._on_lifecycle_event(ServerLifecycleEvent.BOOTING)
        self._options = new(options or self._options, **kwargs)
        logger.debug(
            f"[{self._options.ip_address}:{self._options.port}/{self.name or hex(id(self))}] "
            f"options: {self._options}"
        )
        try:
            await cast(AsyncProcessProtocol, self._process_protocol).boot(self._options)
        except ServerCannotBoot:
            if not self._boot_future.done():
                self._boot_future.set_result(False)
                self._exit_future.set_result(False)
            self._boot_status = BootStatus.OFFLINE
            raise
        self._is_owner = True
        self._setup_shm()
        await self._connect()
        logger.info(
            f"[{self._options.ip_address}:{self._options.port}/{self.name or hex(id(self))}] "
            "... booted!"
        )
        self._on_lifecycle_event(ServerLifecycleEvent.BOOTED)
        if self.is_owner:
            self._boot_future.set_result(True)
        return self

    async def connect(
        self, *, options: Optional[Options] = None, **kwargs
    ) -> "AsyncServer":
        """
        Connect to a running server.

        :param options: The context's options.
        :param kwargs: Keyword arguments for options.
        """
        if self._boot_status != BootStatus.OFFLINE:
            raise ServerOnline
        loop = asyncio.get_running_loop()
        self._boot_future = loop.create_future()
        self._exit_future = loop.create_future()
        self._boot_status = BootStatus.BOOTING
        self._options = new(options or self._options, **kwargs)
        self._is_owner = False
        await self._connect()
        return self

    async def disconnect(self) -> "AsyncServer":
        """
        Disconnect from a running server.
        """
        if self._boot_status == BootStatus.OFFLINE:
            raise ServerOffline
        if self._is_owner:
            raise OwnedServerShutdown("Cannot disconnect from owned server.")
        self._boot_status = BootStatus.QUITTING
        await self._disconnect()
        return self

    async def dump_tree(
        self,
        group: Optional[Group] = None,
        include_controls: bool = True,
        sync: bool = True,
    ) -> Optional[QueryTreeGroup]:
        """
        Dump the server's node tree.

        Emit ``/g_dumpTree`` requests.

        :param group: The group whose tree to query. Defaults to the root node.
        :param include_controls: Flag for including synth control values.
        :param sync: If true, communicate the request immediately. Otherwise bundle it
            with the current request context.
        """
        self._validate_can_request()
        request = DumpTree(items=[(group or self.root_node, bool(include_controls))])
        if sync:
            with self.process_protocol.capture() as transcript:
                await request.communicate_async(server=self)
                await self.sync(timeout=10.0)
                return QueryTreeGroup.from_string("\n".join(transcript.lines))
        self._add_requests(request)
        return None

    async def get_buffer(
        self, buffer: Buffer, *indices: int, sync: bool = True
    ) -> Optional[Dict[int, float]]:
        """
        Get a buffer sample.

        Emit ``/b_get`` requests.

        :param buffer: The buffer whose sample to get.
        :param indices: The sample indices to read.
        :param sync: If true, communicate the request immediately. Otherwise bundle it
            with the current request context.
        """
        request = GetBuffer(buffer_id=buffer, indices=indices)
        if sync:
            return dict(
                cast(GetBufferInfo, await request.communicate_async(server=self)).items
            )
        self._add_requests(request)
        return None

    async def get_buffer_range(
        self, buffer: Buffer, index: int, count: int, sync: bool = True
    ) -> Optional[Sequence[float]]:
        """
        Get a buffer sample range.

        Emit ``/b_getn`` requests.

        :param buffer: The buffer whose samples to get.
        :param index: The sample index to start reading at.
        :param count: The number of samples to read.
        :param sync: If true, communicate the request immediately. Otherwise bundle it
            with the current request context.
        """
        request = GetBufferRange(buffer_id=buffer, items=[(index, count)])
        if sync:
            return cast(
                GetBufferRangeInfo, await request.communicate_async(server=self)
            ).items[0][-1]
        self._add_requests(request)
        return None

    async def get_bus(self, bus: Bus, sync: bool = True) -> Optional[float]:
        """
        Get a control bus value.

        Emit ``/c_get`` requests.

        :param bus: The control bus whose value to get.
        :param sync: If true, communicate the request immediately. Otherwise bundle it
            with the current request context.
        """
        if bus.calculation_rate != CalculationRate.CONTROL:
            raise InvalidCalculationRate
        request = GetControlBus(bus_ids=[bus.id_])
        if sync:
            return cast(
                GetControlBusInfo, await request.communicate_async(server=self)
            ).items[0][-1]
        self._add_requests(request)
        return None

    async def get_bus_range(
        self, bus: Bus, count: int, sync: bool = True
    ) -> Optional[Sequence[float]]:
        """
        Get a range of control bus values.

        Emit ``/c_getn`` requests.

        :param bus: The control bus to start reading at.
        :param count: The number of contiguous buses whose values to get.
        :param sync: If true, communicate the request immediately. Otherwise bundle it
            with the current request context.
        """
        if bus.calculation_rate != CalculationRate.CONTROL:
            raise InvalidCalculationRate
        request = GetControlBusRange(items=[(bus.id_, count)])
        if sync:
            return cast(
                GetControlBusRangeInfo, await request.communicate_async(server=self)
            ).items[0][-1]
        self._add_requests(request)
        return None

    async def get_synth_controls(
        self, synth: Synth, *controls: Union[int, str], sync: bool = True
    ) -> Optional[Dict[Union[int, str], float]]:
        """
        Get a synth control.

        Emit ``/s_get`` requests.

        :param synth: The synth whose control to get.
        :param controls: The controls to get.
        :param sync: If true, communicate the request immediately. Otherwise bundle it
            with the current request context.
        """
        request = GetSynthControl(synth_id=synth, controls=controls)
        if sync:
            return dict(
                cast(
                    GetNodeControlInfo, await request.communicate_async(server=self)
                ).items
            )
        self._add_requests(request)
        return None

    async def get_synth_control_range(
        self, synth: Synth, control: Union[int, str], count: int, sync: bool = True
    ) -> Optional[Sequence[Union[float, str]]]:
        """
        Get a range of synth controls.

        Emit ``/s_getn`` requests.

        :param synth: The synth whose control to get.
        :param control: The control to start reading at.
        :param count: The number of contiguous controls to get.
        :param sync: If true, communicate the request immediately. Otherwise bundle it
            with the current request context.
        """
        request = GetSynthControlRange(synth_id=synth, items=[(control, count)])
        if sync:
            return cast(
                GetNodeControlRangeInfo, await request.communicate_async(server=self)
            ).items[0][-1]
        self._add_requests(request)
        return None

    async def query_buffer(
        self, buffer: Buffer, sync: bool = True
    ) -> Optional[BufferInfo]:
        """
        Query a buffer.

        Emit ``/b_query`` requests.

        :param buffer: The buffer to query.
        :param sync: If true, communicate the request immediately. Otherwise bundle it
            with the current request context.
        """
        request = QueryBuffer(buffer_ids=[buffer.id_])
        if sync:
            return cast(BufferInfo, await request.communicate_async(server=self))
        self._add_requests(request)
        return None

    async def query_node(self, node: Node, sync: bool = True) -> Optional[NodeInfo]:
        """
        Query a node.

        Emit ``/n_query`` requests.

        :param node: The node to query.
        :param sync: If true, communicate the request immediately. Otherwise bundle it
            with the current request context.
        """
        request = QueryNode(node_ids=[node.id_])
        if sync:
            return cast(NodeInfo, await request.communicate_async(server=self))
        self._add_requests(request)
        return None

    async def query_status(self, sync: bool = True) -> Optional[StatusInfo]:
        """
        Query the server's status.

        Emit ``/status`` requests.

        :param sync: If true, communicate the request immediately. Otherwise bundle it
            with the current request context.
        """
        request = QueryStatus()
        if sync:
            return cast(StatusInfo, await request.communicate_async(server=self))
        self._add_requests(request)
        return None

    async def query_tree(
        self,
        group: Optional[Group] = None,
        include_controls: bool = True,
        sync: bool = True,
    ) -> Optional[Union[QueryTreeGroup, QueryTreeSynth]]:
        """
        Query the server's node tree.

        Emit ``/g_queryTree`` requests.

        :param group: The group whose tree to query. Defaults to the root node.
        :param include_controls: Flag for including synth control values.
        :param sync: If true, communicate the request immediately. Otherwise bundle it
            with the current request context.
        """
        request = QueryTree(items=[(group or 0, include_controls)])
        if sync:
            return QueryTreeGroup.from_query_tree_info(
                cast(QueryTreeInfo, await request.communicate_async(server=self))
            )
        self._add_requests(request)
        return None

    async def query_version(self, sync: bool = True) -> Optional[VersionInfo]:
        """
        Query the server's version.

        Emit ``/version`` requests.

        :param sync: If true, communicate the request immediately. Otherwise bundle it
            with the current request context.
        """
        request = QueryVersion()
        if sync:
            return cast(VersionInfo, await request.communicate_async(server=self))
        self._add_requests(request)
        return None

    async def quit(self, force: bool = False) -> "AsyncServer":
        """
        Quit the server.

        Emit ``/quit`` requests.

        :param force: Force the server to quit, even if this client doesn't own the
            process.
        """
        if self._boot_status != BootStatus.ONLINE:
            return self
        if not self._is_owner and not force:
            raise UnownedServerShutdown(
                "Cannot quit unowned server without force flag."
            )
        logger.info(
            f"[{self._options.ip_address}:{self._options.port}/{self.name or hex(id(self))}] "
            "quitting ..."
        )
        self._boot_status = BootStatus.QUITTING
        self._on_lifecycle_event(ServerLifecycleEvent.QUITTING)
        try:
            await Quit().communicate_async(server=self, timeout=1)
        except (OscProtocolOffline, asyncio.TimeoutError):
            pass
        await self._disconnect()
        await cast(AsyncProcessProtocol, self._process_protocol).quit()
        logger.info(
            f"[{self._options.ip_address}:{self._options.port}/{self.name or hex(id(self))}] "
            "... quit!"
        )
        self._on_lifecycle_event(ServerLifecycleEvent.QUIT)
        if not self._boot_future.done():
            self._boot_future.set_result(True)
        if not self._exit_future.done():
            self._exit_future.set_result(True)
        return self

    async def reboot(self) -> "AsyncServer":
        """
        Reboot the server.
        """
        await self.quit()
        await self.boot()
        return self

    async def reset(self) -> "AsyncServer":
        """
        Reset the server's state without quitting.
        """
        with self.at():
            self.clear_schedule()
            self.free_all_synthdefs()
            self.free_group_children(self.root_node)
        await self.sync()
        self._teardown_state()
        self._setup_allocators()
        self._setup_system()
        await self.sync()
        return self

    async def sync(
        self, sync_id: Optional[int] = None, timeout: float = 1.0
    ) -> "AsyncServer":
        """
        Sync the server.

        Emit ``/sync`` requests.

        :param sync_id: The sync ID to wait on.
        """
        if self._boot_status not in (BootStatus.BOOTING, BootStatus.ONLINE):
            raise ServerOffline
        await Sync(
            sync_id=sync_id if sync_id is not None else self._get_next_sync_id()
        ).communicate_async(server=self, timeout=timeout)
        return self
