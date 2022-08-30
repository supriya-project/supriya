import abc
import collections
import contextlib
import dataclasses
import os
import pathlib
import re
import tempfile
from types import MappingProxyType
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
)

from uqbar.objects import new

import supriya.nonrealtime  # noqa
import supriya.realtime  # noqa
from supriya import commands, nonrealtime, realtime
from supriya.assets.synthdefs.default import default
from supriya.enums import AddAction, CalculationRate, ParameterRate
from supriya.nonrealtime import Session
from supriya.realtime import AsyncServer, BaseServer, Server
from supriya.synthdefs import SynthDef
from supriya.typing import AddActionLike, HeaderFormatLike, SampleFormatLike


@dataclasses.dataclass(frozen=True)
class Proxy:
    provider: "Provider"


@dataclasses.dataclass(frozen=True)
class BufferProxy:
    provider: "Provider"
    identifier: Union["supriya.nonrealtime.Buffer", int]
    channel_count: Optional[int] = None
    frame_count: Optional[int] = None
    file_path: Optional[os.PathLike] = None
    starting_frame: Optional[int] = None

    def __float__(self) -> float:
        return float(int(self))

    def __int__(self) -> int:
        return int(self.identifier)

    def close(self) -> None:
        pass

    def free(self) -> None:
        self.provider.free_buffer(self)

    def normalize(self, new_maximum: float = 1.0) -> None:
        pass

    def read(self, file_path: os.PathLike, leave_open: bool = False) -> None:
        pass

    def write(
        self,
        file_path: os.PathLike,
        frame_count: Optional[int] = None,
        header_format: HeaderFormatLike = "aiff",
        leave_open: bool = False,
        sample_format: SampleFormatLike = "int24",
        starting_frame: Optional[int] = None,
    ) -> None:
        pass

    def as_allocate_request(
        self,
    ) -> Union[
        commands.BufferAllocateRequest,
        commands.BufferAllocateReadRequest,
        commands.BufferAllocateReadChannelRequest,
    ]:
        kwargs: Dict[str, Any] = dict(buffer_id=int(self), frame_count=self.frame_count)
        if self.file_path is None:
            return commands.BufferAllocateRequest(
                **kwargs, channel_count=self.channel_count
            )
        kwargs["file_path"] = self.file_path
        kwargs["starting_frame"] = self.starting_frame
        if self.channel_count is None:
            return commands.BufferAllocateReadRequest(**kwargs)
        return commands.BufferAllocateReadChannelRequest(
            **kwargs, channel_indices=list(range(self.channel_count))
        )

    def as_free_request(self) -> commands.BufferFreeRequest:
        return commands.BufferFreeRequest(buffer_id=int(self))


@dataclasses.dataclass(frozen=True)
class OscCallbackProxy(Proxy):
    provider: "Provider"
    identifier: Any

    def unregister(self) -> None:
        self.provider.unregister_osc_callback(self)


@dataclasses.dataclass(frozen=True)
class BusProxy(Proxy):
    calculation_rate: CalculationRate
    provider: "Provider"
    identifier: Union["supriya.nonrealtime.Bus", int]

    def __float__(self) -> float:
        return float(int(self))

    def __int__(self) -> int:
        return int(self.identifier)

    def set_(self, value) -> None:
        self.provider.set_bus(self, value)

    def free(self) -> None:
        self.provider.free_bus(self)

    @property
    def map_symbol(self) -> str:
        if self.calculation_rate == CalculationRate.AUDIO:
            return f"a{int(self)}"
        return f"c{int(self)}"


@dataclasses.dataclass(frozen=True)
class BusGroupProxy(Proxy):
    calculation_rate: CalculationRate
    channel_count: int
    identifier: Union["supriya.nonrealtime.BusGroup", int]
    provider: "Provider"
    buses: Sequence["BusProxy"] = dataclasses.field(init=False)

    def __post_init__(self):
        if isinstance(self.identifier, int):
            bus_identifiers = range(
                self.identifier, self.identifier + self.channel_count
            )
        else:
            bus_identifiers = self.identifier[:]
        object.__setattr__(
            self,
            "buses",
            tuple(
                BusProxy(
                    calculation_rate=self.calculation_rate,
                    provider=self.provider,
                    identifier=bus_identifier,
                )
                for bus_identifier in bus_identifiers
            ),
        )

    def __float__(self) -> float:
        return float(int(self))

    def __getitem__(self, item) -> BusProxy:
        return self.buses[item]

    def __int__(self) -> int:
        return int(self.identifier)

    def __len__(self) -> int:
        return self.channel_count

    def free(self) -> None:
        self.provider.free_bus_group(self)

    @property
    def map_symbol(self) -> str:
        return self[0].map_symbol


