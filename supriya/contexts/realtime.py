import abc
import asyncio
import dataclasses
import enum
import logging
import threading
from typing import (
    TYPE_CHECKING,
    Awaitable,
    Dict,
    List,
    Optional,
    Set,
    SupportsInt,
    Type,
    Union,
    cast,
)

from uqbar.objects import new

from ..assets.synthdefs import system_synthdefs
from ..commands import (
    BufferInfo,
    BufferQueryRequest,
    DoneResponse,
    FailResponse,
    GroupQueryTreeRequest,
    NodeInfo,
    NodeQueryRequest,
    NotifyRequest,
    QuitRequest,
    Requestable,
    SyncRequest,
)
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
from ..querytree import QueryTreeGroup
from ..scsynth import AsyncProcessProtocol, Options, SyncProcessProtocol
from ..synthdefs import SynthDef
from .core import Buffer, Bus, Context, ContextObject, Group, Node

if TYPE_CHECKING:
    from ..realtime.shm import ServerSHM

logger = logging.getLogger(__name__)

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


class RealtimeContext(Context):

    ### CLASS VARIABLES ###

    _contexts: Set["RealtimeContext"] = set()

    ### INITIALIZER ###

    def __init__(
        self, osc_protocol: OscProtocol, options: Optional[Options], **kwargs
    ) -> None:
        super().__init__(options)
        self._is_owner = False
        self._boot_status = BootStatus.OFFLINE
        self._buffers: Set[int] = set()
        self._lock = threading.RLock()
        self._maximum_logins = 1
        self._node_active: Dict[int, bool] = {}
        self._node_children: Dict[int, List[int]] = {}
        self._node_parents: Dict[int, int] = {}
        self._osc_protocol = osc_protocol
        self._shm: Optional["ServerSHM"] = None
        self._setup_osc_callbacks()

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

    def _get_next_sync_id(self) -> int:
        with self._lock:
            sync_id = self._sync_id
            self._sync_id += 1
            if self._sync_id > self._sync_id_maximum:
                self._sync_id = self._sync_id_minimum
            return sync_id

    def _handle_osc_callbacks(self, message: OscMessage) -> None:
        def _handle_done(message: OscMessage) -> None:
            if message.contents[0] in (
                "/b_alloc",
                "/b_allocRead",
                "/b_allocReadChannel",
            ):
                self._buffers.add(message.contents[1])
            elif message.contents[0] == "/b_free":
                self._buffers.remove(message.contents[1])
                self._free_id(Buffer, message.contents[1])

        def _handle_n_end(message: OscMessage) -> None:
            id_, parent_id, *_ = message.contents
            if parent_id == -1:
                parent_id = self._node_parents[id_]
            _remove_node_from_children(id_, parent_id)
            self._free_id(Node, id_)
            self._node_active.pop(id_)
            self._node_children.pop(id_)
            self._node_parents.pop(id_)

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
            "/n_end": _handle_n_end,
            "/n_go": _handle_n_go,
            "/n_move": _handle_n_move,
            "/n_off": _handle_n_off,
            "/n_on": _handle_n_on,
        }

        with self._lock:
            handler = handlers.get(message.address)
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
            ["/n_info"],
            ["/n_move"],
            ["/n_off"],
            ["/n_on"],
            ["/n_set"],
            ["/n_setn"],
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

    @abc.abstractmethod
    def get_bus(self, bus: Bus) -> Union[Awaitable[float], float]:
        raise NotImplementedError

    @abc.abstractmethod
    def query_buffer(self, buffer: Buffer) -> Union[Awaitable[BufferInfo], BufferInfo]:
        raise NotImplementedError

    @abc.abstractmethod
    def query_node(self, node: Node) -> Union[Awaitable[NodeInfo], NodeInfo]:
        raise NotImplementedError

    def send(self, message: Union[OscBundle, OscMessage, Requestable]) -> None:
        if self._boot_status not in (BootStatus.BOOTING, BootStatus.ONLINE):
            raise ServerOffline
        self._osc_protocol.send(
            message.to_osc() if isinstance(message, Requestable) else message
        )

    @abc.abstractmethod
    def query_tree(self) -> Union[Awaitable[QueryTreeGroup], QueryTreeGroup]:
        raise NotImplementedError

    ### PUBLIC PROPERTIES ###

    @property
    def boot_status(self) -> BootStatus:
        return self._boot_status

    @property
    def default_group(self) -> Group:
        return Group(context=self, id_=self._client_id + 1)

    @property
    def is_owner(self) -> bool:
        return self._is_owner

    @property
    def osc_protocol(self) -> OscProtocol:
        return self._osc_protocol


