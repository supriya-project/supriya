import abc
import contextlib
import dataclasses
import itertools
import threading
from os import PathLike
from typing import (
    TYPE_CHECKING,
    Awaitable,
    Callable,
    Container,
    Dict,
    List,
    Optional,
    SupportsFloat,
    SupportsInt,
    Tuple,
    Type,
    Union,
    cast,
)

from uqbar.objects import new

from ..allocators import BlockAllocator, NodeIdAllocator
from ..assets.synthdefs.default import default
from ..commands import (
    BufferAllocateReadChannelRequest,
    BufferAllocateReadRequest,
    BufferAllocateRequest,
    BufferCloseRequest,
    BufferCopyRequest,
    BufferFillRequest,
    BufferFreeRequest,
    BufferInfo,
    BufferNormalizeRequest,
    BufferReadChannelRequest,
    BufferReadRequest,
    BufferWriteRequest,
    BufferZeroRequest,
    ControlBusFillRequest,
    ControlBusSetRequest,
    GroupDeepFreeRequest,
    GroupFreeAllRequest,
    GroupHeadRequest,
    GroupNewRequest,
    GroupTailRequest,
    NodeAfterRequest,
    NodeBeforeRequest,
    NodeInfo,
    NodeMapToAudioBusRequest,
    NodeMapToControlBusRequest,
    NodeOrderRequest,
    NodeReleaseRequest,
    NodeRunRequest,
    NodeSetRequest,
    ParallelGroupNewRequest,
    Request,
    RequestBundle,
    Requestable,
    SynthDefFreeAllRequest,
    SynthDefFreeRequest,
    SynthDefLoadDirectoryRequest,
    SynthDefLoadRequest,
    SynthDefReceiveRequest,
    SynthNewRequest,
)
from ..enums import AddAction, CalculationRate, ParameterRate
from ..scsynth import Options
from ..synthdefs import SynthDef
from ..typing import (
    AddActionLike,
    CalculationRateLike,
    HeaderFormatLike,
    SampleFormatLike,
)

if TYPE_CHECKING:
    from .realtime import RealtimeContext


class ContextError(Exception):
    pass


class InvalidCalculationRate(ContextError):
    pass


class InvalidMoment(ContextError):
    pass


class MomentClosed(ContextError):
    pass


@dataclasses.dataclass
class RequestContext:
    context: "Context"
    requests: List[Tuple[Request, Optional["Completion"]]]


@dataclasses.dataclass
class Moment(RequestContext):
    seconds: Optional[float] = None
    closed: bool = False

    def __enter__(self) -> "Moment":
        if self.closed:
            raise MomentClosed
        self.context._push_moment(self)
        return self

    def __exit__(self, *args) -> None:
        self.context._pop_moment()
        requests = self.context._apply_completions(self.requests)
        timestamp = (
            self.seconds + self.context._latency if self.seconds is not None else None
        )
        if len(requests) > 1 or timestamp is not None:
            self.context.send(RequestBundle(timestamp=timestamp, contents=requests))
        else:
            self.context.send(requests[0])
        self.closed = True


@dataclasses.dataclass
class Completion(RequestContext):
    moment: Moment

    def __enter__(self) -> "Completion":
        if self.moment.closed:
            raise MomentClosed
        self.context._push_completion(self)
        return self

    def __exit__(self, *args) -> None:
        self.context._pop_completion()

    def __call__(self, request: Request) -> Request:
        if not hasattr(request, "callback"):
            raise ValueError(request)
        requests = self.context._apply_completions(self.requests)
        if len(requests) > 1:
            request = new(request, callback=RequestBundle(contents=requests))
        elif len(requests) == 1:
            request = new(request, callback=requests[0])
        return request


@dataclasses.dataclass(frozen=True)
class ContextObject:
    context: "Context"
    id_: int

    def __float__(self) -> float:
        return float(self.id_)

    def __int__(self) -> int:
        return self.id_

    @property
    def allocated(self) -> bool:
        return self in cast("RealtimeContext", self.context)