@dataclasses.dataclass(frozen=True)
class NodeProxy(Proxy):
    identifier: Union["supriya.nonrealtime.Node", int]
    provider: "Provider"

    def __float__(self) -> float:
        return float(int(self))

    def __int__(self) -> int:
        return int(self.identifier)

    def __setitem__(self, key, value) -> None:
        self.provider.set_node(self, **{key: value})

    def add_group(
        self,
        *,
        add_action: AddActionLike = AddAction.ADD_TO_HEAD,
        name: Optional[str] = None,
    ) -> "GroupProxy":
        return self.provider.add_group(add_action=add_action, target_node=self)

    def add_synth(
        self,
        *,
        synthdef: Optional[SynthDef] = None,
        add_action: AddActionLike = AddAction.ADD_TO_HEAD,
        name: Optional[str] = None,
        **settings,
    ) -> "SynthProxy":
        return self.provider.add_synth(
            add_action=add_action, synthdef=synthdef, target_node=self, **settings
        )

    def as_move_request(
        self, add_action: AddActionLike, target_node: "NodeProxy"
    ) -> commands.MoveRequest:
        request_classes: Dict[int, Type[commands.MoveRequest]] = {
            AddAction.ADD_TO_HEAD: commands.GroupHeadRequest,
            AddAction.ADD_TO_TAIL: commands.GroupTailRequest,
            AddAction.ADD_BEFORE: commands.NodeBeforeRequest,
            AddAction.ADD_AFTER: commands.NodeAfterRequest,
        }
        request_class: Type[commands.MoveRequest] = request_classes[
            AddAction.from_expr(add_action)
        ]
        return request_class(
            node_id_pairs=[request_class.NodeIdPair(int(self), int(target_node))]
        )

    def as_set_request(self, **settings) -> commands.NodeSetRequest:
        coerced_settings = {}
        for key, value in settings.items():
            if isinstance(value, (BusProxy, BusGroupProxy)):
                if value.calculation_rate == CalculationRate.AUDIO:
                    value = f"a{value.identifier}"
                else:
                    value = f"c{value.identifier}"
            coerced_settings[key] = value
        return commands.NodeSetRequest(node_id=int(self), **coerced_settings)

    def dispose(self) -> None:
        self.provider.dispose(self)

    def free(self) -> None:
        self.provider.free_node(self)

    def move(self, add_action: AddActionLike, target_node: "NodeProxy") -> None:
        self.provider.move_node(self, add_action, target_node)


@dataclasses.dataclass(frozen=True)
class GroupProxy(NodeProxy):
    identifier: Union["supriya.nonrealtime.Node", int]
    provider: "Provider"

    def as_add_request(self, add_action, target_node) -> commands.GroupNewRequest:
        return commands.GroupNewRequest(
            items=[
                commands.GroupNewRequest.Item(
                    node_id=int(self.identifier),
                    add_action=add_action,
                    target_node_id=int(target_node),
                )
            ]
        )

    def as_free_request(self, force=False) -> commands.NodeFreeRequest:
        return commands.NodeFreeRequest(node_ids=[int(self)])