class Server(RealtimeContext):

    ### INITIALIZER ###

    def __init__(self, options: Optional[Options] = None, **kwargs):
        super().__init__(osc_protocol=ThreadedOscProtocol(), options=options, **kwargs)
        self._process_protocol = SyncProcessProtocol()

    ### PRIVATE METHODS ###

    def _connect(self) -> None:
        logger.info("connecting")
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
        self._setup_allocators(self.client_id, self.options)
        if self._client_id == 0:
            self._setup_system()
            self.sync()
        self._boot_status = BootStatus.ONLINE
        logger.info("connected")

    def _disconnect(self) -> None:
        logger.info("disconnecting")
        self._boot_status = BootStatus.QUITTING
        self._teardown_shm()
        cast(ThreadedOscProtocol, self._osc_protocol).disconnect()
        self._teardown_shm()
        self._teardown_state()
        if self in self._contexts:
            self._contexts.remove(self)
        self._is_owner = False
        self._boot_status = BootStatus.OFFLINE
        logger.info("disconnected")

    def _setup_notifications(self) -> None:
        response: Union[DoneResponse, FailResponse] = NotifyRequest(True).communicate(
            server=self
        )
        if isinstance(response, FailResponse):
            self._shutdown()
            raise TooManyClients
        if len(response.action) == 2:  # supernova doesn't provide a max logins value
            self._client_id, self._maximum_logins = (
                response.action[1],
                self._options.maximum_logins,
            )
        else:
            self._client_id, self._maximum_logins = response.action[1:3]

    def _shutdown(self):
        if self.is_owner:
            self.quit()
        else:
            self.disconnect()

    ### PUBLIC METHODS ###

    def boot(self, *, options: Optional[Options] = None, **kwargs) -> "Server":
        if self._boot_status != BootStatus.OFFLINE:
            raise ServerOnline
        self._boot_status = BootStatus.BOOTING
        self._options = new(options or self._options, **kwargs)
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
        if self._boot_status in (BootStatus.BOOTING, BootStatus.ONLINE):
            raise ServerOnline
        self._boot_status = BootStatus.BOOTING
        self._options = new(options or self._options, **kwargs)
        self._is_owner = False
        self._connect()
        return self

    def disconnect(self) -> "Server":
        if self._boot_status == BootStatus.OFFLINE:
            raise ServerOffline
        if self._is_owner:
            raise OwnedServerShutdown("Cannot disconnect from owned server.")
        self._disconnect()
        return self

    async def get_bus(self, bus: Bus) -> float:
        raise NotImplementedError

    def query_buffer(self, buffer: Buffer) -> BufferInfo:
        request = BufferQueryRequest(buffer_ids=[buffer.id_])
        response = request.communicate(server=self)
        return response

    def query_node(self, node: Node) -> NodeInfo:
        return NodeQueryRequest(node_id=node).communicate(server=self)

    def query_tree(self) -> Union[Awaitable[QueryTreeGroup], QueryTreeGroup]:
        request = GroupQueryTreeRequest(node_id=0, include_controls=True)
        response = request.communicate(server=self)
        return response.query_tree_group

    def quit(self, force: bool = False) -> "Server":
        if self._boot_status != BootStatus.ONLINE:
            return self
        if not self._is_owner and not force:
            raise UnownedServerShutdown(
                "Cannot quit unowned server without force flag."
            )
        try:
            QuitRequest().communicate(server=self)
        except OscProtocolOffline:
            pass
        self._teardown_shm()
        self._process_protocol.quit()
        self._disconnect()
        return self

    def sync(self, sync_id: Optional[int] = None) -> "Server":
        if self._boot_status not in (BootStatus.BOOTING, BootStatus.ONLINE):
            raise ServerOffline
        SyncRequest(
            sync_id=sync_id if sync_id is not None else self._get_next_sync_id()
        ).communicate(server=self)
        return self