@dataclasses.dataclass(frozen=True)
class Buffer(ContextObject):
    completion: Optional[Completion] = None

    def __enter__(self) -> Completion:
        if self.completion is None:
            raise InvalidMoment
        return self.completion.__enter__()

    def __exit__(self, *args) -> None:
        if self.completion is None:
            raise InvalidMoment
        return self.completion.__exit__(*args)

    def close(
        self, on_completion: Optional[Callable[["Context"], None]] = None
    ) -> Completion:
        return self.context.close_buffer(self, on_completion=on_completion)

    def copy(
        self,
        *,
        target_buffer: "Buffer",
        starting_frame: int,
        target_starting_frame: int,
        frame_count: int,
    ) -> None:
        self.context.copy_buffer(
            frame_count=frame_count,
            source_buffer=self,
            source_starting_frame=starting_frame,
            target_buffer=target_buffer,
            target_starting_frame=target_starting_frame,
        )

    def fill(self, starting_frame: int, frame_count: int, value: float) -> None:
        self.context.fill_buffer(self, starting_frame, frame_count, value)

    def free(
        self, on_completion: Optional[Callable[["Context"], None]] = None
    ) -> Completion:
        return self.context.free_buffer(self, on_completion=on_completion)

    def normalize(self, new_maximum=1.0) -> None:
        self.context.normalize_buffer(self, new_maximum)

    def query(self) -> Union[Awaitable[BufferInfo], BufferInfo]:
        return cast("RealtimeContext", self.context).query_buffer(self)

    def read(
        self,
        file_path: PathLike,
        *,
        buffer_starting_frame: Optional[int] = None,
        channel_indices: Optional[List[int]] = None,
        frame_count: Optional[int] = None,
        leave_open: bool = False,
        on_completion: Optional[Callable[["Context"], None]] = None,
        starting_frame: Optional[int] = None,
    ) -> Completion:
        return self.context.read_buffer(
            self,
            file_path,
            buffer_starting_frame=buffer_starting_frame,
            channel_indices=channel_indices,
            frame_count=frame_count,
            leave_open=leave_open,
            on_completion=on_completion,
            starting_frame=starting_frame,
        )

    def write(
        self,
        file_path: PathLike,
        *,
        frame_count: Optional[int] = None,
        header_format: HeaderFormatLike = "aiff",
        leave_open: bool = False,
        on_completion: Optional[Callable[["Context"], None]] = None,
        sample_format: SampleFormatLike = "int24",
        starting_frame: Optional[int] = None,
    ) -> Completion:
        return self.context.write_buffer(
            self,
            file_path,
            frame_count=frame_count,
            header_format=header_format,
            leave_open=leave_open,
            on_completion=on_completion,
            sample_format=sample_format,
            starting_frame=starting_frame,
        )

    def zero(
        self, on_completion: Optional[Callable[["Context"], None]] = None
    ) -> Completion:
        return self.context.zero_buffer(self, on_completion=on_completion)


@dataclasses.dataclass(frozen=True)
class Bus(ContextObject):
    calculation_rate: CalculationRate

    def fill(self, count: int, value: float) -> None:
        self.context.fill_buses(self, count, value)

    def free(self) -> None:
        self.context.free_bus(self)

    def get_(self) -> Union[Awaitable[float], float]:
        return cast("RealtimeContext", self.context).get_bus(self)

    def map_symbol(self) -> str:
        if self.calculation_rate is CalculationRate.AUDIO:
            return f"a{self.id_}"
        elif self.calculation_rate is CalculationRate.CONTROL:
            return f"c{self.id_}"
        raise InvalidCalculationRate

    def set_(self, value: float) -> None:
        self.context.set_bus(self, value)