@dataclasses.dataclass(frozen=True)
class SynthProxy(NodeProxy):
    identifier: Union["supriya.nonrealtime.Node", int]
    provider: "Provider"
    synthdef: SynthDef
    settings: Dict[str, Union[float, BusGroupProxy]]

    def as_add_request(self, add_action, target_node) -> commands.SynthNewRequest:
        # TODO: Handle map symbols
        #       If arg is a bus proxy, and synth param is scalar, cast to int
        #       Elif arg is a bus proxy, and synth param not scalar, map
        #       Else cast to float
        synthdef = self.synthdef or default

        synthdef_kwargs: Dict[str, Union[float, str]] = {}
        for _, parameter in synthdef.indexed_parameters:
            if parameter.name not in self.settings:
                continue
            value = self.settings[parameter.name]
            if value == parameter.value:
                continue
            if parameter.parameter_rate == ParameterRate.SCALAR:
                synthdef_kwargs[parameter.name] = float(value)
            elif parameter.name in ("in_", "out"):
                synthdef_kwargs[parameter.name] = float(value)
            elif isinstance(value, (BusProxy, BusGroupProxy)):
                synthdef_kwargs[parameter.name] = value.map_symbol
            else:
                synthdef_kwargs[parameter.name] = float(value)

        return commands.SynthNewRequest(
            node_id=int(self.identifier),
            add_action=add_action,
            target_node_id=int(target_node),
            synthdef=synthdef,
            **synthdef_kwargs,
        )

    def as_free_request(
        self, force=False
    ) -> Union[commands.NodeFreeRequest, commands.NodeSetRequest]:
        if force or "gate" not in self.synthdef.parameters:
            return commands.NodeFreeRequest(node_ids=[int(self)])
        return commands.NodeSetRequest(node_id=int(self), gate=0)


