"""
Tools for interacting with realtime execution contexts.
"""

import asyncio
import concurrent.futures
import logging
import os
import platform
import shlex
import threading
import time
import warnings
from collections.abc import Sequence as SequenceABC
from typing import (
    Awaitable,
    Callable,
    Iterable,
    Literal,
    NamedTuple,
    Sequence,
    SupportsInt,
    Type,
    cast,
)

from ..enums import (
    AddAction,
    BootStatus,
    CalculationRate,
    ServerLifecycleEvent,
    ServerShutdownEvent,
)
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
    OscCallback,
    OscMessage,
    OscProtocol,
    OscProtocolOffline,
    ThreadedOscProtocol,
)
from ..scsynth import AsyncProcessProtocol, Options, ThreadedProcessProtocol
from ..typing import AddActionLike, ServerLifecycleEventLike, SupportsOsc
from ..ugens import SYSTEM_SYNTHDEFS
from .core import Context
from .entities import (
    Buffer,
    Bus,
    BusGroup,
    ContextObject,
    Group,
    Node,
    Synth,
)
from .errors import InvalidCalculationRate
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
    StatusInfo,
    VersionInfo,
)
from .scopes import AmplitudeScope, FrequencyScope
from .shm import ServerSHM

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


class ServerLifecycleCallback(NamedTuple):
    context: "BaseServer"
    events: tuple[ServerLifecycleEvent, ...]
    procedure: Callable[[ServerLifecycleEvent], Awaitable[None] | None]
    once: bool = False
    args: tuple | None = None
    kwargs: dict | None = None

    def unregister(self) -> None:
        self.context.unregister_lifecycle_callback(self)


