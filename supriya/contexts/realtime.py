"""
Tools for interacting with realtime execution contexts.
"""

import asyncio
import dataclasses
import enum
import logging
import warnings
from typing import (
    TYPE_CHECKING,
    Dict,
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
from ..synthdefs import SynthDef
from ..typing import SupportsOsc
from .core import (
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
    ...


warnings.simplefilter("always", FailWarning)


DEFAULT_HEALTHCHECK = HealthCheck(
    active=False,
    backoff_factor=1.5,
    callback=lambda: None,
    max_attempts=5,
    request_pattern=["/status"],
    response_pattern=["/status.reply"],
    timeout=1.0,
)


class BootStatus(enum.IntEnum):
    OFFLINE = 0
    BOOTING = 1
    ONLINE = 2
    QUITTING = 3


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
        options: Optional[Options],
        osc_protocol: OscProtocol,
        process_protocol: ProcessProtocol,
        **kwargs,
    ) -> None:
        super().__init__(options)
        self._latency = 0.1
        self._is_owner = False
        self._boot_status = BootStatus.OFFLINE
        self._buffers: Set[int] = set()
        self._maximum_logins = 1
        self._node_active: Dict[int, bool] = {}
        self._node_children: Dict[int, List[int]] = {}
        self._node_parents: Dict[int, int] = {}
        self._osc_protocol = osc_protocol
        self._process_protocol = process_protocol
        self._shm: Optional["ServerSHM"] = None
        self._setup_osc_callbacks()
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

    def _free_id(
        self,
        type_: Type[ContextObject],
        id_: int,
        calculation_rate: Optional[CalculationRate] = None,
    ) -> None:
        self._get_allocator(type_, calculation_rate).free(id_)

    def _handle_osc_callbacks(self, message: OscMessage) -> None:
        def _handle_done(message: OscMessage) -> None:
            if message.contents[0] in (
                "/b_alloc",
                "/b_allocRead",
                "/b_allocReadChannel",
            ):
                self._buffers.add(message.contents[1])
            elif message.contents[0] == "/b_free":
                if message.contents[1] in self._buffers:
                    self._buffers.remove(message.contents[1])
                self._free_id(Buffer, message.contents[1])

        def _handle_fail(message: OscMessage) -> None:
            warnings.warn(" ".join(str(x) for x in message.contents), FailWarning)

        def _handle_n_end(message: OscMessage) -> None:
            id_, parent_id, *_ = message.contents
            if parent_id == -1:
                parent_id = self._node_parents.get(id_)
            if parent_id is not None:
                _remove_node_from_children(id_, parent_id)
            self._free_id(Node, id_)
            self._node_active.pop(id_, None)
            self._node_children.pop(id_, None)
            self._node_parents.pop(id_, None)

        def _handle_n_go(message: OscMessage) -> None:
            id_, parent_id, previous_id, next_id, is_group, *_ = message.contents
            self._node_parents[id_] = parent_id
            self._node_active[id_] = True
            if is_group:
                self._node_children[id_] = []
            _add_node_to_children(id_, parent_id, previous_id, next_id)

        def _handle_n_move(message: OscMessage) -> None:
            id_, parent_id, previous_id, next_id, *_ = message.contents
            old_parent_id = self._node_parents[id_]
            _remove_node_from_children(id_, old_parent_id)
            _add_node_to_children(id_, parent_id, previous_id, next_id)

        def _handle_n_off(message: OscMessage) -> None:
            self._node_active[message.contents[0]] = False

        def _handle_n_on(message: OscMessage) -> None:
            self._node_active[message.contents[0]] = True

        def _handle_status_reply(message: OscMessage):
            self._status = cast(StatusInfo, StatusInfo.from_osc(message))

        def _add_node_to_children(
            id_: int, parent_id: int, previous_id: int, next_id: int
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

        def _remove_node_from_children(id_: int, parent_id: int) -> None:
            children = self._node_children[parent_id]
            try:
                children.pop(children.index(id_))
            except ValueError:
                pass

        handlers = {
            "/done": _handle_done,
            "/fail": _handle_fail,
            "/n_end": _handle_n_end,
            "/n_go": _handle_n_go,
            "/n_move": _handle_n_move,
            "/n_off": _handle_n_off,
            "/n_on": _handle_n_on,
            "/status.reply": _handle_status_reply,
        }

        with self._lock:
            handler = handlers.get(str(message.address))
            if handler is not None:
                handler(message)

    def _resolve_node(self, node: Union[Node, SupportsInt, None]) -> int:
        if node is None:
            return self._client_id + 1
        return int(node)

    def _setup_osc_callbacks(self) -> None:
        for pattern in (
            ["/done"],
            ["/fail"],
            ["/n_end"],
            ["/n_go"],
            ["/n_move"],
            ["/n_off"],
            ["/n_on"],
            ["/status.reply"],
        ):
            self._osc_protocol.register(
                pattern=pattern, procedure=self._handle_osc_callbacks
            )

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

    def send(self, message: SupportsOsc) -> None:
        """
        Send a message to the execution context.

        :param message: The message to send.
        """
        if self._boot_status not in (BootStatus.BOOTING, BootStatus.ONLINE):
            raise ServerOffline
        self._osc_protocol.send(
            message.to_osc() if hasattr(message, "to_osc") else message
        )

    def set_latency(self, latency: float) -> None:
        """
        Set the context's latency.

        :param latency: The latency in seconds.
        """
        self._latency = float(latency)

    ### PUBLIC PROPERTIES ###

    @property
    def boot_status(self) -> BootStatus:
        """
        Get the server's boot status.
        """
        return self._boot_status

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

    def __init__(self, options: Optional[Options] = None, **kwargs):
        super().__init__(
            osc_protocol=ThreadedOscProtocol(),
            options=options,
            process_protocol=SyncProcessProtocol(),
            **kwargs,
        )

    ### PRIVATE METHODS ###

    def _connect(self) -> None:
        logger.info("Connecting")
        cast(ThreadedOscProtocol, self._osc_protocol).connect(
            ip_address=self._options.ip_address,
            port=self._options.port,
            healthcheck=dataclasses.replace(
                DEFAULT_HEALTHCHECK, callback=self._shutdown
            ),
        )
        self._setup_notifications()
        self._contexts.add(self)
        self._osc_protocol.activate_healthcheck()
        self._setup_allocators()
        if self._client_id == 0:
            self._setup_system()
            self.sync()
        self._boot_status = BootStatus.ONLINE
        logger.info("Connected")

    def _disconnect(self) -> None:
        logger.info("Disconnecting")
        self._boot_status = BootStatus.QUITTING
        self._teardown_shm()
        self._osc_protocol.disconnect()
        self._teardown_shm()
        self._teardown_state()
        if self in self._contexts:
            self._contexts.remove(self)
        self._is_owner = False
        self._boot_status = BootStatus.OFFLINE
        logger.info("Disconnected")

    def _setup_notifications(self) -> None:
        logger.info("Setting up notifications")
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
        self._boot_status = BootStatus.BOOTING
        self._options = new(options or self._options, **kwargs)
        logger.debug(f"Options: {self._options}")
        try:
            self._process_protocol.boot(self._options)
        except ServerCannotBoot:
            self._boot_status = BootStatus.OFFLINE
            raise
        self._is_owner = True
        self._connect()
        self._setup_shm()
        return self

    def connect(self, *, options: Optional[Options] = None, **kwargs) -> "Server":
        """
        Connect to a running server.

        :param options: The context's options.
        :param kwargs: Keyword arguments for options.
        """
        if self._boot_status in (BootStatus.BOOTING, BootStatus.ONLINE):
            raise ServerOnline
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
        self._disconnect()
        return self

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
        try:
            Quit().communicate(server=self)
        except OscProtocolOffline:
            pass
        self._teardown_shm()
        self._process_protocol.quit()
        self._disconnect()
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
            self.free_all_synthdefs()
            self.free_group_children(self.root_node)
        self.sync()
        self._teardown_state()
        self._setup_allocators()
        self._setup_system()
        self.sync()
        return self

    def sync(self, sync_id: Optional[int] = None) -> "Server":
        """
        Sync the server.

        Emit ``/sync`` requests.

        :param sync_id: The sync ID to wait on.
        """
        if self._boot_status not in (BootStatus.BOOTING, BootStatus.ONLINE):
            raise ServerOffline
        Sync(
            sync_id=sync_id if sync_id is not None else self._get_next_sync_id()
        ).communicate(server=self)
        return self


class AsyncServer(BaseServer):
    """
    A realtime execution context with :py:mod:`asyncio`-based OSC and process protocols.

    :param options: The context's options.
    :param kwargs: Keyword arguments for options.
    """

    ### INITIALIZER ###

    def __init__(self, options: Optional[Options] = None, **kwargs):
        super().__init__(
            osc_protocol=AsyncOscProtocol(),
            options=options,
            process_protocol=AsyncProcessProtocol(),
            **kwargs,
        )

    ### PRIVATE METHODS ###

    async def _connect(self) -> None:
        logger.info("Connecting")
        await cast(AsyncOscProtocol, self._osc_protocol).connect(
            ip_address=self._options.ip_address,
            port=self._options.port,
            healthcheck=dataclasses.replace(
                DEFAULT_HEALTHCHECK, callback=self._shutdown
            ),
        )
        await self._setup_notifications()
        self._contexts.add(self)
        self._osc_protocol.activate_healthcheck()
        self._setup_allocators()
        if self._client_id == 0:
            self._setup_system()
            await self.sync()
        self._boot_status = BootStatus.ONLINE
        logger.info("Connected")

    async def _disconnect(self) -> None:
        logger.info("Disconnecting")
        self._boot_status = BootStatus.QUITTING
        self._osc_protocol.disconnect()
        self._teardown_shm()
        self._teardown_state()
        if self in self._contexts:
            self._contexts.remove(self)
        self._is_owner = False
        self._boot_status = BootStatus.OFFLINE
        logger.info("Disconnected")

    async def _setup_notifications(self) -> None:
        logger.info("Setting up notifications")
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
        self._boot_status = BootStatus.BOOTING
        self._options = new(options or self._options, **kwargs)
        logger.debug(f"Options: {self._options}")
        try:
            await self._process_protocol.boot(self._options)
        except ServerCannotBoot:
            self._boot_status = BootStatus.OFFLINE
            raise
        self._is_owner = True
        await self._connect()
        return self

    async def connect(
        self, *, options: Optional[Options] = None, **kwargs
    ) -> "AsyncServer":
        """
        Connect to a running server.

        :param options: The context's options.
        :param kwargs: Keyword arguments for options.
        """
        if self._boot_status in (BootStatus.BOOTING, BootStatus.ONLINE):
            raise ServerOnline
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
        await self._disconnect()
        return self

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
        try:
            await Quit().communicate_async(server=self, timeout=1)
        except (OscProtocolOffline, asyncio.TimeoutError):
            pass
        await self._process_protocol.quit()
        await self._disconnect()
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

    async def sync(self, sync_id: Optional[int] = None) -> "AsyncServer":
        """
        Sync the server.

        Emit ``/sync`` requests.

        :param sync_id: The sync ID to wait on.
        """
        if self._boot_status not in (BootStatus.BOOTING, BootStatus.ONLINE):
            raise ServerOffline
        await Sync(
            sync_id=sync_id if sync_id is not None else self._get_next_sync_id()
        ).communicate_async(server=self)
        return self