@dataclasses.dataclass(frozen=True)
class ProviderMoment:
    provider: "Provider"
    seconds: float
    bus_settings: List[Tuple[BusProxy, float]] = dataclasses.field(default_factory=list)
    buffer_additions: List[BufferProxy] = dataclasses.field(default_factory=list)
    buffer_removals: List[BufferProxy] = dataclasses.field(default_factory=list)
    node_reorderings: List[Tuple[NodeProxy, AddAction, NodeProxy]] = dataclasses.field(
        default_factory=list
    )
    node_additions: List[Tuple[NodeProxy, AddAction, NodeProxy]] = dataclasses.field(
        default_factory=list
    )
    node_removals: List[NodeProxy] = dataclasses.field(default_factory=list)
    node_settings: List[
        Tuple[NodeProxy, Dict[str, Union[float, BusGroupProxy]]]
    ] = dataclasses.field(default_factory=list)
    wait: bool = dataclasses.field(default=False)
    exit_stack: contextlib.ExitStack = dataclasses.field(
        init=False, default_factory=contextlib.ExitStack, compare=False
    )

    async def __aenter__(self):
        if self.provider.server and not isinstance(self.provider.server, AsyncServer):
            raise RuntimeError(repr(self.provider.server))
        return self._enter()

    async def __aexit__(self, *args):
        results = self._exit()
        if not results:
            return
        timestamp, request_bundle, synthdefs = results
        server = self.provider.server
        # The underlying asyncio UDP transport will silently drop oversize packets
        if len(request_bundle.to_datagram()) <= 8192:
            if self.wait:
                # If waiting, the original ProviderMoment timestamp can be ignored
                await request_bundle.communicate_async(server=server, sync=True)
            else:
                server.send(request_bundle.to_osc())
        else:
            # If over the UDP packet limit, partition the message
            requests = request_bundle.contents
            # Always wait for SynthDefs to load.
            if synthdefs:
                synthdef_request = requests[0]
                requests = synthdef_request.callback.contents or []
                synthdef_request = new(synthdef_request, callback=None)
                await synthdef_request.communicate_async(sync=True, server=server)
            if self.wait:
                # If waiting, the original ProviderMoment timestamp can be ignored
                for bundle in commands.RequestBundle.partition(requests):
                    await bundle.communicate_async(server=server, sync=True)
            else:
                for bundle in commands.RequestBundle.partition(
                    requests, timestamp=timestamp
                ):
                    server.send(bundle.to_osc())

    def __enter__(self):
        if self.provider.session is not None:
            self.exit_stack.enter_context(self.provider.session.at(self.seconds or 0))
        if self.provider.server and not isinstance(self.provider.server, Server):
            raise RuntimeError(repr(self.provider.server))
        return self._enter()

    def __exit__(self, *args):
        results = self._exit()
        if not results:
            return
        timestamp, request_bundle, synthdefs = results
        try:
            self.provider.server.send(request_bundle.to_osc())
        except OSError:
            requests = request_bundle.contents
            if synthdefs:
                synthdef_request = requests[0]
                requests = synthdef_request.callback.contents or []
                synthdef_request = new(synthdef_request, callback=None)
                synthdef_request.communicate(sync=True, server=self.provider.server)
            for bundle in commands.RequestBundle.partition(
                requests, timestamp=timestamp
            ):
                self.provider.server.send(bundle.to_osc())

    def _enter(self):
        self.provider._moments.append(self)
        self.provider._counter[self.seconds] += 1
        return self

    def _exit(self):
        self.exit_stack.close()
        self.provider._moments.pop()
        self.provider._counter[self.seconds] -= 1
        if not self.provider.server:
            return
        elif self.provider._counter[self.seconds]:
            return
        requests = []
        synthdefs = set()
        new_nodes = set()
        for buffer_proxy in self.buffer_additions:
            requests.append(buffer_proxy.as_allocate_request())
        for node_proxy, add_action, target_node in self.node_additions:
            request = node_proxy.as_add_request(add_action, target_node)
            if isinstance(request, commands.SynthNewRequest):
                if request.synthdef not in self.provider.server:
                    synthdefs.add(request.synthdef)
            requests.append(request)
            new_nodes.add(node_proxy.identifier)
        for node_proxy, add_action, target_node in self.node_reorderings:
            requests.append(node_proxy.as_move_request(add_action, target_node))
        for node_proxy, settings in self.node_settings:
            requests.append(node_proxy.as_set_request(**settings))
        for node_proxy in self.node_removals:
            requests.append(
                node_proxy.as_free_request(force=node_proxy.identifier in new_nodes)
            )
        for buffer_proxy in self.buffer_removals:
            requests.append(buffer_proxy.as_free_request())
        if self.bus_settings:
            sorted_pairs = sorted(
                dict(
                    (int(bus_proxy.identifier), value)
                    for bus_proxy, value in self.bus_settings
                ).items()
            )
            request = commands.ControlBusSetRequest(index_value_pairs=sorted_pairs)
            requests.append(request)
        if not requests:
            return
        timestamp = self.seconds
        if timestamp is not None:
            timestamp += self.provider._latency
        if synthdefs:
            request_bundle = commands.RequestBundle(
                timestamp=timestamp,
                contents=[
                    commands.SynthDefReceiveRequest(
                        synthdefs=sorted(synthdefs, key=lambda x: x.actual_name),
                        callback=commands.RequestBundle(contents=requests),
                    )
                ],
            )
            # check bundle size, write synthdefs to disk and do /d_load
            if len(request_bundle.to_datagram(with_placeholders=True)) > 8192:
                directory_path = pathlib.Path(tempfile.mkdtemp())
                # directory_path = pathlib.Path("~/Desktop").resolve()
                for synthdef in synthdefs:
                    name = synthdef.anonymous_name
                    if synthdef.name:
                        name += "-" + re.sub(r"[^\w]", "-", synthdef.name)
                    file_name = "{}.scsyndef".format(name)
                    synthdef_path = directory_path / file_name
                    synthdef_path.write_bytes(synthdef.compile())
                request_bundle = commands.RequestBundle(
                    timestamp=timestamp,
                    contents=[
                        supriya.commands.SynthDefLoadDirectoryRequest(
                            directory_path=directory_path,
                            callback=commands.RequestBundle(contents=requests),
                        )
                    ],
                )
        else:
            request_bundle = commands.RequestBundle(
                timestamp=timestamp, contents=requests
            )
        for synthdef in synthdefs:
            synthdef._register_with_local_server(server=self.provider.server)
        return timestamp, request_bundle, synthdefs