@dataclasses.dataclass(frozen=True)
class Node(ContextObject):
    def add_group(
        self,
        add_action: AddActionLike = AddAction.ADD_TO_HEAD,
        name: Optional[str] = None,
        parallel: bool = False,
        permanent=False,
    ) -> "Group":
        return self.context.add_group(
            add_action=add_action,
            name=name,
            parallel=parallel,
            permanent=permanent,
            target_node=self,
        )

    def add_synth(
        self,
        synthdef: SynthDef,
        *,
        add_action: AddActionLike = AddAction.ADD_TO_HEAD,
        name: Optional[str] = None,
        permanent=False,
        **settings,
    ) -> "Synth":
        return self.context.add_synth(
            synthdef=synthdef,
            add_action=add_action,
            name=name,
            permanent=permanent,
            target_node=self,
            **settings,
        )

    def free(self) -> None:
        return self.context.free_node(self)

    def map(self, **settings: Union[Bus, None]) -> None:
        self.context.map_node(self, **settings)

    def move(self, target: "Node", add_action: AddActionLike = None) -> None:
        self.context.move_node(node=self, add_action=add_action, target_node=target)

    def order(self, *nodes: "Node", add_action: AddActionLike = None) -> None:
        self.context.order_nodes(self, *nodes, add_action=add_action)

    def pause(self) -> None:
        self.context.pause_node(self)

    def query(self) -> Union[Awaitable[NodeInfo], NodeInfo]:
        return cast("RealtimeContext", self.context).query_node(self)

    def set_(self, **settings: SupportsFloat) -> None:
        self.context.set_node(self, **settings)

    def unpause(self) -> None:
        self.context.unpause_node(self)

    @property
    def active(self) -> bool:
        return cast("RealtimeContext", self.context)._node_active.get(self.id_, True)

    @property
    def parent(self) -> Optional["Group"]:
        parent_id = cast("RealtimeContext", self.context)._node_parents.get(self.id_)
        if parent_id is None:
            return None
        elif parent_id == 0:
            return RootNode(context=self.context)
        return Group(context=self.context, id_=parent_id)

    @property
    def valid_add_actions(self) -> Container[int]:
        return (
            AddAction.ADD_AFTER,
            AddAction.ADD_BEFORE,
            AddAction.ADD_TO_HEAD,
            AddAction.ADD_TO_TAIL,
            AddAction.REPLACE,
        )


@dataclasses.dataclass(frozen=True)
class Group(Node):
    parallel: bool = False

    def free_children(self, synths_only=False) -> None:
        self.context.free_group_children(self, synths_only=synths_only)

    @property
    def children(self) -> List[Node]:
        children: List[Node] = []
        for id_ in cast("RealtimeContext", self.context)._node_children.get(
            self.id_, []
        ):
            if id_ in cast("RealtimeContext", self.context)._node_children:
                children.append(Group(context=self.context, id_=id_))
            else:
                # cannot get synthdef name without running /g_queryTree
                children.append(Synth(context=self.context, id_=id_, synthdef=default))
        return children


@dataclasses.dataclass(frozen=True)
class RootNode(Group):
    id_: int = 0

    def __post_init__(self) -> None:
        object.__setattr__(self, "id_", 0)
        object.__setattr__(self, "parallel", False)

    @property
    def valid_add_actions(self) -> Container[int]:
        return (AddAction.ADD_TO_HEAD, AddAction.ADD_TO_TAIL)


@dataclasses.dataclass(frozen=True)
class Synth(Node):
    synthdef: SynthDef

    @property
    def valid_add_actions(self) -> Container[int]:
        return (AddAction.ADD_AFTER, AddAction.ADD_BEFORE, AddAction.REPLACE)