class BaseServer(Context):
    """
    Base class for realtime execution contexts.

    :param options: The context's options.
    :param kwargs: Keyword arguments for options.
    """

    ### CLASS VARIABLES ###

    _contexts: set["BaseServer"] = set()

    ### INITIALIZER ###

    def __init__(
        self,
        options: Options | None,
        name: str | None = None,
        **kwargs,
    ) -> None:
        Context.__init__(self, options, name=name, **kwargs)
        self._buffers: set[int] = set()
        self._is_owner: bool = False
        self._latency: float = 0.1
        self._lifecycle_event_callbacks: dict[
            ServerLifecycleEvent, list[ServerLifecycleCallback]
        ] = {}
        self._maximum_logins: int = 1
        self._node_active: dict[int, bool] = {}
        self._node_children: dict[int, list[int]] = {}
        self._node_parents: dict[int, int] = {}
        self._shared_memory: ServerSHM | None = None
        self._status: StatusInfo | None = None

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

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.boot_status.name} [{shlex.join(self.options)}]>"

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
        calculation_rate: CalculationRate | None = None,
    ) -> None:
        self._get_allocator(type_, calculation_rate).free(id_)

    def _handle_done_b_alloc(self, message: OscMessage) -> None:
        with self._lock:
            self._buffers.add(cast(int, message.contents[1]))

    def _handle_done_b_alloc_read(self, message: OscMessage) -> None:
        with self._lock:
            self._buffers.add(cast(int, message.contents[1]))

    def _handle_done_b_alloc_read_channel(self, message: OscMessage) -> None:
        with self._lock:
            self._buffers.add(cast(int, message.contents[1]))

    def _handle_done_b_free(self, message: OscMessage) -> None:
        with self._lock:
            buffer_id = cast(int, message.contents[1])
            if buffer_id in self._buffers:
                self._buffers.remove(buffer_id)
            self._free_id(Buffer, buffer_id)

    def _handle_fail(self, message: OscMessage) -> None:
        warnings.warn(
            " ".join(str(x) for x in message.contents).strip(),
            FailWarning,
        )

    def _handle_n_end(self, message: OscMessage) -> None:
        with self._lock:
            node_id = cast(int, message.contents[0])
            parent_id = cast(int | None, message.contents[1])
            if parent_id == -1:
                parent_id = self._node_parents.get(node_id)
            if parent_id is not None:
                self._remove_node_from_children(node_id, parent_id)
            self._free_id(Node, node_id)
            self._node_active.pop(node_id, None)
            self._node_children.pop(node_id, None)
            self._node_parents.pop(node_id, None)

    def _handle_n_go(self, message: OscMessage) -> None:
        with self._lock:
            node_id = cast(int, message.contents[0])
            parent_id = cast(int, message.contents[1])
            previous_id = cast(int, message.contents[2])
            next_id = cast(int, message.contents[3])
            is_group = bool(message.contents[4])
            self._node_parents[node_id] = parent_id
            self._node_active[node_id] = True
            if is_group:
                self._node_children[node_id] = []
            self._add_node_to_children(node_id, parent_id, previous_id, next_id)

    def _handle_n_move(self, message: OscMessage) -> None:
        with self._lock:
            node_id = cast(int, message.contents[0])
            parent_id = cast(int, message.contents[1])
            previous_id = cast(int, message.contents[2])
            next_id = cast(int, message.contents[3])
            old_parent_id = self._node_parents[node_id]
            self._remove_node_from_children(node_id, old_parent_id)
            self._add_node_to_children(node_id, parent_id, previous_id, next_id)

    def _handle_n_off(self, message: OscMessage) -> None:
        with self._lock:
            node_id = cast(int, message.contents[0])
            self._node_active[node_id] = False

    def _handle_n_on(self, message: OscMessage) -> None:
        with self._lock:
            node_id = cast(int, message.contents[0])
            self._node_active[node_id] = True

    def _handle_status_reply(self, message: OscMessage) -> None:
        with self._lock:
            self._status = cast(StatusInfo, StatusInfo.from_osc(message))

    def _log_prefix(self) -> str:
        return f"[{self._options.ip_address}:{self._options.port}/{self.name or hex(id(self))}] "

    def _register_lifecycle_callback(
        self,
        event: ServerLifecycleEventLike | Iterable[ServerLifecycleEventLike],
        procedure: Callable[[ServerLifecycleEvent], Awaitable[None] | None],
        *,
        once: bool = False,
        args: tuple | None = None,
        kwargs: dict | None = None,
    ) -> ServerLifecycleCallback:
        events: list[ServerLifecycleEvent] = []
        if isinstance(event, Iterable) and not isinstance(event, str):
            for event_ in event:
                events.append(ServerLifecycleEvent.from_expr(event_))
        else:
            events.append(ServerLifecycleEvent.from_expr(event))
        callback = ServerLifecycleCallback(
            context=self,
            events=tuple(sorted(events)),
            procedure=procedure,
            once=once,
            args=args,
            kwargs=kwargs,
        )
        for event_ in events:
            self._lifecycle_event_callbacks.setdefault(event_, []).append(callback)
        return callback

    def _remove_node_from_children(self, id_: int, parent_id: int) -> None:
        if not (children := self._node_children.get(parent_id, [])):
            return
        try:
            children.pop(children.index(id_))
        except ValueError:
            pass

    def _resolve_node(self, node: Node | SupportsInt | None) -> int:
        if node is None:
            return self._client_id + 1
        return int(node)

    def _setup_osc_callbacks(self, osc_protocol: OscProtocol) -> None:
        for pattern, procedure in [
            (["/done", "/b_alloc"], self._handle_done_b_alloc),
            (["/done", "/b_allocRead"], self._handle_done_b_alloc_read),
            (["/done", "/b_allocReadChannel"], self._handle_done_b_alloc_read_channel),
            (["/done", "/b_free"], self._handle_done_b_free),
            (["/fail"], self._handle_fail),
            (["/n_end"], self._handle_n_end),
            (["/n_go"], self._handle_n_go),
            (["/n_move"], self._handle_n_move),
            (["/n_off"], self._handle_n_off),
            (["/n_on"], self._handle_n_on),
            (["/status.reply"], self._handle_status_reply),
        ]:
            osc_protocol.register(pattern=pattern, procedure=procedure)

    def _setup_shared_memory(self) -> None:
        try:
            self._shared_memory = ServerSHM(
                self._options.port, self._options.control_bus_channel_count
            )
        except (ImportError, ModuleNotFoundError):
            pass

    def _setup_system(self) -> None:
        self._node_children[0] = []
        with self.at():
            for i in range(self._maximum_logins):
                self.add_group(permanent=True, add_action="ADD_TO_TAIL", target_node=0)
        for synthdef in SYSTEM_SYNTHDEFS.values():
            with self.at():
                self.add_synthdefs(synthdef)

    def _teardown_shared_memory(self) -> None:
        self._shared_memory = None

    def _teardown_state(self) -> None:
        self._node_active.clear()
        self._node_children.clear()
        self._node_parents.clear()
        self._buffers.clear()

    def _validate_can_request(self) -> None:
        if self._boot_status not in (BootStatus.BOOTING, BootStatus.ONLINE):
            raise ServerOffline("Server already offline!")
        pass  # Otherwise always OK to request in RT

    def _validate_moment_timestamp(self, seconds: float | None) -> None:
        pass  # Floats and None are OK in RT

    ### PUBLIC METHODS ###

    def add_amplitude_scope(
        self,
        bus: Bus | BusGroup,
        add_action: AddActionLike = AddAction.ADD_TO_TAIL,
        target_node: Node | None = None,
    ) -> AmplitudeScope:
        """
        Add an amplitude scope.
        """
        scope = AmplitudeScope(
            add_action=add_action,
            bus=bus,
            context=self,
            target_node=target_node,
        )
        scope.play()
        return scope

    def add_frequency_scope(
        self,
        bus: Bus,
        add_action: AddActionLike = AddAction.ADD_TO_TAIL,
        fft_size: int = 4096,
        frequency_mode: Literal["linear", "logarithmic"] = "linear",
        rate: int = 4,
        target_node: Node | None = None,
    ) -> FrequencyScope:
        """
        Add a frequency scope.
        """
        scope = FrequencyScope(
            add_action=add_action,
            bus=bus,
            context=self,
            fft_size=fft_size,
            frequency_mode=frequency_mode,
            rate=rate,
            target_node=target_node,
        )
        scope.play()
        return scope

    def send(self, message: SequenceABC | SupportsOsc | str) -> None:
        """
        Send a message to the execution context.

        :param message: The message to send.
        """
        if self._boot_status == BootStatus.OFFLINE:
            raise ServerOffline("Server already offline!")
        osc_protocol: OscProtocol = getattr(self, "_osc_protocol")
        osc_protocol.send(message)

    def set_latency(self, latency: float) -> None:
        """
        set the context's latency.

        :param latency: The latency in seconds.
        """
        self._latency = float(latency)

    def unregister_lifecycle_callback(self, callback: ServerLifecycleCallback) -> None:
        """
        Unregister a lifecycle callback.

        :param callback: The callback to unregister.
        """
        for event in callback.events:
            if event not in self._lifecycle_event_callbacks:
                continue
            if callback in (callbacks := self._lifecycle_event_callbacks[event]):
                callbacks.remove(callback)
            if not callbacks:
                self._lifecycle_event_callbacks.pop(event)

    ### PUBLIC PROPERTIES ###

    @property
    def default_group(self) -> Group:
        """
        Get the server's default group.
        """
        return Group(context=self, id_=self._client_id + 1)

    @property
    def is_owner(self) -> bool:
        """
        Get the server's ownership flag.
        """
        return self._is_owner

    @property
    def shared_memory(self) -> ServerSHM | None:
        """
        Get the server's shared memory interface, if available.
        """
        return self._shared_memory

    @property
    def status(self) -> StatusInfo | None:
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
        options: Options | None = None,
        name: str | None = None,
        **kwargs,
    ) -> None:
        def on_panic(event: ServerShutdownEvent) -> None:
            if not self._shutdown_future.done():
                self._shutdown_future.set_result(event)

        BaseServer.__init__(
            self,
            name=name,
            options=options,
            **kwargs,
        )
        self._boot_future: concurrent.futures.Future[bool] = concurrent.futures.Future()
        self._exit_future: concurrent.futures.Future[bool] = concurrent.futures.Future()
        self._shutdown_future: concurrent.futures.Future[ServerShutdownEvent] = (
            concurrent.futures.Future()
        )
        self._osc_protocol: ThreadedOscProtocol = ThreadedOscProtocol(
            name=name, on_panic_callback=lambda: on_panic(ServerShutdownEvent.OSC_PANIC)
        )
        self._process_protocol: ThreadedProcessProtocol = ThreadedProcessProtocol(
            name=name,
            on_panic_callback=lambda: on_panic(ServerShutdownEvent.PROCESS_PANIC),
        )
        self._setup_osc_callbacks(self._osc_protocol)

    ### PRIVATE METHODS ###

    def _lifecycle(self, owned: bool = True) -> None:
        log_prefix = self._log_prefix()
        logger.info(log_prefix + "booting ...")
        if owned:
            self._on_lifecycle_event(ServerLifecycleEvent.BOOTING)
            try:
                self._process_protocol.boot(self._options)
            except ServerCannotBoot:
                self._on_lifecycle_event(ServerLifecycleEvent.PROCESS_PANICKED)
                self._boot_status = BootStatus.OFFLINE
                self._boot_future.set_result(False)
                self._exit_future.set_result(False)
                return
            self._is_owner = True
            self._setup_shared_memory()
            self._on_lifecycle_event(ServerLifecycleEvent.PROCESS_BOOTED)
        logger.info(log_prefix + "connecting ...")
        self._on_lifecycle_event(ServerLifecycleEvent.CONNECTING)
        self._osc_protocol.connect(
            ip_address=self._options.ip_address,
            port=self._options.port,
            healthcheck=DEFAULT_HEALTHCHECK,
        )
        try:
            self._setup_notifications()
            self._contexts.add(self)
            self._osc_protocol.activate_healthcheck()
            self._setup_allocators(owned=self._is_owner)
            if self._client_id == 0:
                self._setup_system()
                self.sync()
            if self._osc_protocol.boot_future.result():
                self._boot_status = BootStatus.ONLINE
                self._on_lifecycle_event(ServerLifecycleEvent.OSC_CONNECTED)
                self._on_lifecycle_event(ServerLifecycleEvent.CONNECTED)
                logger.info(log_prefix + "... connected!")
                if owned:
                    logger.info(log_prefix + "... booted!")
                    self._on_lifecycle_event(ServerLifecycleEvent.BOOTED)
                self._boot_future.set_result(True)
        except TooManyClients:
            self._shutdown_future.set_result(ServerShutdownEvent.TOO_MANY_CLIENTS)
        # await shutdown future, osc panic, process panic
        shutdown = self._shutdown_future.result()
        # fire off quitting?
        if shutdown == ServerShutdownEvent.QUIT:
            logger.info(log_prefix + "quitting ...")
        self._boot_status = BootStatus.QUITTING
        if shutdown == ServerShutdownEvent.QUIT:
            try:
                Quit().communicate(server=self, timeout=1)
            except (OscProtocolOffline, asyncio.TimeoutError):
                pass
        elif shutdown == ServerShutdownEvent.DISCONNECT:
            pass
        elif shutdown == ServerShutdownEvent.OSC_PANIC:
            self._on_lifecycle_event(ServerLifecycleEvent.OSC_PANICKED)
        elif shutdown == ServerShutdownEvent.PROCESS_PANIC:
            self._on_lifecycle_event(ServerLifecycleEvent.PROCESS_PANICKED)
            self._on_lifecycle_event(ServerLifecycleEvent.OSC_PANICKED)
        if owned or shutdown == ServerShutdownEvent.QUIT:
            self._on_lifecycle_event(ServerLifecycleEvent.QUITTING)
        # handle shutdown future specifically with Quit request
        logger.info(log_prefix + "disconnecting ...")
        self._on_lifecycle_event(ServerLifecycleEvent.DISCONNECTING)
        self._osc_protocol.disconnect()
        if shutdown in (ServerShutdownEvent.QUIT, ServerShutdownEvent.DISCONNECT):
            self._on_lifecycle_event(ServerLifecycleEvent.OSC_DISCONNECTED)
        if owned:
            self._teardown_shared_memory()
        self._teardown_state()
        self._is_owner = False
        if self in self._contexts:
            self._contexts.remove(self)
        logger.info(log_prefix + "disconnected!")
        self._on_lifecycle_event(ServerLifecycleEvent.DISCONNECTED)
        if owned:
            self._process_protocol.quit()
            if shutdown == ServerShutdownEvent.QUIT:
                self._on_lifecycle_event(ServerLifecycleEvent.PROCESS_QUIT)
        self._boot_status = BootStatus.OFFLINE
        if not self._boot_future.done():
            self._boot_future.set_result(
                shutdown in (ServerShutdownEvent.QUIT, ServerShutdownEvent.DISCONNECT)
            )
        if owned or shutdown == ServerShutdownEvent.QUIT:
            logger.info(log_prefix + "quit!")
            self._on_lifecycle_event(ServerLifecycleEvent.QUIT)
        self._exit_future.set_result(
            shutdown in (ServerShutdownEvent.QUIT, ServerShutdownEvent.DISCONNECT)
        )
        return

    def _on_lifecycle_event(self, event: ServerLifecycleEvent) -> None:
        for callback in self._lifecycle_event_callbacks.get(event, []):
            logger.info(
                self._log_prefix() + f"lifecycle event: {event.name} {callback}"
            )
            callback.procedure(event, *(callback.args or ()), **(callback.kwargs or {}))
            if callback.once:
                self.unregister_lifecycle_callback(callback)

    def _setup_notifications(self) -> None:
        logger.info(self._log_prefix() + "setting up notifications ...")
        response = ToggleNotifications(True).communicate(server=self)
        if response is None or not isinstance(response, (DoneInfo, FailInfo)):
            raise RuntimeError
        if isinstance(response, FailInfo):
            raise TooManyClients("Too many clients connected already")
        if len(response.other) == 1:  # supernova doesn't provide a max logins value
            self._client_id = int(response.other[0])
            self._maximum_logins = self._options.maximum_logins
        else:
            self._client_id = int(response.other[0])
            self._maximum_logins = int(response.other[1])

    def _shutdown(self) -> None:
        if self.is_owner:
            self.quit()
        else:
            self.disconnect()

    ### PUBLIC METHODS ###

    def boot(self, *, options: Options | None = None, **kwargs) -> "Server":
        """
        Boot the server.

        :param options: The context's options.
        :param kwargs: Keyword arguments for options.
        """
        if self._boot_status != BootStatus.OFFLINE:
            raise ServerOnline("Server already online!")
        self._boot_status = BootStatus.BOOTING
        self._options = self._get_options(options or self._options, **kwargs)
        self._boot_future = concurrent.futures.Future()
        self._exit_future = concurrent.futures.Future()
        self._shutdown_future = concurrent.futures.Future()
        self._lifecycle_thread = threading.Thread(
            daemon=True,
            kwargs=dict(owned=True),
            target=self._lifecycle,
        )
        self._lifecycle_thread.start()
        if not (self._boot_future.result()):
            if (self._shutdown_future.result()) == ServerShutdownEvent.PROCESS_PANIC:
                raise ServerCannotBoot(self.process_protocol.error_text)
        return self

    def connect(self, *, options: Options | None = None, **kwargs) -> "Server":
        """
        Connect to a running server.

        :param options: The context's options.
        :param kwargs: Keyword arguments for options.
        """
        if self._boot_status != BootStatus.OFFLINE:
            raise ServerOnline("Server already online!")
        self._boot_status = BootStatus.BOOTING
        self._options = self._get_options(options or self._options, **kwargs)
        self._boot_future = concurrent.futures.Future()
        self._exit_future = concurrent.futures.Future()
        self._shutdown_future = concurrent.futures.Future()
        self._lifecycle_thread = threading.Thread(
            daemon=True,
            kwargs=dict(owned=False),
            target=self._lifecycle,
        )
        self._lifecycle_thread.start()
        if not (self._boot_future.result()):
            if self._shutdown_future.result() == ServerShutdownEvent.TOO_MANY_CLIENTS:
                raise TooManyClients("Too many clients connected already")
        return self

    def disconnect(self) -> "Server":
        """
        Disconnect from a running server.
        """
        if self._boot_status == BootStatus.OFFLINE:
            raise ServerOffline("Server already offline!")
        if self._is_owner:
            raise OwnedServerShutdown("Cannot disconnect from owned server.")
        self._shutdown_future.set_result(ServerShutdownEvent.DISCONNECT)
        self._exit_future.result()
        return self

    def dump_tree(
        self,
        group: Group | None = None,
        include_controls: bool = True,
        sync: bool = True,
    ) -> QueryTreeGroup | None:
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
                # TODO: We need an end-delimiter for /g_dumpTree
                if platform.system() == "Windows" and os.environ.get("CI"):
                    time.sleep(0.05)
                self.sync(timeout=10.0)
                return QueryTreeGroup.from_string("\n".join(transcript.lines))
        self._add_requests(request)
        return None

    def get_buffer(
        self, buffer: Buffer, *indices: int, sync: bool = True
    ) -> dict[int, float] | None:
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
    ) -> Sequence[float] | None:
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

    def get_bus(self, bus: Bus, sync: bool = True) -> float | None:
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
    ) -> Sequence[float] | None:
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
        self, synth: Synth, *controls: int | str, sync: bool = True
    ) -> dict[int | str, float] | None:
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
        self, synth: Synth, control: int | str, count: int, sync: bool = True
    ) -> Sequence[float | str] | None:
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

    def query_buffer(self, buffer: Buffer, sync: bool = True) -> BufferInfo | None:
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

    def query_node(self, node: Node, sync: bool = True) -> NodeInfo | None:
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

    def query_status(self, sync: bool = True) -> StatusInfo | None:
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
        group: Group | None = None,
        include_controls: bool = True,
        sync: bool = True,
    ) -> QueryTreeGroup | None:
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

    def query_version(self, sync: bool = True) -> VersionInfo | None:
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
        self._shutdown_future.set_result(ServerShutdownEvent.QUIT)
        self._exit_future.result()
        return self

    def reboot(self) -> "Server":
        """
        Reboot the server.
        """
        self.quit()
        self.boot()
        return self

    def register_lifecycle_callback(
        self,
        event: ServerLifecycleEventLike | Iterable[ServerLifecycleEventLike],
        procedure: Callable[[ServerLifecycleEvent], None],
        *,
        once: bool = False,
        args: tuple | None = None,
        kwargs: dict | None = None,
    ) -> ServerLifecycleCallback:
        """
        Register a server lifecycle callback.
        """
        return self._register_lifecycle_callback(
            event=event,
            procedure=procedure,
            once=once,
            args=args,
            kwargs=kwargs,
        )

    def register_osc_callback(
        self,
        pattern: Sequence[float | str],
        procedure: Callable[[OscMessage], None],
        *,
        failure_pattern: Sequence[float | str] | None = None,
        once: bool = False,
        args: tuple | None = None,
        kwargs: dict | None = None,
    ) -> OscCallback:
        """
        Register an OSC callback.
        """
        return self.osc_protocol.register(
            args=args,
            failure_pattern=failure_pattern,
            kwargs=kwargs,
            once=once,
            pattern=pattern,
            procedure=procedure,
        )

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
        self._setup_allocators(owned=self._is_owner)
        self._setup_system()
        self.sync()
        return self

    def sync(self, sync_id: int | None = None, timeout: float = 1.0) -> "Server":
        """
        Sync the server.

        Emit ``/sync`` requests.

        :param sync_id: The sync ID to wait on.
        """
        if self._boot_status not in (BootStatus.BOOTING, BootStatus.ONLINE):
            raise ServerOffline("Server already offline!")
        Sync(
            sync_id=sync_id if sync_id is not None else self._get_next_sync_id()
        ).communicate(server=self, timeout=timeout)
        return self

    def unregister_osc_callback(self, callback: OscCallback) -> None:
        """
        Unregister an OSC callback.

        :param callback: The callback to unregister.
        """
        # TODO: Implemented here because BaseServer does not define _osc_protocol
        self._osc_protocol.unregister(callback)

    ### PUBLIC PROPERTIES ###

    @property
    def boot_future(self) -> concurrent.futures.Future[bool]:
        """
        Get the server's boot future.

        Only reference this _after_ booting or connecting, as the future is
        created when booting or connecting.
        """
        return self._boot_future

    @property
    def exit_future(self) -> concurrent.futures.Future[bool]:
        """
        Get the server's exit future.

        Only reference this _after_ booting or connecting, as the future is
        created when booting or connecting.
        """
        return self._exit_future

    @property
    def osc_protocol(self) -> ThreadedOscProtocol:
        """
        Get the server's OSC protocol.
        """
        return self._osc_protocol

    @property
    def process_protocol(self) -> ThreadedProcessProtocol:
        """
        Get the server's process protocol.
        """
        return self._process_protocol