class Provider(metaclass=abc.ABCMeta):
    """
    Provides limited realtime/non-realtime compatibility layer.
    """

    ### INITIALIZER ###

    def __init__(self, latency=0.1):
        self._moments: List[ProviderMoment] = []
        self._counter = collections.Counter()
        self._latency: float = latency
        self._annotation_map: Dict[Union["supriya.nonrealtime.Node", int], str] = {}

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def add_buffer(
        self,
        *,
        channel_count: Optional[int] = None,
        file_path: Optional[os.PathLike] = None,
        frame_count: Optional[int] = None,
        starting_frame: Optional[int] = None,
    ) -> BufferProxy:
        raise NotImplementedError

    @abc.abstractmethod
    def add_bus(self, calculation_rate=CalculationRate.CONTROL) -> BusProxy:
        raise NotImplementedError

    @abc.abstractmethod
    def add_bus_group(
        self, channel_count=1, calculation_rate=CalculationRate.CONTROL
    ) -> BusGroupProxy:
        raise NotImplementedError

    @abc.abstractmethod
    def add_group(
        self,
        *,
        target_node=None,
        add_action=AddAction.ADD_TO_HEAD,
        name: Optional[str] = None,
    ) -> GroupProxy:
        raise NotImplementedError

    @abc.abstractmethod
    def add_synth(
        self,
        *,
        synthdef: SynthDef = None,
        target_node=None,
        add_action=AddAction.ADD_TO_HEAD,
        name: Optional[str] = None,
        **settings,
    ) -> SynthProxy:
        raise NotImplementedError

    @abc.abstractmethod
    def dispose(self, node_proxy: NodeProxy) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def free_buffer(self, buffer_proxy) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def free_bus(self, bus_proxy: BusProxy) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def free_bus_group(self, bus_group_proxy: BusGroupProxy) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def free_node(self, node_proxy: NodeProxy) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def move_node(
        self, node_proxy: NodeProxy, add_action: AddActionLike, target_node: NodeProxy
    ) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def set_bus(self, bus_proxy: BusProxy, value: float) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def set_node(self, node_proxy: NodeProxy, **settings) -> None:
        raise NotImplementedError

    def at(self, seconds=None, wait=False) -> ProviderMoment:
        if self._moments and self._moments[-1].seconds == seconds:
            provider_moment = self._moments[-1]
        else:
            provider_moment = ProviderMoment(provider=self, seconds=seconds, wait=wait)
        return provider_moment

    @classmethod
    def from_context(cls, context, latency=0.1) -> "Provider":
        if isinstance(context, Session):
            return NonrealtimeProvider(context, latency=latency)
        elif isinstance(context, BaseServer):
            return RealtimeProvider(context, latency=latency)
        raise ValueError("Unknown context")

    @classmethod
    def nonrealtime(cls) -> "NonrealtimeProvider":
        session = Session()
        return cast("NonrealtimeProvider", cls.from_context(session))

    @classmethod
    def realtime(
        cls, scsynth_path=None, options=None, port=None, **kwargs
    ) -> "RealtimeProvider":
        server = Server()
        server.boot(port=port, scsynth_path=scsynth_path, options=options, **kwargs)
        return cast("RealtimeProvider", cls.from_context(server))

    @classmethod
    async def realtime_async(
        cls, scsynth_path=None, options=None, port=None, **kwargs
    ) -> "RealtimeProvider":
        server = AsyncServer()
        await server.boot(
            port=port, scsynth_path=scsynth_path, options=options, **kwargs
        )
        return cast("RealtimeProvider", cls.from_context(server))

    @abc.abstractmethod
    def register_osc_callback(
        self, pattern: Tuple[Union[str, float], ...], procedure: Callable
    ) -> OscCallbackProxy:
        raise NotImplementedError

    @abc.abstractmethod
    def unregister_osc_callback(self, proxy: OscCallbackProxy) -> None:
        raise NotImplementedError

    ### PUBLIC PROPERTIES ###

    @property
    def annotation_map(self) -> Mapping[Union["supriya.nonrealtime.Node", int], str]:
        return MappingProxyType(self._annotation_map)

    @property
    def latency(self) -> float:
        return self._latency

    @property
    def moment(self) -> Optional[ProviderMoment]:
        if self._moments:
            return self._moments[-1]
        return None

    @property
    def server(self) -> Optional[BaseServer]:
        return None

    @property
    def session(self) -> Optional[Session]:
        return None