class Context(metaclass=abc.ABCMeta):
    """
    A synthesis execution context.
    """

    ### INITIALIZER ###

    def __init__(self, options: Optional[Options], **kwargs) -> None:
        self._audio_bus_allocator = BlockAllocator()
        self._buffer_allocator = BlockAllocator()
        self._client_id = 0
        self._control_bus_allocator = BlockAllocator()
        self._latency = 0.0
        self._node_id_allocator = NodeIdAllocator()
        self._options = new(options or Options(), **kwargs)
        self._sync_id = self._sync_id_minimum = 0
        self._sync_id_maximum = 32 << 26
        self._thread_local = threading.local()
        self._setup_allocators(self.client_id, self.options)

    ### PRIVATE METHODS ###

    def _add_requests(self, *requests: Request) -> None:
        with contextlib.ExitStack() as stack:
            current_requests = cast(
                RequestContext,
                self._get_request_context() or stack.enter_context(self.at()),
            ).requests
            for request in requests:
                current_requests.append((request, None))

    def _add_request_with_completion(
        self, request: Request, on_completion: Optional[Callable[["Context"], None]]
    ) -> Completion:
        with contextlib.ExitStack() as stack:
            current_requests = cast(
                RequestContext,
                self._get_request_context() or stack.enter_context(self.at()),
            ).requests
            moment = self._get_moment()
            if moment is None:
                raise ContextError
            completion = Completion(context=self, moment=moment, requests=[])
            current_requests.append((request, completion))
            if on_completion:
                stack.enter_context(completion)
                on_completion(self)
        return completion

    def _allocate_id(
        self,
        type_: Type[ContextObject],
        calculation_rate: Optional[CalculationRate] = None,
        count: int = 1,
        permanent: bool = False,
    ) -> int:
        if type_ is Node:
            if permanent:
                return self._node_id_allocator.allocate_permanent_node_id()
            return self._node_id_allocator.allocate_node_id()
        if type_ is Buffer:
            return self._buffer_allocator.allocate(count)
        if type_ is Bus:
            if calculation_rate is CalculationRate.AUDIO:
                return self._audio_bus_allocator.allocate(count)
            elif calculation_rate is CalculationRate.CONTROL:
                return self._control_bus_allocator.allocate(count)
        raise ValueError

    @staticmethod
    def _apply_completions(
        pairs: List[Tuple[Request, Optional[Completion]]]
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

    @abc.abstractmethod
    def _free_id(
        self,
        type_: Type[ContextObject],
        id_: int,
        calculation_rate: Optional[CalculationRate] = None,
    ) -> None:
        raise NotImplementedError

    def _get_allocator(
        self,
        type_: Type[ContextObject],
        calculation_rate: Optional[CalculationRate] = None,
    ) -> Union[BlockAllocator, NodeIdAllocator]:
        if type_ is Node:
            return self._node_id_allocator
        if type_ is Buffer:
            return self._buffer_allocator
        if type_ is Bus:
            if calculation_rate is CalculationRate.AUDIO:
                return self._audio_bus_allocator
            elif calculation_rate is CalculationRate.CONTROL:
                return self._control_bus_allocator
        raise ValueError

    def _get_moment(self) -> Optional[Moment]:
        moments = self._thread_local.__dict__.get("moments", [])
        if not moments:
            return None
        return moments[-1]

    def _get_request_context(self) -> Optional[RequestContext]:
        moments = self._thread_local.__dict__.get("moments", [])
        completions = self._thread_local.__dict__.get("completions", [])
        if completions:
            return completions[-1]
        if moments:
            return moments[-1]
        return None

    def _pop_completion(self) -> None:
        self._thread_local.__dict__.setdefault("completions", []).pop()

    def _pop_moment(self) -> None:
        self._thread_local.__dict__.setdefault("moments", []).pop()

    def _push_completion(self, completion: Completion) -> None:
        self._thread_local.__dict__.setdefault("completions", []).append(completion)

    def _push_moment(self, moment: Moment) -> None:
        self._thread_local.__dict__.setdefault("moments", []).append(moment)

    @abc.abstractmethod
    def _resolve_node(self, node: Union[Node, SupportsInt, None]) -> int:
        raise NotImplementedError

    def _setup_allocators(self, client_id: int, options: Options) -> None:
        # audio buses
        audio_bus_minimum, audio_bus_maximum = options.get_audio_bus_ids(client_id)
        self._audio_bus_allocator = BlockAllocator(
            heap_minimum=audio_bus_minimum, heap_maximum=audio_bus_maximum
        )
        # control buses
        control_bus_minimum, control_bus_maximum = options.get_control_bus_ids(
            client_id
        )
        self._control_bus_allocator = BlockAllocator(
            heap_minimum=control_bus_minimum, heap_maximum=control_bus_maximum
        )
        # buffers
        buffer_minimum, buffer_maximum = options.get_buffer_ids(client_id)
        self._buffer_allocator = BlockAllocator(
            heap_minimum=buffer_minimum, heap_maximum=buffer_maximum
        )
        # node IDs
        self._node_id_allocator = NodeIdAllocator(
            initial_node_id=options.initial_node_id, client_id=client_id
        )
        # sync IDs
        self._sync_id_minimum, self._sync_id_maximum = options.get_sync_ids(client_id)
        self._sync_id = self._sync_id_minimum

    @abc.abstractmethod
    def _validate_can_request(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _validate_moment_timestamp(self, seconds: Optional[float]):
        raise NotImplementedError

    ### PUBLIC METHODS ###

    def add_buffer(
        self,
        *,
        channel_count: Optional[int] = None,
        channel_indices: Optional[List[int]] = None,
        file_path: Optional[PathLike] = None,
        frame_count: Optional[int] = None,
        starting_frame: Optional[int] = None,
        on_completion: Optional[Callable[["Context"], None]] = None,
    ) -> Buffer:
        self._validate_can_request()
        if not (frame_count or file_path):
            raise ValueError
        if channel_count and channel_indices:
            raise ValueError
        id_ = self._allocate_id(Buffer)
        if file_path and channel_indices:
            request: Request = BufferAllocateReadChannelRequest(
                buffer_id=id_,
                channel_indices=channel_indices,
                file_path=file_path,
                frame_count=frame_count,
                starting_frame=starting_frame,
            )
        elif file_path:
            request = BufferAllocateReadRequest(
                buffer_id=id_,
                file_path=file_path,
                frame_count=frame_count,
                starting_frame=starting_frame,
            )
        else:
            request = BufferAllocateRequest(
                buffer_id=id_, channel_count=channel_count, frame_count=frame_count
            )
        completion = self._add_request_with_completion(request, on_completion)
        return Buffer(context=self, id_=id_, completion=completion)

    def add_buffer_group(
        self,
        *,
        channel_count: Optional[int] = None,
        count: int = 1,
        frame_count: Optional[int] = None,
    ) -> List[Buffer]:
        self._validate_can_request()
        if not (channel_count and frame_count):
            raise ValueError
        if count < 1:
            raise ValueError
        id_ = self._allocate_id(Buffer, count=count)
        buffers: List[Buffer] = []
        requests: List[Request] = []
        for i in range(count):
            buffers.append(Buffer(context=self, id_=id_ + i))
            requests.append(
                BufferAllocateRequest(
                    buffer_id=id_ + i,
                    channel_count=channel_count,
                    frame_count=frame_count,
                )
            )
        self._add_requests(*requests)
        return buffers

    def add_bus(
        self, calculation_rate: CalculationRateLike = CalculationRate.CONTROL
    ) -> Bus:
        self._validate_can_request()
        rate = CalculationRate.from_expr(calculation_rate)
        if rate not in (CalculationRate.AUDIO, CalculationRate.CONTROL):
            raise InvalidCalculationRate(rate)
        id_ = self._allocate_id(Bus, calculation_rate=rate)
        return Bus(calculation_rate=rate, context=self, id_=id_)

    def add_bus_group(
        self,
        calculation_rate: CalculationRateLike = CalculationRate.CONTROL,
        count: int = 1,
    ) -> List[Bus]:
        self._validate_can_request()
        rate = CalculationRate.from_expr(calculation_rate)
        if rate not in (CalculationRate.AUDIO, CalculationRate.CONTROL):
            raise InvalidCalculationRate(rate)
        if count < 1:
            raise ValueError
        id_ = self._allocate_id(Bus, calculation_rate=rate, count=count)
        return [
            Bus(calculation_rate=rate, context=self, id_=id_ + i) for i in range(count)
        ]

    def add_group(
        self,
        *,
        add_action: AddActionLike = AddAction.ADD_TO_HEAD,
        name: Optional[str] = None,
        parallel: bool = False,
        permanent=False,
        target_node: Optional[SupportsInt] = None,
    ) -> Group:
        self._validate_can_request()
        add_action_ = AddAction.from_expr(add_action)
        if isinstance(target_node, Node):
            if add_action_ not in target_node.valid_add_actions:
                raise ValueError(add_action_)
        target_node_id = self._resolve_node(target_node)
        id_ = self._allocate_id(Node, permanent=permanent)
        kwargs = dict(
            add_action=add_action_, node_id=id_, target_node_id=target_node_id
        )
        if parallel:
            request: Request = ParallelGroupNewRequest(
                items=[GroupNewRequest.Item(**kwargs)]
            )
        else:
            request = GroupNewRequest(items=[GroupNewRequest.Item(**kwargs)])
        self._add_requests(request)
        return Group(context=self, id_=id_, parallel=parallel)

    def add_synth(
        self,
        synthdef: SynthDef,
        *,
        add_action: AddActionLike = AddAction.ADD_TO_HEAD,
        name: Optional[str] = None,
        permanent=False,
        target_node: Optional[SupportsInt] = None,
        **settings,
    ) -> Synth:
        self._validate_can_request()
        add_action_ = AddAction.from_expr(add_action)
        if isinstance(target_node, Node):
            if add_action_ not in target_node.valid_add_actions:
                raise ValueError(add_action_)
        target_node_id = self._resolve_node(target_node)
        synthdef_kwargs: Dict[str, Union[float, str]] = {}
        for _, parameter in synthdef.indexed_parameters:
            if parameter.name not in settings:
                continue
            value = settings[parameter.name]
            if value == parameter.value:
                continue
            if parameter.parameter_rate is ParameterRate.SCALAR:
                synthdef_kwargs[parameter.name] = float(value)
            elif parameter.name in ("in_", "out"):
                synthdef_kwargs[parameter.name] = float(value)
            elif isinstance(value, Bus):
                synthdef_kwargs[parameter.name] = value.map_symbol()
            elif isinstance(value, str):
                synthdef_kwargs[parameter.name] = value
            else:
                synthdef_kwargs[parameter.name] = float(value)
        id_ = self._allocate_id(Node, permanent=permanent)
        self._add_requests(
            SynthNewRequest(
                add_action=add_action_,
                node_id=id_,
                synthdef=synthdef,
                target_node_id=target_node_id,
                **synthdef_kwargs,
            )
        )
        return Synth(context=self, id_=id_, synthdef=synthdef)

    def add_synthdefs(
        self,
        *synthdefs: SynthDef,
        on_completion: Optional[Callable[["Context"], None]] = None,
    ) -> Completion:
        self._validate_can_request()
        if not synthdefs:
            raise ValueError
        request = SynthDefReceiveRequest(synthdefs=synthdefs)
        return self._add_request_with_completion(request, on_completion)

    def at(self, seconds=None) -> Moment:
        self._validate_moment_timestamp(seconds)
        return Moment(context=self, seconds=seconds, requests=[])

    def close_buffer(
        self,
        buffer: Buffer,
        on_completion: Optional[Callable[["Context"], None]] = None,
    ) -> Completion:
        self._validate_can_request()
        request = BufferCloseRequest(buffer_id=buffer.id_)
        return self._add_request_with_completion(request, on_completion)

    def copy_buffer(
        self,
        *,
        source_buffer: Buffer,
        target_buffer: Buffer,
        source_starting_frame: int,
        target_starting_frame: int,
        frame_count: int,
    ):
        self._validate_can_request()
        request = BufferCopyRequest(
            frame_count=frame_count,
            source_buffer_id=source_buffer,
            source_starting_frame=source_starting_frame,
            target_buffer_id=target_buffer,
            target_starting_frame=target_starting_frame,
        )
        self._add_requests(request)

    def fill_buffer(
        self, buffer: Buffer, starting_frame: int, frame_count: int, value: float
    ) -> None:
        self._validate_can_request()
        request = BufferFillRequest(
            buffer_id=buffer,
            index_count_value_triples=[(starting_frame, frame_count, value)],
        )
        self._add_requests(request)

    def fill_buses(self, bus: Bus, count: int, value: float) -> None:
        self._validate_can_request()
        if bus.calculation_rate != CalculationRate.CONTROL:
            raise InvalidCalculationRate
        request = ControlBusFillRequest(
            index_count_value_triples=[(bus.id_, count, value)]
        )
        self._add_requests(request)

    def free_buffer(
        self,
        buffer: Buffer,
        on_completion: Optional[Callable[["Context"], None]] = None,
    ) -> Completion:
        self._validate_can_request()
        request = BufferFreeRequest(buffer_id=buffer)
        return self._add_request_with_completion(request, on_completion)

    def free_bus(self, bus: Bus) -> None:
        self._validate_can_request()
        self._free_id(Bus, bus.id_, calculation_rate=bus.calculation_rate)

    def free_group_children(self, group: Group, synths_only=False) -> None:
        self._validate_can_request()
        if synths_only:
            request: Request = GroupDeepFreeRequest(group.id_)
        else:
            request = GroupFreeAllRequest(group.id_)
        self._add_requests(request)

    def free_node(self, node: Node) -> None:
        self._validate_can_request()
        request = NodeReleaseRequest(
            node.id_,
            has_gate=isinstance(node, Synth) and "gate" in node.synthdef.parameters,
        )
        self._add_requests(request)

    def free_synthdefs(self, *synthdefs: SynthDef) -> None:
        self._validate_can_request()
        if not synthdefs:
            raise ValueError
        request = SynthDefFreeRequest(*synthdefs)
        self._add_requests(request)

    def free_all_synthdefs(self) -> None:
        self._validate_can_request()
        request = SynthDefFreeAllRequest()
        self._add_requests(request)

    def load_synthdefs(
        self,
        path: PathLike,
        on_completion: Optional[Callable[["Context"], None]] = None,
    ) -> Completion:
        self._validate_can_request()
        request = SynthDefLoadRequest(path=path)
        return self._add_request_with_completion(request, on_completion)

    def load_synthdefs_directory(
        self,
        path: PathLike,
        on_completion: Optional[Callable[["Context"], None]] = None,
    ) -> Completion:
        self._validate_can_request()
        request = SynthDefLoadDirectoryRequest(path=path)
        return self._add_request_with_completion(request, on_completion)

    def map_node(self, node: Node, **settings: Union[Bus, None]) -> None:
        self._validate_can_request()
        control, audio = {}, {}
        for key, value in settings.items():
            if isinstance(value, Bus):
                if value.calculation_rate is CalculationRate.AUDIO:
                    audio[key] = int(value)
                else:
                    control[key] = int(value)
            elif value is None:
                control[key] = -1
        requests: List[Request] = []
        if control:
            requests.append(NodeMapToControlBusRequest(node_id=node, **control))
        if audio:
            requests.append(NodeMapToAudioBusRequest(node_id=node, **audio))
        self._add_requests(*requests)

    def move_node(
        self, node: Node, add_action: AddActionLike, target_node: Node
    ) -> None:
        self._validate_can_request()
        add_action_ = AddAction.from_expr(add_action)
        items = [(node, target_node)]
        if add_action_ is AddAction.ADD_BEFORE:
            request: Request = NodeBeforeRequest(items)
        elif add_action_ is AddAction.ADD_AFTER:
            request = NodeAfterRequest(items)
        elif add_action_ is AddAction.ADD_TO_TAIL:
            request = GroupTailRequest(items)
        elif add_action_ is AddAction.ADD_TO_HEAD:
            request = GroupHeadRequest(items)
        else:
            raise ValueError
        self._add_requests(request)

    def normalize_buffer(self, buffer: Buffer, new_maximum: float = 1.0) -> None:
        self._validate_can_request()
        request = BufferNormalizeRequest(buffer_id=buffer.id_, new_maximum=new_maximum)
        self._add_requests(request)

    def order_nodes(
        self, target_node: Node, *nodes: Node, add_action: AddActionLike = None
    ) -> None:
        self._validate_can_request()
        request = NodeOrderRequest(add_action, target_node, *nodes)
        self._add_requests(request)

    def pause_node(self, node: Node) -> None:
        self._validate_can_request()
        request = NodeRunRequest([[node, False]])
        self._add_requests(request)

    def read_buffer(
        self,
        buffer: Buffer,
        file_path: PathLike,
        *,
        buffer_starting_frame: Optional[int] = None,
        channel_indices: Optional[List[int]] = None,
        frame_count: Optional[int] = None,
        leave_open: bool = False,
        starting_frame: Optional[int] = None,
        on_completion: Optional[Callable[["Context"], None]] = None,
    ) -> Completion:
        self._validate_can_request()
        kwargs = dict(
            buffer_id=buffer.id_,
            file_path=file_path,
            frame_count=frame_count,
            leave_open=leave_open,
            starting_frame_in_buffer=buffer_starting_frame,
            starting_frame_in_file=starting_frame,
        )
        if channel_indices:
            request: Request = BufferReadChannelRequest(
                **kwargs, channel_indices=channel_indices
            )
        else:
            request = BufferReadRequest(**kwargs)
        return self._add_request_with_completion(request, on_completion)

    @abc.abstractmethod
    def send(self, requestable: Requestable):
        raise NotImplementedError

    def set_bus(self, bus: Bus, value: float) -> None:
        self._validate_can_request()
        if bus.calculation_rate != CalculationRate.CONTROL:
            raise InvalidCalculationRate
        request = ControlBusSetRequest(index_value_pairs=[[bus.id_, value]])
        self._add_requests(request)

    def set_node(self, node: Node, **settings: SupportsFloat) -> None:
        self._validate_can_request()
        coerced_settings: Dict[str, float] = {}
        for key, value in settings.items():
            coerced_settings[key] = float(value)
        request = NodeSetRequest(node_id=node.id_, **coerced_settings)
        self._add_requests(request)

    def unpause_node(self, node: Node) -> None:
        self._validate_can_request()
        request = NodeRunRequest([[node, True]])
        self._add_requests(request)

    def write_buffer(
        self,
        buffer: Buffer,
        file_path: PathLike,
        *,
        frame_count: Optional[int] = None,
        header_format: HeaderFormatLike = "aiff",
        leave_open: bool = False,
        sample_format: SampleFormatLike = "int24",
        starting_frame: Optional[int] = None,
        on_completion: Optional[Callable[["Context"], None]] = None,
    ) -> Completion:
        self._validate_can_request()
        request = BufferWriteRequest(
            buffer_id=buffer.id_,
            file_path=file_path,
            frame_count=frame_count,
            header_format=header_format,
            leave_open=leave_open,
            sample_format=sample_format,
            starting_frame=starting_frame,
        )
        return self._add_request_with_completion(request, on_completion)

    def zero_buffer(
        self,
        buffer: Buffer,
        on_completion: Optional[Callable[["Context"], None]] = None,
    ) -> Completion:
        self._validate_can_request()
        request = BufferZeroRequest(buffer_id=buffer)
        return self._add_request_with_completion(request, on_completion)

    ### PUBLIC PROPERTIES ###

    @property
    def client_id(self) -> int:
        return self._client_id

    @property
    def options(self) -> Options:
        return self._options

    @property
    def root_node(self) -> RootNode:
        return RootNode(context=self)
