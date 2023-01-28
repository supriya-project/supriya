import abc
import collections
import contextlib
import dataclasses
import itertools
import logging
import os
from types import MappingProxyType
from typing import (
    Any,
    Callable,
    Counter,
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

import supriya.nonrealtime  # noqa
import supriya.realtime  # noqa
from supriya import commands, nonrealtime, realtime
from supriya.assets.synthdefs.default import default
from supriya.enums import AddAction, CalculationRate, ParameterRate
from supriya.nonrealtime import Session
from supriya.realtime import AsyncServer, BaseServer, Server
from supriya.scsynth import Options
from supriya.synthdefs import SynthDef
from supriya.typing import (
    AddActionLike,
    CalculationRateLike,
    HeaderFormatLike,
    SampleFormatLike,
)

from .commands import (
    BufferAllocateReadChannelRequest,
    BufferAllocateReadRequest,
    BufferAllocateRequest,
    BufferCloseRequest,
    BufferFreeRequest,
    BufferReadChannelRequest,
    BufferReadRequest,
    BufferWriteRequest,
    BufferZeroRequest,
    ControlBusSetRequest,
    GroupHeadRequest,
    GroupNewRequest,
    GroupTailRequest,
    NodeAfterRequest,
    NodeBeforeRequest,
    NodeFreeRequest,
    NodeSetRequest,
    ParallelGroupNewRequest,
    Request,
    RequestBundle,
    SynthDefReceiveRequest,
    SynthNewRequest,
)

logger = logging.getLogger(__name__)


def _process_requests(
    pairs: List[Tuple[Request, Optional["Completion"]]]
) -> List[Request]:
    requests: List[Request] = []
    for key, group in itertools.groupby(
        [
            request if completion is None else completion(request)
            for request, completion in pairs
        ],
        key=lambda x: type(x),
    ):
        requests.extend(key.merge(list(group)))
    return requests


@dataclasses.dataclass(frozen=True)
class Proxy:
    provider: "Provider"


@dataclasses.dataclass(frozen=True)
class BufferProxy(Proxy):
    provider: "Provider"
    identifier: int
    completion: "Completion"
    channel_count: Optional[int] = None
    channel_indices: Optional[List[int]] = None
    frame_count: Optional[int] = None
    file_path: Optional[os.PathLike] = None
    starting_frame: Optional[int] = None

    def __float__(self) -> float:
        return float(self.identifier)

    def __int__(self) -> int:
        return self.identifier

    def close(self) -> "Completion":
        return self.provider.close_buffer(self)

    def free(self) -> "Completion":
        return self.provider.free_buffer(self)

    def normalize(self, new_maximum: float = 1.0) -> None:
        self.provider.normalize_buffer(self, new_maximum=new_maximum)

    def read(
        self,
        file_path: os.PathLike,
        *,
        buffer_starting_frame: Optional[int] = None,
        channel_indices: Optional[List[int]] = None,
        frame_count: Optional[int] = None,
        leave_open: bool = False,
        starting_frame: Optional[int] = None,
    ) -> "Completion":
        return self.provider.read_buffer(
            self,
            buffer_starting_frame=buffer_starting_frame,
            channel_indices=channel_indices,
            file_path=file_path,
            frame_count=frame_count,
            leave_open=leave_open,
            starting_frame=starting_frame,
        )

    def write(
        self,
        file_path: os.PathLike,
        *,
        buffer_starting_frame: Optional[int] = None,
        frame_count: Optional[int] = None,
        header_format: HeaderFormatLike = "aiff",
        leave_open: bool = False,
        sample_format: SampleFormatLike = "int24",
        starting_frame: Optional[int] = None,
    ) -> "Completion":
        return self.provider.write_buffer(
            self,
            file_path=file_path,
            frame_count=frame_count,
            header_format=header_format,
            leave_open=leave_open,
            sample_format=sample_format,
            starting_frame=starting_frame,
        )

    def zero(self) -> "Completion":
        return self.provider.zero_buffer(self)


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
    identifier: int

    def __float__(self) -> float:
        return float(self.identifier)

    def __int__(self) -> int:
        return self.identifier

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
    identifier: int
    provider: "Provider"
    buses: Sequence["BusProxy"] = dataclasses.field(init=False)

    def __post_init__(self):
        object.__setattr__(
            self,
            "buses",
            tuple(
                BusProxy(
                    calculation_rate=self.calculation_rate,
                    provider=self.provider,
                    identifier=bus_identifier,
                )
                for bus_identifier in range(
                    self.identifier, self.identifier + self.channel_count
                )
            ),
        )

    def __float__(self) -> float:
        return float(self.identifier)

    def __getitem__(self, item) -> BusProxy:
        return self.buses[item]

    def __int__(self) -> int:
        return self.identifier

    def __len__(self) -> int:
        return self.channel_count

    def free(self) -> None:
        self.provider.free_bus_group(self)

    @property
    def map_symbol(self) -> str:
        return self[0].map_symbol


@dataclasses.dataclass(frozen=True)
class NodeProxy(Proxy):
    identifier: int
    provider: "Provider"

    def __float__(self) -> float:
        return float(self.identifier)

    def __int__(self) -> int:
        return self.identifier

    def __setitem__(self, key, value) -> None:
        self.provider.set_node(self, **{key: value})

    def add_group(
        self,
        *,
        add_action: AddActionLike = AddAction.ADD_TO_HEAD,
        name: Optional[str] = None,
        parallel: bool = False,
    ) -> "GroupProxy":
        return self.provider.add_group(
            add_action=add_action, target_node=self, parallel=parallel
        )

    def add_synth(
        self,
        *,
        add_action: AddActionLike = AddAction.ADD_TO_HEAD,
        name: Optional[str] = None,
        synthdef: Optional[SynthDef] = None,
        **settings,
    ) -> "SynthProxy":
        return self.provider.add_synth(
            add_action=add_action, synthdef=synthdef, target_node=self, **settings
        )

    def free(self) -> None:
        self.provider.free_node(self)

    def move(self, add_action: AddActionLike, target_node: "NodeProxy") -> None:
        self.provider.move_node(self, add_action, target_node)


@dataclasses.dataclass(frozen=True)
class GroupProxy(NodeProxy):
    identifier: int
    provider: "Provider"
    parallel: bool = False


@dataclasses.dataclass(frozen=True)
class SynthProxy(NodeProxy):
    identifier: int
    provider: "Provider"
    synthdef: SynthDef
    settings: Dict[str, Union[float, str, BusProxy, BusGroupProxy]]


@dataclasses.dataclass(frozen=True)
class ProviderMoment:
    provider: "Provider"
    seconds: float
    requests: List[Tuple[Request, Optional["Completion"]]] = dataclasses.field(
        default_factory=list
    )
    exit_stack: contextlib.ExitStack = dataclasses.field(
        init=False, default_factory=contextlib.ExitStack, compare=False
    )

    async def __aenter__(self):
        self._enter()
        return self

    async def __aexit__(self, *args):
        request_bundle = self._exit()
        if self.provider.server is not None and request_bundle:
            self.provider.server.send(request_bundle.to_osc())

    def __enter__(self):
        self._enter()
        return self

    def __exit__(self, *args):
        request_bundle = self._exit()
        if self.provider.server is not None and request_bundle:
            self.provider.server.send(request_bundle.to_osc())

    def _enter(self):
        self.provider._moments.append(self)
        if self.provider.session is not None:
            self.exit_stack.enter_context(self.provider.session.at(self.seconds))

    def _exit(self) -> Optional[RequestBundle]:
        self.provider._moments.pop()
        if self.provider.session is not None:
            self.exit_stack.close()
            return None
        timestamp = (
            self.seconds + self.provider._latency if self.seconds is not None else None
        )
        requests = _process_requests(self.requests)
        if not requests:
            return None
        request_bundle = RequestBundle(contents=requests, timestamp=timestamp)
        return request_bundle


@dataclasses.dataclass
class Completion:
    provider: "Provider"
    requests: List[Tuple[Request, Optional["Completion"]]] = dataclasses.field(
        default_factory=list
    )

    def __enter__(self) -> None:
        self.provider._completions.append(self)

    def __exit__(self, *args) -> None:
        self.provider._completions.pop()

    def __call__(self, request: Request) -> Request:
        if not hasattr(request, "callback"):
            raise ValueError(request)
        requests = _process_requests(self.requests)
        if len(requests) > 1:
            request.callback = RequestBundle(contents=requests)
        elif len(requests) == 1:
            request.callback = requests[0]
        return request


class Provider(metaclass=abc.ABCMeta):
    """
    Provides limited realtime/non-realtime compatibility layer.
    """

    ### INITIALIZER ###

    def __init__(self, latency=0.1) -> None:
        self._moments: List[ProviderMoment] = []
        self._completions: List[Completion] = []
        self._counter: Counter[float] = collections.Counter()
        self._latency: float = latency
        self._annotation_map: Dict[Union["supriya.nonrealtime.Node", int], str] = {}

    ### PRIVATE METHODS ###

    def _add_request(
        self, request: commands.Request, completion: Optional[Completion] = None
    ) -> None:
        if not self._moments:
            raise ValueError
        requests = self._moments[-1].requests
        if self._completions:
            requests = self._completions[-1].requests
        requests.append((request, completion))

    def _allocate_id(
        self,
        proxy_type: Type[Proxy],
        calculation_rate: Optional[CalculationRate] = None,
        count: int = 1,
    ) -> int:
        context = self.server or self.session
        if not context:
            raise ValueError
        if proxy_type is NodeProxy:
            return context._node_id_allocator.allocate_node_id()
        if proxy_type is BufferProxy:
            return context._buffer_allocator.allocate(count)
        if proxy_type is BusProxy:
            if calculation_rate is CalculationRate.AUDIO:
                return context._audio_bus_allocator.allocate(count)
            elif calculation_rate is CalculationRate.CONTROL:
                return context._control_bus_allocator.allocate(count)
        raise ValueError

    def _free_id(
        self,
        proxy_type: Type[Proxy],
        id_: int,
        calculation_rate: Optional[CalculationRate] = None,
    ) -> None:
        if self.session:
            return None
        if not self.server:
            raise ValueError
        if proxy_type is NodeProxy:
            return None
        if proxy_type is BufferProxy:
            self.server._buffer_allocator.free(id_)
            return None
        if proxy_type is BusProxy:
            if calculation_rate is CalculationRate.AUDIO:
                self.server._audio_bus_allocator.free(id_)
                return None
            elif calculation_rate is CalculationRate.CONTROL:
                self.server._control_bus_allocator.free(id_)
                return None
        raise ValueError

    def _resolve_target_node_id(
        self, target: Union[None, NodeProxy, int, nonrealtime.Node, realtime.Node]
    ) -> int:
        if isinstance(target, int):
            return target
        elif isinstance(target, NodeProxy):
            return target.identifier
        elif self.session:
            if target is None:
                return 0
            elif isinstance(target, nonrealtime.Node):
                return int(target)
        elif self.server:
            if target is None:
                return self.server.client_id + 1
            elif isinstance(target, realtime.Node):
                return int(target)
        raise ValueError(target)

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def add_buffer(
        self,
        *,
        channel_count: Optional[int] = None,
        channel_indices: Optional[List[int]] = None,
        file_path: Optional[os.PathLike] = None,
        frame_count: Optional[int] = None,
        starting_frame: Optional[int] = None,
    ) -> BufferProxy:
        if not self.moment:
            raise ValueError("No current moment")
        if not (frame_count or file_path):
            raise ValueError
        if channel_count and channel_indices:
            raise ValueError
        id_ = self._allocate_id(BufferProxy)
        completion = Completion(provider=self)
        if file_path and channel_indices:
            self._add_request(
                BufferAllocateReadChannelRequest(
                    buffer_id=id_,
                    channel_indices=channel_indices,
                    file_path=file_path,
                    frame_count=frame_count,
                    starting_frame=starting_frame,
                ),
                completion,
            )
        elif file_path:
            self._add_request(
                BufferAllocateReadRequest(
                    buffer_id=id_,
                    file_path=file_path,
                    frame_count=frame_count,
                    starting_frame=starting_frame,
                ),
                completion,
            )
        else:
            self._add_request(
                BufferAllocateRequest(
                    buffer_id=id_, channel_count=channel_count, frame_count=frame_count
                ),
                completion,
            )
        proxy = BufferProxy(
            channel_count=channel_count,
            channel_indices=channel_indices,
            completion=completion,
            file_path=file_path,
            frame_count=frame_count,
            identifier=id_,
            provider=self,
            starting_frame=starting_frame,
        )
        return proxy

    @abc.abstractmethod
    def add_bus(
        self, calculation_rate: CalculationRateLike = CalculationRate.CONTROL
    ) -> BusProxy:
        if not self.moment:
            raise ValueError("No current moment")
        rate = CalculationRate.from_expr(calculation_rate)
        if rate not in (CalculationRate.AUDIO, CalculationRate.CONTROL):
            raise ValueError(f"Invalid calculation rate: {rate!r}")
        id_ = self._allocate_id(BusProxy, calculation_rate=rate)
        return BusProxy(calculation_rate=rate, identifier=id_, provider=self)

    @abc.abstractmethod
    def add_bus_group(
        self,
        channel_count=1,
        calculation_rate: CalculationRateLike = CalculationRate.CONTROL,
    ) -> BusGroupProxy:
        if not self.moment:
            raise ValueError("No current moment")
        rate = CalculationRate.from_expr(calculation_rate)
        if rate not in (CalculationRate.AUDIO, CalculationRate.CONTROL):
            raise ValueError(f"Invalid calculation rate: {rate!r}")
        if channel_count < 1:
            raise ValueError("Channel-count must be positive, non-zero integer")
        id_ = self._allocate_id(BusProxy, calculation_rate=rate, count=channel_count)
        return BusGroupProxy(
            calculation_rate=rate,
            channel_count=channel_count,
            identifier=id_,
            provider=self,
        )

    @abc.abstractmethod
    def add_group(
        self,
        *,
        add_action: AddActionLike = AddAction.ADD_TO_HEAD,
        name: Optional[str] = None,
        parallel: bool = False,
        target_node: Optional[Union[NodeProxy, int]] = None,
    ) -> GroupProxy:
        if not self.moment:
            raise ValueError("No current moment")
        target_node_id = self._resolve_target_node_id(target_node)
        add_action_ = AddAction.from_expr(add_action)
        id_ = self._allocate_id(NodeProxy)
        if name:
            self._annotation_map[id_] = name
        proxy = GroupProxy(identifier=id_, provider=self, parallel=parallel)
        kwargs = dict(
            add_action=add_action_, node_id=id_, target_node_id=target_node_id
        )
        if parallel:
            self._add_request(
                ParallelGroupNewRequest(items=[GroupNewRequest.Item(**kwargs)])
            )
        else:
            self._add_request(GroupNewRequest(items=[GroupNewRequest.Item(**kwargs)]))
        return proxy

    @abc.abstractmethod
    def add_synth(
        self,
        *,
        add_action: AddActionLike = AddAction.ADD_TO_HEAD,
        name: Optional[str] = None,
        synthdef: Optional[SynthDef] = None,
        target_node: Optional[Union[NodeProxy, int]] = None,
        **settings,
    ) -> SynthProxy:
        if not self.moment:
            raise ValueError("No current moment")
        target_node_id = self._resolve_target_node_id(target_node)
        add_action_ = AddAction.from_expr(add_action)
        id_ = self._allocate_id(NodeProxy)
        if name:
            self._annotation_map[id_] = name
        synthdef = synthdef or default
        synthdef_kwargs: Dict[str, Union[float, str, BusProxy, BusGroupProxy]] = {}
        for _, parameter in synthdef.indexed_parameters:
            if parameter.name not in settings:
                continue
            value = settings[parameter.name]
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
        proxy = SynthProxy(
            identifier=id_, provider=self, synthdef=synthdef, settings=synthdef_kwargs
        )
        self._add_request(
            SynthNewRequest(
                add_action=add_action_,
                node_id=id_,
                synthdef=synthdef,
                target_node_id=target_node_id,
                **synthdef_kwargs,
            )
        )
        return proxy

    @abc.abstractmethod
    def add_synthdefs(self, *synthdefs: SynthDef) -> Completion:
        if not self.moment:
            raise ValueError("No current moment")
        completion = Completion(self)
        self._add_request(SynthDefReceiveRequest(*synthdefs), completion)
        return completion

    def at(self, seconds=None) -> ProviderMoment:
        return ProviderMoment(provider=self, seconds=seconds)

    @abc.abstractmethod
    def close_buffer(self, buffer_proxy: BufferProxy) -> Completion:
        if not self.moment:
            raise ValueError("No current moment")
        request = BufferCloseRequest(buffer_id=buffer_proxy.identifier)
        completion = Completion(provider=self)
        self._add_request(request, completion)
        return completion

    @abc.abstractmethod
    def free_buffer(self, buffer_proxy) -> Completion:
        if not self.moment:
            raise ValueError("No current moment")
        self._free_id(BufferProxy, buffer_proxy.identifier)
        request = BufferFreeRequest(buffer_id=buffer_proxy.identifier)
        completion = Completion(provider=self)
        self._add_request(request, completion)
        return completion

    @abc.abstractmethod
    def free_bus(self, bus_proxy: BusProxy) -> None:
        if not self.moment:
            raise ValueError("No current moment")
        self._free_id(
            BusProxy, bus_proxy.identifier, calculation_rate=bus_proxy.calculation_rate
        )
        return None

    @abc.abstractmethod
    def free_bus_group(self, bus_group_proxy: BusGroupProxy) -> None:
        if not self.moment:
            raise ValueError("No current moment")
        self._free_id(
            BusProxy,
            bus_group_proxy.identifier,
            calculation_rate=bus_group_proxy.calculation_rate,
        )
        return None

    @abc.abstractmethod
    def free_node(self, node_proxy: NodeProxy) -> None:
        # TODO: Create a NodeReleaseRequest class
        #       ... which formats to either `/n_set ID gate 0` or `/n_free ID`
        #       ... and teach Session to recognize it
        if not self.moment:
            raise ValueError("No current moment")
        self._annotation_map.pop(node_proxy.identifier, None)
        self._free_id(NodeProxy, node_proxy.identifier)
        if (
            isinstance(node_proxy, SynthProxy)
            and "gate" in node_proxy.synthdef.parameters
        ):
            # TODO: How to signal to NRT that this is a free?
            self._add_request(NodeSetRequest(node_id=node_proxy.identifier, gate=0))
        else:
            self._add_request(NodeFreeRequest(node_ids=[node_proxy.identifier]))
        return None

    @classmethod
    def from_context(cls, context, latency=0.1) -> "Provider":
        if isinstance(context, Session):
            return NonrealtimeProvider(context, latency=latency)
        elif isinstance(context, BaseServer):
            return RealtimeProvider(context, latency=latency)
        raise ValueError("Unknown context")

    @abc.abstractmethod
    def move_node(
        self, node_proxy: NodeProxy, add_action: AddActionLike, target_node: NodeProxy
    ) -> None:
        if not self.moment:
            raise ValueError("No current moment")
        target_node_id = self._resolve_target_node_id(target_node)
        add_action_ = AddAction.from_expr(add_action)
        pairs = [[int(node_proxy), target_node_id]]
        if add_action_ is AddAction.ADD_AFTER:
            self._add_request(NodeAfterRequest(pairs))
        elif add_action_ is AddAction.ADD_BEFORE:
            self._add_request(NodeBeforeRequest(pairs))
        elif add_action_ is AddAction.ADD_TO_HEAD:
            self._add_request(GroupHeadRequest(pairs))
        elif add_action_ is AddAction.ADD_TO_TAIL:
            self._add_request(GroupTailRequest(pairs))
        else:
            raise ValueError
        return None

    @classmethod
    def nonrealtime(cls) -> "NonrealtimeProvider":
        session = Session()
        return cast("NonrealtimeProvider", cls.from_context(session))

    @abc.abstractmethod
    def normalize_buffer(
        self, buffer_proxy: BufferProxy, new_maximum: float = 1.0
    ) -> None:
        if not self.moment:
            raise ValueError("No current moment")
        request = commands.BufferNormalizeRequest(
            buffer_id=buffer_proxy.identifier, new_maximum=new_maximum
        )
        self._add_request(request)
        return None

    @abc.abstractmethod
    def read_buffer(
        self,
        buffer_proxy: BufferProxy,
        file_path: os.PathLike,
        *,
        buffer_starting_frame: Optional[int] = None,
        channel_indices: Optional[List[int]] = None,
        frame_count: Optional[int] = None,
        leave_open: bool = False,
        starting_frame: Optional[int] = None,
    ) -> Completion:
        if not self.moment:
            raise ValueError("No current moment")
        kwargs = dict(
            buffer_id=buffer_proxy.identifier,
            file_path=file_path,
            frame_count=frame_count,
            leave_open=leave_open,
            starting_frame_in_buffer=buffer_starting_frame,
            starting_frame_in_file=starting_frame,
        )
        if channel_indices:
            request: commands.Request = BufferReadChannelRequest(
                **kwargs, channel_indices=channel_indices
            )
        else:
            request = BufferReadRequest(**kwargs)
        completion = Completion(provider=self)
        self._add_request(request, completion)
        return completion

    @classmethod
    def realtime(
        cls, *, options: Optional[Options] = None, **kwargs
    ) -> "RealtimeProvider":
        server = Server()
        server.boot(options=options, **kwargs)
        return cast("RealtimeProvider", cls.from_context(server))

    @classmethod
    async def realtime_async(
        cls, *, options: Optional[Options] = None, **kwargs
    ) -> "RealtimeProvider":
        server = AsyncServer()
        await server.boot(options=options, **kwargs)
        return cast("RealtimeProvider", cls.from_context(server))

    @abc.abstractmethod
    def register_osc_callback(
        self, pattern: Tuple[Union[str, float], ...], procedure: Callable
    ) -> OscCallbackProxy:
        raise NotImplementedError

    @abc.abstractmethod
    def set_bus(self, bus_proxy: BusProxy, value: float) -> None:
        if not self.moment:
            raise ValueError("No current moment")
        if bus_proxy.calculation_rate != CalculationRate.CONTROL:
            raise ValueError("Can only set control-rate buses")
        self._add_request(
            ControlBusSetRequest(index_value_pairs=[[int(bus_proxy), value]])
        )
        return None

    @abc.abstractmethod
    def set_node(self, node_proxy: NodeProxy, **settings) -> None:
        if not self.moment:
            raise ValueError("No current moment")
        coerced_settings: Dict[str, Union[float, str]] = {}
        for key, value in settings.items():
            if isinstance(value, (BusProxy, BusGroupProxy)):
                coerced_settings[key] = value.map_symbol
            else:
                coerced_settings[key] = float(value)
        self._add_request(NodeSetRequest(node_id=int(node_proxy), **coerced_settings))
        return None

    @abc.abstractmethod
    def unregister_osc_callback(self, proxy: OscCallbackProxy) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def write_buffer(
        self,
        buffer_proxy: BufferProxy,
        file_path: os.PathLike,
        *,
        frame_count: Optional[int] = None,
        header_format: HeaderFormatLike = "aiff",
        leave_open: bool = False,
        sample_format: SampleFormatLike = "int24",
        starting_frame: Optional[int] = None,
    ) -> Completion:
        if not self.moment:
            raise ValueError("No current moment")
        request = BufferWriteRequest(
            buffer_id=buffer_proxy.identifier,
            file_path=file_path,
            frame_count=frame_count,
            header_format=header_format,
            leave_open=leave_open,
            sample_format=sample_format,
            starting_frame=starting_frame,
        )
        completion = Completion(provider=self)
        self._add_request(request, completion)
        return completion

    @abc.abstractmethod
    def zero_buffer(self, buffer_proxy: BufferProxy):
        if not self.moment:
            raise ValueError("No current moment")
        request = BufferZeroRequest(buffer_id=buffer_proxy.identifier)
        completion = Completion(provider=self)
        self._add_request(request, completion)
        return completion

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

    def _resolve_target_node(
        self, target_node: Union[None, int, NodeProxy, nonrealtime.Node]
    ) -> nonrealtime.Node:
        if target_node is None:
            return self._session.root_node
        elif isinstance(target_node, NodeProxy):
            return self._session.nodes_by_session_id[target_node.identifier]
        elif isinstance(target_node, int):
            return self._session.nodes_by_session_id[target_node]
        return target_node

    ### PUBLIC METHODS ###

    def add_buffer(
        self,
        *,
        channel_count: Optional[int] = None,
        channel_indices: Optional[List[int]] = None,
        file_path: Optional[os.PathLike] = None,
        frame_count: Optional[int] = None,
        starting_frame: Optional[int] = None,
    ) -> BufferProxy:
        if not self.moment:
            raise ValueError("No current moment")
        buffer_ = self._session.add_buffer(
            channel_count=channel_count,
            channel_indices=channel_indices,
            file_path=file_path,
            frame_count=frame_count,
            starting_frame=starting_frame,
        )
        return BufferProxy(
            channel_count=channel_count,
            channel_indices=channel_indices,
            completion=Completion(self),
            file_path=file_path,
            frame_count=frame_count,
            identifier=buffer_.session_id,
            provider=self,
            starting_frame=starting_frame,
        )

    def add_bus(
        self, calculation_rate: CalculationRateLike = CalculationRate.CONTROL
    ) -> BusProxy:
        if not self.moment:
            raise ValueError("No current moment")
        rate = CalculationRate.from_expr(calculation_rate)
        if rate not in (CalculationRate.AUDIO, CalculationRate.CONTROL):
            raise ValueError(f"Invalid calculation rate: {rate!r}")
        return BusProxy(
            calculation_rate=rate,
            identifier=self._session.add_bus(
                calculation_rate=calculation_rate
            ).session_id,
            provider=self,
        )

    def add_bus_group(
        self,
        channel_count=1,
        calculation_rate: CalculationRateLike = CalculationRate.CONTROL,
    ) -> BusGroupProxy:
        if not self.moment:
            raise ValueError("No current moment")
        rate = CalculationRate.from_expr(calculation_rate)
        if rate not in (CalculationRate.AUDIO, CalculationRate.CONTROL):
            raise ValueError(f"Invalid calculation rate: {rate!r}")
        if channel_count < 1:
            raise ValueError("Channel-count must be positive, non-zero integer")
        return BusGroupProxy(
            calculation_rate=rate,
            channel_count=channel_count,
            identifier=self._session.add_bus_group(
                bus_count=channel_count, calculation_rate=calculation_rate
            ).session_id,
            provider=self,
        )

    def add_group(
        self,
        *,
        target_node=None,
        add_action=AddAction.ADD_TO_HEAD,
        name: Optional[str] = None,
        parallel: bool = False,
    ) -> GroupProxy:
        if not self.moment:
            raise ValueError("No current moment")
        proxy = GroupProxy(
            identifier=self._resolve_target_node(target_node)
            .add_group(add_action=add_action)
            .session_id,
            provider=self,
            parallel=parallel,
        )
        return proxy

    def add_synth(
        self,
        *,
        synthdef: Optional[SynthDef] = None,
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
                sanitized_settings[key] = self._session.get_object_by_session_id(
                    type_=nonrealtime.Bus,
                    session_id=value.identifier,
                    calculation_rate=value.calculation_rate,
                )
            else:
                sanitized_settings[key] = value
        synth = self._resolve_target_node(target_node).add_synth(
            add_action=add_action, synthdef=synthdef, **sanitized_settings
        )
        proxy = SynthProxy(
            identifier=synth.session_id,
            provider=self,
            synthdef=synthdef or default,
            settings=settings,
        )
        return proxy

    def add_synthdefs(self, *synthdef: SynthDef) -> Completion:
        if not self.moment:
            raise ValueError("No current moment")
        return Completion(self)

    def close_buffer(self, buffer_proxy: BufferProxy) -> Completion:
        if not self.moment:
            raise ValueError("No current moment")
        self._session.buffers_by_session_id[buffer_proxy.identifier].close()
        return Completion(self)

    def free_buffer(self, buffer_: BufferProxy) -> Completion:
        if not self.moment:
            raise ValueError("No current moment")
        return Completion(self)

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
        self._session.nodes_by_session_id[node_proxy.identifier].free()

    def move_node(
        self,
        node_proxy: NodeProxy,
        add_action: AddActionLike,
        target_node: Union[NodeProxy, nonrealtime.Node],
    ) -> None:
        if not self.moment:
            raise ValueError("No current moment")
        self._resolve_target_node(target_node).move_node(
            self._session.nodes_by_session_id[node_proxy.identifier],
            add_action=add_action,
        )

    def normalize_buffer(
        self, buffer_proxy: BufferProxy, new_maximum: float = 1.0
    ) -> None:
        if not self.moment:
            raise ValueError("No current moment")
        self._session.buffers_by_session_id[buffer_proxy.identifier].normalize(
            new_maximum=new_maximum
        )

    def read_buffer(
        self,
        buffer_proxy: BufferProxy,
        file_path: os.PathLike,
        *,
        buffer_starting_frame: Optional[int] = None,
        channel_indices: Optional[List[int]] = None,
        frame_count: Optional[int] = None,
        leave_open: bool = False,
        starting_frame: Optional[int] = None,
    ) -> Completion:
        if not self.moment:
            raise ValueError("No current moment")
        self._session.buffers_by_session_id[buffer_proxy.identifier].read(
            channel_indices=channel_indices,
            file_path=file_path,
            frame_count=frame_count,
            leave_open=leave_open,
            starting_frame_in_buffer=buffer_starting_frame,
            starting_frame_in_file=starting_frame,
        )
        return Completion(self)

    def register_osc_callback(
        self, pattern: Tuple[Union[str, float], ...], procedure: Callable
    ) -> OscCallbackProxy:
        return OscCallbackProxy(provider=self, identifier=None)

    def set_bus(self, bus_proxy: BusProxy, value: float) -> None:
        if not self.moment:
            raise ValueError("No current moment")
        elif bus_proxy.calculation_rate != CalculationRate.CONTROL:
            raise ValueError("Can only set control-rate buses")
        self._session.get_object_by_session_id(
            type_=nonrealtime.Bus,
            session_id=bus_proxy.identifier,
            calculation_rate=bus_proxy.calculation_rate,
        ).set_(value)

    def set_node(self, node_proxy: NodeProxy, **settings) -> None:
        if not self.moment:
            raise ValueError("No current moment")
        node = self._session.nodes_by_session_id[node_proxy.identifier]
        for key, value in settings.items():
            if isinstance(value, (BusProxy, BusGroupProxy)):
                node[key] = self._session.get_object_by_session_id(
                    type_=nonrealtime.Bus,
                    session_id=value.identifier,
                    calculation_rate=value.calculation_rate,
                )
            else:
                node[key] = value

    def unregister_osc_callback(self, proxy: OscCallbackProxy) -> None:
        pass  # no-op

    def write_buffer(
        self,
        buffer_proxy: BufferProxy,
        file_path: os.PathLike,
        *,
        frame_count: Optional[int] = None,
        header_format: HeaderFormatLike = "aiff",
        leave_open: bool = False,
        sample_format: SampleFormatLike = "int24",
        starting_frame: Optional[int] = None,
    ) -> Completion:
        if not self.moment:
            raise ValueError("No current moment")
        self._session.buffers_by_session_id[buffer_proxy.identifier].write(
            file_path=file_path,
            frame_count=frame_count,
            header_format=header_format,
            leave_open=leave_open,
            sample_format=sample_format,
            starting_frame=starting_frame,
        )
        return Completion(self)

    def zero_buffer(self, buffer_proxy: BufferProxy) -> None:
        if not self.moment:
            raise ValueError("No current moment")
        self._session.buffers_by_session_id[buffer_proxy.identifier].zero()

    ### PUBLIC PROPERTIES ###

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
        channel_indices: Optional[List[int]] = None,
        file_path: Optional[os.PathLike] = None,
        frame_count: Optional[int] = None,
        starting_frame: Optional[int] = None,
    ) -> BufferProxy:
        return super().add_buffer(
            channel_count=channel_count,
            channel_indices=channel_indices,
            file_path=file_path,
            frame_count=frame_count,
            starting_frame=starting_frame,
        )

    def add_bus(
        self, calculation_rate: CalculationRateLike = CalculationRate.CONTROL
    ) -> BusProxy:
        return super().add_bus(calculation_rate=calculation_rate)

    def add_bus_group(
        self,
        channel_count=1,
        calculation_rate: CalculationRateLike = CalculationRate.CONTROL,
    ) -> BusGroupProxy:
        return super().add_bus_group(
            calculation_rate=calculation_rate, channel_count=channel_count
        )

    def add_group(
        self,
        *,
        add_action=AddAction.ADD_TO_HEAD,
        name: Optional[str] = None,
        parallel: bool = False,
        target_node=None,
    ) -> GroupProxy:
        return super().add_group(
            add_action=add_action, name=name, parallel=parallel, target_node=target_node
        )

    def add_synth(
        self,
        *,
        add_action=AddAction.ADD_TO_HEAD,
        name: Optional[str] = None,
        synthdef: Optional[SynthDef] = None,
        target_node=None,
        **settings,
    ) -> SynthProxy:
        return super().add_synth(
            synthdef=synthdef,
            target_node=target_node,
            add_action=add_action,
            name=name,
            **settings,
        )

    def add_synthdefs(self, *synthdefs: SynthDef) -> Completion:
        return super().add_synthdefs(*synthdefs)

    def close_buffer(self, buffer_proxy: BufferProxy) -> Completion:
        return super().close_buffer(buffer_proxy)

    def free_buffer(self, buffer_proxy: BufferProxy) -> Completion:
        return super().free_buffer(buffer_proxy)

    def free_bus(self, bus_proxy: BusProxy) -> None:
        return super().free_bus(bus_proxy)

    def free_bus_group(self, bus_group_proxy: BusGroupProxy) -> None:
        return super().free_bus_group(bus_group_proxy)

    def free_node(self, node_proxy: NodeProxy) -> None:
        return super().free_node(node_proxy)

    def move_node(
        self, node_proxy: NodeProxy, add_action: AddActionLike, target_node: NodeProxy
    ) -> None:
        return super().move_node(
            node_proxy=node_proxy, add_action=add_action, target_node=target_node
        )

    def normalize_buffer(
        self, buffer_proxy: BufferProxy, new_maximum: float = 1.0
    ) -> None:
        return super().normalize_buffer(buffer_proxy, new_maximum=new_maximum)

    def read_buffer(
        self,
        buffer_proxy: BufferProxy,
        file_path: os.PathLike,
        *,
        buffer_starting_frame: Optional[int] = None,
        channel_indices: Optional[List[int]] = None,
        frame_count: Optional[int] = None,
        leave_open: bool = False,
        starting_frame: Optional[int] = None,
    ) -> Completion:
        return super().read_buffer(
            buffer_proxy=buffer_proxy,
            file_path=file_path,
            buffer_starting_frame=buffer_starting_frame,
            channel_indices=channel_indices,
            frame_count=frame_count,
            leave_open=leave_open,
            starting_frame=starting_frame,
        )

    def register_osc_callback(
        self, pattern: Tuple[Union[str, float], ...], procedure: Callable
    ) -> OscCallbackProxy:
        identifier = self._server.osc_protocol.register(
            pattern=pattern, procedure=procedure
        )
        return OscCallbackProxy(provider=self, identifier=identifier)

    def set_bus(self, bus_proxy: BusProxy, value: float) -> None:
        return super().set_bus(bus_proxy, value)

    def set_node(self, node_proxy: NodeProxy, **settings) -> None:
        return super().set_node(node_proxy, **settings)

    def unregister_osc_callback(self, proxy: OscCallbackProxy) -> None:
        self._server.osc_protocol.unregister(proxy.identifier)

    def write_buffer(
        self,
        buffer_proxy: BufferProxy,
        file_path: os.PathLike,
        *,
        frame_count: Optional[int] = None,
        header_format: HeaderFormatLike = "aiff",
        leave_open: bool = False,
        sample_format: SampleFormatLike = "int24",
        starting_frame: Optional[int] = None,
    ) -> Completion:
        return super().write_buffer(
            buffer_proxy=buffer_proxy,
            file_path=file_path,
            frame_count=frame_count,
            header_format=header_format,
            leave_open=leave_open,
            sample_format=sample_format,
            starting_frame=starting_frame,
        )

    def zero_buffer(self, buffer_proxy: BufferProxy) -> Completion:
        return super().zero_buffer(buffer_proxy)

    ### PUBLIC PROPERTIES ###

    @property
    def server(self) -> Optional[BaseServer]:
        return self._server