class NonrealtimeProvider(Provider):

    ### INITIALIZER ###

    def __init__(self, session: Session, latency: float = 0.1):
        if not isinstance(session, Session):
            raise ValueError(f"Expected session, got {session}")
        Provider.__init__(self, latency=latency)
        self._session: Session = session

    ### SPECIAL METHODS ###

    def __str__(self) -> str:
        return f"<{type(self).__name__} {self._session!r}>"

    ### PRIVATE METHODS ###

    def _resolve_target_node(self, target_node) -> nonrealtime.Node:
        if target_node is None:
            target_node = self._session.root_node
        elif isinstance(target_node, NodeProxy):
            target_node = target_node.identifier
        return target_node

    ### PUBLIC METHODS ###

    def add_buffer(
        self,
        *,
        channel_count: Optional[int] = None,
        file_path: Optional[os.PathLike] = None,
        frame_count: Optional[int] = None,
        starting_frame: Optional[int] = None,
    ) -> BufferProxy:
        if not self.moment:
            raise ValueError("No current moment")
        identifier = self._session.add_buffer(
            channel_count=channel_count,
            file_path=file_path,
            frame_count=frame_count,
            starting_frame=starting_frame,
        )
        return BufferProxy(
            channel_count=channel_count,
            file_path=file_path,
            frame_count=frame_count,
            identifier=identifier,
            provider=self,
            starting_frame=starting_frame,
        )

    def add_bus(self, calculation_rate=CalculationRate.CONTROL) -> BusProxy:
        if not self.moment:
            raise ValueError("No current moment")
        calculation_rate = CalculationRate.from_expr(calculation_rate)
        if calculation_rate not in (CalculationRate.AUDIO, CalculationRate.CONTROL):
            raise ValueError(f"Invalid calculation rate: {calculation_rate!r}")
        identifier = self._session.add_bus(calculation_rate=calculation_rate)
        return BusProxy(
            calculation_rate=calculation_rate, identifier=identifier, provider=self
        )

    def add_bus_group(
        self, channel_count=1, calculation_rate=CalculationRate.CONTROL
    ) -> BusGroupProxy:
        if not self.moment:
            raise ValueError("No current moment")
        calculation_rate = CalculationRate.from_expr(calculation_rate)
        if calculation_rate not in (CalculationRate.AUDIO, CalculationRate.CONTROL):
            raise ValueError(f"Invalid calculation rate: {calculation_rate!r}")
        if channel_count < 1:
            raise ValueError("Channel-count must be positive, non-zero integer")
        identifier = self._session.add_bus_group(
            bus_count=channel_count, calculation_rate=calculation_rate
        )
        return BusGroupProxy(
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            identifier=identifier,
            provider=self,
        )

    def add_group(
        self,
        *,
        target_node=None,
        add_action=AddAction.ADD_TO_HEAD,
        name: Optional[str] = None,
    ) -> GroupProxy:
        if not self.moment:
            raise ValueError("No current moment")
        identifier = self._resolve_target_node(target_node).add_group(
            add_action=add_action
        )
        proxy = GroupProxy(identifier=identifier, provider=self)
        return proxy

    def add_synth(
        self,
        *,
        synthdef: SynthDef = None,
        target_node=None,
        add_action=AddAction.ADD_TO_HEAD,
        name: Optional[str] = None,
        **settings,
    ) -> SynthProxy:
        if not self.moment:
            raise ValueError("No current moment")
        sanitized_settings = {}
        for key, value in settings.items():
            if isinstance(value, (BusProxy, BusGroupProxy)):
                value = value.identifier
            sanitized_settings[key] = value
        identifier = self._resolve_target_node(target_node).add_synth(
            add_action=add_action, synthdef=synthdef, **sanitized_settings
        )
        proxy = SynthProxy(
            identifier=identifier,
            provider=self,
            synthdef=synthdef or default,
            settings=settings,
        )
        return proxy

    def free_buffer(self, buffer_: BufferProxy) -> None:
        if not self.moment:
            raise ValueError("No current moment")
        return  # This is currently a no-op

    def dispose(self, node_proxy: NodeProxy) -> None:
        if not self.moment:
            raise ValueError("No current moment")
        return  # This is currently a no-op

    def free_bus(self, bus: BusProxy) -> None:
        if not self.moment:
            raise ValueError("No current moment")
        return  # This is currently a no-op

    def free_bus_group(self, bus_group: BusGroupProxy) -> None:
        if not self.moment:
            raise ValueError("No current moment")
        return  # This is currently a no-op

    def free_node(self, node_proxy: NodeProxy) -> None:
        if not self.moment:
            raise ValueError("No current moment")
        cast(nonrealtime.Node, node_proxy.identifier).free()

    def move_node(
        self,
        node_proxy: NodeProxy,
        add_action: AddActionLike,
        target_node: Union[NodeProxy, nonrealtime.Node],
    ) -> None:
        if not self.moment:
            raise ValueError("No current moment")
        self._resolve_target_node(target_node).move_node(
            node_proxy.identifier, add_action=add_action
        )

    def set_bus(self, bus_proxy: BusProxy, value: float) -> None:
        if not self.moment:
            raise ValueError("No current moment")
        elif bus_proxy.calculation_rate != CalculationRate.CONTROL:
            raise ValueError("Can only set control-rate buses")
        cast(nonrealtime.Bus, bus_proxy.identifier).set_(value)

    def set_node(self, node_proxy: NodeProxy, **settings) -> None:
        if not self.moment:
            raise ValueError("No current moment")
        for key, value in settings.items():
            if isinstance(value, (BusProxy, BusGroupProxy)):
                value = value.identifier
            cast(nonrealtime.Node, node_proxy.identifier)[key] = value

    def register_osc_callback(
        self, pattern: Tuple[Union[str, float], ...], procedure: Callable
    ) -> OscCallbackProxy:
        return OscCallbackProxy(provider=self, identifier=None)

    def unregister_osc_callback(self, proxy: OscCallbackProxy) -> None:
        pass  # no-op

    @property
    def session(self) -> Optional[Session]:
        return self._session