class AsyncServer(RealtimeContext):

    ### INITIALIZER ###

    def __init__(self, options: Optional[Options] = None, **kwargs):
        super().__init__(osc_protocol=AsyncOscProtocol(), options=options, **kwargs)
        self._process_protocol = AsyncProcessProtocol()

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
        self._setup_allocators(self.client_id, self.options)
        if self._client_id == 0:
            self._setup_system()
            await self.sync()
        self._boot_status = BootStatus.ONLINE
        logger.info("Connected")

    async def _disconnect(self) -> None:
        logger.info("Disconnecting")
        self._boot_status = BootStatus.QUITTING
        await cast(AsyncOscProtocol, self._osc_protocol).disconnect()
        self._teardown_shm()
        self._teardown_state()
        if self in self._contexts:
            self._contexts.remove(self)
        self._is_owner = False
        self._boot_status = BootStatus.OFFLINE
        logger.info("Disconnected")

    async def _setup_notifications(self) -> None:
        logger.info("Setting up notifications")
        response: Union[DoneResponse, FailResponse] = await NotifyRequest(
            True
        ).communicate_async(server=self)
        if isinstance(response, FailResponse):
            await self._shutdown()
            raise TooManyClients
        if len(response.action) == 2:  # supernova doesn't provide a max logins value
            self._client_id, self._maximum_logins = (
                response.action[1],
                self._options.maximum_logins,
            )
        else:
            self._client_id, self._maximum_logins = response.action[1:3]

    async def _shutdown(self):
        if self.is_owner:
            await self.quit()
        else:
            await self.disconnect()

    ### PUBLIC METHODS ###

    async def boot(
        self, *, options: Optional[Options] = None, **kwargs
    ) -> "AsyncServer":
        if self._boot_status != BootStatus.OFFLINE:
            raise ServerOnline
        self._boot_status = BootStatus.BOOTING
        self._options = new(options or self._options, **kwargs)
        await self._process_protocol.boot(self._options)
        if not await self._process_protocol.boot_future:
            self._boot_status = BootStatus.OFFLINE
            raise ServerCannotBoot
        self._is_owner = True
        await self._connect()
        return self

    async def connect(
        self, *, options: Optional[Options] = None, **kwargs
    ) -> "AsyncServer":
        if self._boot_status in (BootStatus.BOOTING, BootStatus.ONLINE):
            raise ServerOnline
        self._boot_status = BootStatus.BOOTING
        self._options = new(options or self._options, **kwargs)
        self._is_owner = False
        await self._connect()
        return self

    async def disconnect(self) -> "AsyncServer":
        if self._boot_status == BootStatus.OFFLINE:
            raise ServerOffline
        if self._is_owner:
            raise OwnedServerShutdown("Cannot disconnect from owned server.")
        await self._disconnect()
        return self

    async def get_bus(self, bus: Bus) -> float:
        raise NotImplementedError

    async def query_buffer(self, buffer: Buffer) -> BufferInfo:
        request = BufferQueryRequest(buffer_ids=[buffer.id_])
        response = await request.communicate_async(server=self)
        return response

    async def query_node(self, node: Node) -> NodeInfo:
        return await NodeQueryRequest(node_id=node).communicate_async(server=self)

    async def query_tree(self) -> QueryTreeGroup:
        request = GroupQueryTreeRequest(node_id=0, include_controls=True)
        response = await request.communicate_async(server=self)
        return response.query_tree_group

    async def quit(self, force: bool = False) -> "AsyncServer":
        if self._boot_status != BootStatus.ONLINE:
            return self
        if not self._is_owner and not force:
            raise UnownedServerShutdown(
                "Cannot quit unowned server without force flag."
            )
        try:
            await QuitRequest().communicate_async(server=self, sync=True, timeout=1)
        except (OscProtocolOffline, asyncio.TimeoutError):
            pass
        self._process_protocol.quit()
        await self._disconnect()
        return self

    async def sync(self, sync_id: Optional[int] = None) -> "AsyncServer":
        if self._boot_status not in (BootStatus.BOOTING, BootStatus.ONLINE):
            raise ServerOffline
        await SyncRequest(
            sync_id=sync_id if sync_id is not None else self._get_next_sync_id()
        ).communicate_async(server=self)
        return self