class AsyncServer(BaseServer):
    """
    A realtime execution context with :py:mod:`asyncio`-based OSC and process protocols.

    :param options: The context's options.
    :param kwargs: Keyword arguments for options.
    """

    ### INITIALIZER ###

    def __init__(
        self, options: Options | None = None, name: str | None = None, **kwargs
    ) -> None:
        BaseServer.__init__(
            self,
            name=name,
            options=options,
            **kwargs,
        )
        self._boot_future: asyncio.Future[bool] = asyncio.Future()
        self._exit_future: asyncio.Future[bool] = asyncio.Future()
        self._shutdown_future: asyncio.Future[ServerShutdownEvent] = asyncio.Future()
        self._osc_protocol: AsyncOscProtocol = AsyncOscProtocol(
            name=name,
            on_panic_callback=lambda: self._shutdown_future.set_result(
                ServerShutdownEvent.OSC_PANIC
            ),
        )
        self._process_protocol: AsyncProcessProtocol = AsyncProcessProtocol(
            name=name,
            on_panic_callback=lambda: self._shutdown_future.set_result(
                ServerShutdownEvent.PROCESS_PANIC
            ),
        )
        self._setup_osc_callbacks(self._osc_protocol)

    ### PRIVATE METHODS ###

    async def _lifecycle(self, owned: bool = True) -> None:
        log_prefix = self._log_prefix()
        logger.info(log_prefix + "booting ...")
        if owned:
            await self._on_lifecycle_event(ServerLifecycleEvent.BOOTING)
            try:
                await self._process_protocol.boot(self._options)
            except ServerCannotBoot:
                await self._on_lifecycle_event(ServerLifecycleEvent.PROCESS_PANICKED)
                self._boot_status = BootStatus.OFFLINE
                self._boot_future.set_result(False)
                self._exit_future.set_result(False)
                return
            self._is_owner = True
            self._setup_shared_memory()
            await self._on_lifecycle_event(ServerLifecycleEvent.PROCESS_BOOTED)
        logger.info(log_prefix + "connecting ...")
        await self._on_lifecycle_event(ServerLifecycleEvent.CONNECTING)
        await self._osc_protocol.connect(
            ip_address=self._options.ip_address,
            port=self._options.port,
            healthcheck=DEFAULT_HEALTHCHECK,
        )
        try:
            await self._setup_notifications()
            self._contexts.add(self)
            self._osc_protocol.activate_healthcheck()
            self._setup_allocators(owned=self._is_owner)
            if self._client_id == 0:
                self._setup_system()
                await self.sync()
            if await self._osc_protocol.boot_future:
                self._boot_status = BootStatus.ONLINE
                await self._on_lifecycle_event(ServerLifecycleEvent.OSC_CONNECTED)
                await self._on_lifecycle_event(ServerLifecycleEvent.CONNECTED)
                logger.info(log_prefix + "... connected!")
                if owned:
                    logger.info(log_prefix + "... booted!")
                    await self._on_lifecycle_event(ServerLifecycleEvent.BOOTED)
                self._boot_future.set_result(True)
        except TooManyClients:
            self._shutdown_future.set_result(ServerShutdownEvent.TOO_MANY_CLIENTS)
        # await shutdown future, osc panic, process panic
        shutdown = await self._shutdown_future
        # fire off quitting?
        if shutdown == ServerShutdownEvent.QUIT:
            logger.info(log_prefix + "quitting ...")
        self._boot_status = BootStatus.QUITTING
        if shutdown == ServerShutdownEvent.QUIT:
            try:
                await Quit().communicate_async(server=self, timeout=1)
            except (OscProtocolOffline, asyncio.TimeoutError):
                pass
        elif shutdown == ServerShutdownEvent.DISCONNECT:
            pass
        elif shutdown == ServerShutdownEvent.OSC_PANIC:
            await self._on_lifecycle_event(ServerLifecycleEvent.OSC_PANICKED)
        elif shutdown == ServerShutdownEvent.PROCESS_PANIC:
            await self._on_lifecycle_event(ServerLifecycleEvent.PROCESS_PANICKED)
            await self._on_lifecycle_event(ServerLifecycleEvent.OSC_PANICKED)
        if owned or shutdown == ServerShutdownEvent.QUIT:
            await self._on_lifecycle_event(ServerLifecycleEvent.QUITTING)
        # handle shutdown future specifically with Quit request
        logger.info(log_prefix + "disconnecting ...")
        await self._on_lifecycle_event(ServerLifecycleEvent.DISCONNECTING)
        await self._osc_protocol.disconnect()
        if shutdown in (ServerShutdownEvent.QUIT, ServerShutdownEvent.DISCONNECT):
            await self._on_lifecycle_event(ServerLifecycleEvent.OSC_DISCONNECTED)
        if owned:
            self._teardown_shared_memory()
        self._teardown_state()
        self._is_owner = False
        if self in self._contexts:
            self._contexts.remove(self)
        logger.info(log_prefix + "disconnected!")
        await self._on_lifecycle_event(ServerLifecycleEvent.DISCONNECTED)
        if owned:
            await self._process_protocol.quit()
            if shutdown == ServerShutdownEvent.QUIT:
                await self._on_lifecycle_event(ServerLifecycleEvent.PROCESS_QUIT)
        self._boot_status = BootStatus.OFFLINE
        if not self._boot_future.done():
            self._boot_future.set_result(
                shutdown in (ServerShutdownEvent.QUIT, ServerShutdownEvent.DISCONNECT)
            )
        if owned or shutdown == ServerShutdownEvent.QUIT:
            logger.info(log_prefix + "quit!")
            await self._on_lifecycle_event(ServerLifecycleEvent.QUIT)
        self._exit_future.set_result(
            shutdown in (ServerShutdownEvent.QUIT, ServerShutdownEvent.DISCONNECT)
        )
        return

    async def _on_lifecycle_event(self, event: ServerLifecycleEvent) -> None:
        for callback in self._lifecycle_event_callbacks.get(event, []):
            logger.info(
                self._log_prefix() + f"lifecycle event: {event.name} {callback}"
            )
            if asyncio.iscoroutine(
                result := callback.procedure(
                    event, *(callback.args or ()), **(callback.kwargs or {})
                )
            ):
                await result
            if callback.once:
                self.unregister_lifecycle_callback(callback)

    async def _setup_notifications(self) -> None:
        logger.info(self._log_prefix() + "setting up notifications ...")
        response = await ToggleNotifications(True).communicate_async(server=self)
        if response is None or not isinstance(response, (DoneInfo, FailInfo)):
            raise RuntimeError
        if isinstance(response, FailInfo):
            raise TooManyClients("Too many clients connected already")
        if len(response.other) == 1:  # supernova doesn't provide a max logins value
            self._client_id = int(response.other[0])
            self._maximum_logins = self._options.maximum_logins
        else:
            self._client_id = int(response.other[0])
            self._maximum_logins = int(response.other[1])

    async def _shutdown(self) -> None:
        if self.is_owner:
            await self.quit()
        else:
            await self.disconnect()

    ### PUBLIC METHODS ###

    async def boot(self, *, options: Options | None = None, **kwargs) -> "AsyncServer":
        """
        Boot the server.

        :param options: The context's options.
        :param kwargs: Keyword arguments for options.
        """
        if self._boot_status != BootStatus.OFFLINE:
            raise ServerOnline("Server already online!")
        self._boot_status = BootStatus.BOOTING
        self._options = self._get_options(options or self._options, **kwargs)
        loop = asyncio.get_running_loop()
        self._boot_future = loop.create_future()
        self._exit_future = loop.create_future()
        self._shutdown_future = loop.create_future()
        self._lifecycle_task = loop.create_task(self._lifecycle(owned=True))
        if not (await self._boot_future):
            if (await self._shutdown_future) == ServerShutdownEvent.PROCESS_PANIC:
                raise ServerCannotBoot(self.process_protocol.error_text)
        return self

    async def connect(
        self, *, options: Options | None = None, **kwargs
    ) -> "AsyncServer":
        """
        Connect to a running server.

        :param options: The context's options.
        :param kwargs: Keyword arguments for options.
        """
        if self._boot_status != BootStatus.OFFLINE:
            raise ServerOnline("Server already online!")
        self._boot_status = BootStatus.BOOTING
        self._options = self._get_options(options or self._options, **kwargs)
        loop = asyncio.get_running_loop()
        self._boot_future = loop.create_future()
        self._exit_future = loop.create_future()
        self._shutdown_future = loop.create_future()
        self._lifecycle_task = loop.create_task(self._lifecycle(owned=False))
        if not (await self._boot_future):
            if await self._shutdown_future == ServerShutdownEvent.TOO_MANY_CLIENTS:
                raise TooManyClients("Too many clients connected already")
        return self

    async def disconnect(self) -> "AsyncServer":
        """
        Disconnect from a running server.
        """
        if self._boot_status == BootStatus.OFFLINE:
            raise ServerOffline("Server already offline!")
        if self._is_owner:
            raise OwnedServerShutdown("Cannot disconnect from owned server.")
        self._shutdown_future.set_result(ServerShutdownEvent.DISCONNECT)
        await self._exit_future
        return self

    async def dump_tree(
        self,
        group: Group | None = None,
        include_controls: bool = True,
        sync: bool = True,
    ) -> QueryTreeGroup | None:
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
                # TODO: We need an end-delimiter for /g_dumpTree
                if platform.system() == "Windows" and os.environ.get("CI"):
                    await asyncio.sleep(0.05)
                await self.sync(timeout=10.0)
                return QueryTreeGroup.from_string("\n".join(transcript.lines))
        self._add_requests(request)
        return None

    async def get_buffer(
        self, buffer: Buffer, *indices: int, sync: bool = True
    ) -> dict[int, float] | None:
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
    ) -> Sequence[float] | None:
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

    async def get_bus(self, bus: Bus, sync: bool = True) -> float | None:
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
    ) -> Sequence[float] | None:
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
        self, synth: Synth, *controls: int | str, sync: bool = True
    ) -> dict[int | str, float] | None:
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
        self, synth: Synth, control: int | str, count: int, sync: bool = True
    ) -> Sequence[float | str] | None:
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
    ) -> BufferInfo | None:
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

    async def query_node(self, node: Node, sync: bool = True) -> NodeInfo | None:
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

    async def query_status(self, sync: bool = True) -> StatusInfo | None:
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
        group: Group | None = None,
        include_controls: bool = True,
        sync: bool = True,
    ) -> QueryTreeGroup | None:
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

    async def query_version(self, sync: bool = True) -> VersionInfo | None:
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
        self._shutdown_future.set_result(ServerShutdownEvent.QUIT)
        await self._exit_future
        return self

    async def reboot(self) -> "AsyncServer":
        """
        Reboot the server.
        """
        await self.quit()
        await self.boot()
        return self

    def register_lifecycle_callback(
        self,
        event: ServerLifecycleEventLike | Iterable[ServerLifecycleEventLike],
        procedure: Callable[[ServerLifecycleEvent], Awaitable[None] | None],
        *,
        once: bool = False,
        args: tuple | None = None,
        kwargs: dict | None = None,
    ) -> ServerLifecycleCallback:
        """
        Register a server lifecycle callback.
        """
        return self._register_lifecycle_callback(
            event=event,
            procedure=procedure,
            once=once,
            args=args,
            kwargs=kwargs,
        )

    def register_osc_callback(
        self,
        pattern: Sequence[float | str],
        procedure: Callable[[OscMessage], Awaitable[None] | None],
        *,
        failure_pattern: Sequence[float | str] | None = None,
        once: bool = False,
        args: tuple | None = None,
        kwargs: dict | None = None,
    ) -> OscCallback:
        """
        Register an OSC callback.
        """
        return self.osc_protocol.register(
            args=args,
            failure_pattern=failure_pattern,
            kwargs=kwargs,
            once=once,
            pattern=pattern,
            procedure=procedure,
        )

    async def reset(self) -> "AsyncServer":
        """
        Reset the server's state without quitting.
        """
        with self.at():
            self.clear_schedule()
            self.free_group_children(self.root_node)
            self.free_all_synthdefs()
        await self.sync()
        self._teardown_state()
        self._setup_allocators(owned=self._is_owner)
        self._setup_system()
        await self.sync()
        return self

    async def sync(
        self, sync_id: int | None = None, timeout: float = 1.0
    ) -> "AsyncServer":
        """
        Sync the server.

        Emit ``/sync`` requests.

        :param sync_id: The sync ID to wait on.
        """
        if self._boot_status not in (BootStatus.BOOTING, BootStatus.ONLINE):
            raise ServerOffline("Server already offline!")
        await Sync(
            sync_id=sync_id if sync_id is not None else self._get_next_sync_id()
        ).communicate_async(server=self, timeout=timeout)
        return self

    def unregister_osc_callback(self, callback: OscCallback) -> None:
        """
        Unregister an OSC callback.

        :param callback: The callback to unregister.
        """
        # TODO: Implemented here because BaseServer does not define _osc_protocol
        self._osc_protocol.unregister(callback)

    ### PUBLIC PROPERTIES ###

    @property
    def boot_future(self) -> asyncio.Future[bool]:
        """
        Get the server's boot future.

        Only reference this _after_ booting or connecting, as the future is
        created when booting or connecting.
        """
        return self._boot_future

    @property
    def exit_future(self) -> asyncio.Future[bool]:
        """
        Get the server's exit future.

        Only reference this _after_ booting or connecting, as the future is
        created when booting or connecting.
        """
        return self._exit_future

    @property
    def osc_protocol(self) -> AsyncOscProtocol:
        """
        Get the server's OSC protocol.
        """
        return self._osc_protocol

    @property
    def process_protocol(self) -> AsyncProcessProtocol:
        """
        Get the server's process protocol.
        """
        return self._process_protocol