class RealtimeProvider(Provider):

    ### INITIALIZER ###

    def __init__(self, server: BaseServer, latency: float = 0.1):
        if not isinstance(server, BaseServer):
            raise ValueError(f"Expected Server, got {server}")
        Provider.__init__(self, latency=latency)
        self._server = server

    ### SPECIAL METHODS ###

    def __str__(self) -> str:
        return f"<{type(self).__name__} {self._server!r}>"

    ### PRIVATE METHODS ###

    def _resolve_target_node(self, target_node):
        if target_node is None:
            # TODO: Will this work with AsyncServer?
            target_node = self._server.default_group
        return target_node

    ### PUBLIC METHODS ###

    def add_buffer(
        self,
        *,
        channel_count: Optional[int] = None,
        file_path: Optional[os.PathLike] = None,
        frame_count: Optional[int] = None,
        starting_frame: Optional[int] = None,
    ) -> BufferProxy:
        if not self.moment:
            raise ValueError("No current moment")
        identifier = self._server.buffer_allocator.allocate(1)
        proxy = BufferProxy(
            channel_count=channel_count,
            file_path=file_path,
            frame_count=frame_count,
            identifier=identifier,
            provider=self,
            starting_frame=starting_frame,
        )
        self.moment.buffer_additions.append(proxy)
        return proxy

    def add_bus(self, calculation_rate=CalculationRate.CONTROL) -> BusProxy:
        if not self.moment:
            raise ValueError("No current moment")
        calculation_rate = CalculationRate.from_expr(calculation_rate)
        if calculation_rate not in (CalculationRate.AUDIO, CalculationRate.CONTROL):
            raise ValueError(f"Invalid calculation rate: {calculation_rate!r}")
        allocator = realtime.Bus._get_allocator(calculation_rate, server=self._server)
        identifier = allocator.allocate(1)
        return BusProxy(
            calculation_rate=calculation_rate, identifier=identifier, provider=self
        )

    def add_bus_group(
        self, channel_count=1, calculation_rate=CalculationRate.CONTROL
    ) -> BusGroupProxy:
        if not self.moment:
            raise ValueError("No current moment")
        calculation_rate = CalculationRate.from_expr(calculation_rate)
        if calculation_rate not in (CalculationRate.AUDIO, CalculationRate.CONTROL):
            raise ValueError(f"Invalid calculation rate: {calculation_rate!r}")
        if channel_count < 1:
            raise ValueError("Channel-count must be positive, non-zero integer")
        allocator = realtime.Bus._get_allocator(calculation_rate, server=self._server)
        identifier = allocator.allocate(channel_count)
        if identifier is None:
            raise RuntimeError
        return BusGroupProxy(
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            identifier=identifier,
            provider=self,
        )

    def add_group(
        self,
        *,
        target_node=None,
        add_action=AddAction.ADD_TO_HEAD,
        name: Optional[str] = None,
    ) -> GroupProxy:
        if not self.moment:
            raise ValueError("No current moment")
        target_node = self._resolve_target_node(target_node)
        identifier = self._server.node_id_allocator.allocate_node_id(1)
        proxy = GroupProxy(identifier=identifier, provider=self)
        self.moment.node_additions.append((proxy, add_action, target_node))
        if name:
            self._annotation_map[identifier] = name
        return proxy

    def add_synth(
        self,
        *,
        synthdef: SynthDef = None,
        target_node=None,
        add_action=AddAction.ADD_TO_HEAD,
        name: Optional[str] = None,
        **settings,
    ) -> SynthProxy:
        if not self.moment:
            raise ValueError("No current moment")
        target_node = self._resolve_target_node(target_node)
        identifier = self._server.node_id_allocator.allocate_node_id(1)
        proxy = SynthProxy(
            identifier=identifier,
            provider=self,
            synthdef=synthdef or default,
            settings=settings,
        )
        self.moment.node_additions.append((proxy, add_action, target_node))
        if name:
            self._annotation_map[identifier] = name
        return proxy

    def dispose(self, node_proxy: NodeProxy) -> None:
        if not self.moment:
            raise ValueError("No current moment")
        return  # This is currently a no-op

    def free_buffer(self, buffer_: BufferProxy) -> None:
        if not self.moment:
            raise ValueError("No current moment")
        self._server.buffer_allocator.free(cast(int, buffer_.identifier))
        self.moment.buffer_removals.append(buffer_)

    def free_bus(self, bus_proxy: BusProxy) -> None:
        if not self.moment:
            raise ValueError("No current moment")
        allocator = realtime.Bus._get_allocator(
            bus_proxy.calculation_rate, server=self._server
        )
        allocator.free(cast(int, bus_proxy.identifier))

    def free_bus_group(self, bus_group_proxy: BusGroupProxy) -> None:
        if not self.moment:
            raise ValueError("No current moment")
        allocator = realtime.Bus._get_allocator(
            bus_group_proxy.calculation_rate, server=self._server
        )
        allocator.free(cast(int, bus_group_proxy.identifier))

    def free_node(self, node_proxy: NodeProxy) -> None:
        if not self.moment:
            raise ValueError("No current moment")
        self.moment.node_removals.append(node_proxy)
        self._annotation_map.pop(node_proxy.identifier, None)

    def move_node(
        self, node_proxy: NodeProxy, add_action: AddActionLike, target_node: NodeProxy
    ) -> None:
        if not self.moment:
            raise ValueError("No current moment")
        target_node = self._resolve_target_node(target_node)
        self.moment.node_reorderings.append(
            (node_proxy, AddAction.from_expr(add_action), target_node)
        )

    def set_bus(self, bus_proxy: BusProxy, value: float) -> None:
        if not self.moment:
            raise ValueError("No current moment")
        elif bus_proxy.calculation_rate != CalculationRate.CONTROL:
            raise ValueError("Can only set control-rate buses")
        self.moment.bus_settings.append((bus_proxy, value))

    def set_node(self, node_proxy: NodeProxy, **settings) -> None:
        if not self.moment:
            raise ValueError("No current moment")
        self.moment.node_settings.append((node_proxy, settings))

    def register_osc_callback(
        self, pattern: Tuple[Union[str, float], ...], procedure: Callable
    ) -> OscCallbackProxy:
        identifier = self._server.osc_protocol.register(
            pattern=pattern, procedure=procedure
        )
        return OscCallbackProxy(provider=self, identifier=identifier)

    def unregister_osc_callback(self, proxy: OscCallbackProxy) -> None:
        self._server.osc_protocol.unregister(proxy.identifier)

    @property
    def server(self) -> Optional[BaseServer]:
        return self._server
