"""
Core interfaces for interfacting with :term:`scsynth`-compatible execution contexts.

Context subclasses expose a common interface for realtime and non-realtime synthesis.
"""

import abc
import contextlib
import contextvars
import dataclasses
import itertools
import re
import threading
from collections.abc import Sequence as SequenceABC
from os import PathLike
from typing import (
    Any,
    Callable,
    Literal,
    Optional,
    Sequence,
    SupportsFloat,
    SupportsInt,
    Type,
    cast,
)

from uqbar.objects import new

from ..enums import AddAction, BootStatus, CalculationRate
from ..exceptions import (
    AllocationError,
    ContextError,
    InvalidCalculationRate,
    MomentClosed,
)
from ..scsynth import Options
from ..typing import (
    AddActionLike,
    CalculationRateLike,
    HeaderFormatLike,
    SampleFormatLike,
    SupportsOsc,
)
from ..ugens import SynthDef
from .allocators import BlockAllocator, NodeIdAllocator
from .entities import (
    Buffer,
    BufferGroup,
    Bus,
    BusGroup,
    ContextObject,
    Group,
    Node,
    RootNode,
    ScopeBuffer,
    Synth,
)
from .requests import (
    AllocateBuffer,
    AllocateReadBuffer,
    AllocateReadBufferChannel,
    ClearSchedule,
    CloseBuffer,
    CopyBuffer,
    DoNothing,
    FillBuffer,
    FillControlBusRange,
    FreeAllSynthDefs,
    FreeBuffer,
    FreeGroupChildren,
    FreeGroupDeep,
    FreeSynthDef,
    GenerateBuffer,
    LoadSynthDefDirectory,
    LoadSynthDefs,
    MapAudioBusToNode,
    MapControlBusToNode,
    MoveNodeAfter,
    MoveNodeBefore,
    MoveNodeToGroupHead,
    MoveNodeToGroupTail,
    NewGroup,
    NewParallelGroup,
    NewSynth,
    NormalizeBuffer,
    OrderNodes,
    ReadBuffer,
    ReadBufferChannel,
    ReceiveSynthDefs,
    ReleaseNode,
    Request,
    RequestBundle,
    RunNode,
    SetBuffer,
    SetBufferRange,
    SetControlBus,
    SetControlBusRange,
    SetNodeControl,
    SetNodeControlRange,
    WriteBuffer,
    ZeroBuffer,
)

BUS_PATTERN = re.compile("([ac])(\\d+)")


@dataclasses.dataclass
class Moment:
    """
    A context manager representing a moment in time when requests are made to an execution context.

    Multiple requests made inside a moment are bundled together.

    :param context: The moment's context.
    :param seconds: The moment's timestamp.
    """

    context: "Context"
    seconds: float | None = None
    closed: bool = dataclasses.field(default=False, init=False)
    requests: list[tuple[Request, Optional["Completion"]]] = dataclasses.field(
        default_factory=list, init=False
    )

    def __enter__(self) -> "Moment":
        """
        set this moment the current "request context".
        """
        if self.closed:
            raise MomentClosed
        self.context._push_moment(self)
        return self

    def __exit__(self, *args) -> None:
        """
        Unset this moment as the current "request context".
        """
        self.context._pop_moment()
        requests = self.context._apply_completions(self.requests)
        timestamp = (
            self.seconds + self.context._latency if self.seconds is not None else None
        )
        if len(requests) and timestamp is not None:
            self.context.send(RequestBundle(timestamp=timestamp, contents=requests))
        elif len(requests) > 1:
            self.context.send(RequestBundle(contents=requests))
        elif len(requests):
            self.context.send(requests[0])
        self.closed = True


@dataclasses.dataclass
class Completion:
    """
    A context manager for collecting requests to be made "on completion" of another request.

    Multiple requests made inside a completion are bundled together.

    :param context: The completion's context.
    :param moment: The completion's moment.
    """

    context: "Context"
    moment: Moment
    requests: list[tuple[Request, Optional["Completion"]]] = dataclasses.field(
        default_factory=list, init=False
    )

    def __call__(self, request: Request) -> Request:
        """
        Bundle this completion's collected requests into the ``on_completion`` argument of the request.

        :param request: The request to complete.
        """
        if not hasattr(request, "on_completion"):
            raise ValueError(request)
        requests = self.context._apply_completions(self.requests)
        if len(requests) > 1:
            request = new(request, on_completion=RequestBundle(contents=requests))
        elif len(requests) == 1:
            request = new(request, on_completion=requests[0])
        return request

    def __enter__(self) -> "Completion":
        """
        set this completion as the current "request context".
        """
        if self.moment.closed:
            raise MomentClosed
        self.context._push_completion(self)
        return self

    def __exit__(self, *args) -> None:
        """
        Unset this completion as the current "request context".
        """
        self.context._pop_completion()


class Context(metaclass=abc.ABCMeta):
    """
    A synthesis execution context.

    :param options: The context's options.
    :param kwargs: Keyword arguments for options.
    """

    ### INITIALIZER ###

    def __init__(
        self,
        options: Options | None,
        name: str | None = None,
        **kwargs,
    ) -> None:
        self._audio_bus_allocator = BlockAllocator()
        self._boot_status: BootStatus = BootStatus.OFFLINE
        self._buffer_allocator = BlockAllocator()
        self._client_id: int = 0
        self._completions: contextvars.ContextVar[list[Completion]] = (
            contextvars.ContextVar("completions")
        )
        self._control_bus_allocator = BlockAllocator()
        self._latency: float = 0.0
        self._lock = threading.RLock()
        self._moments: contextvars.ContextVar[list[Moment]] = contextvars.ContextVar(
            "moments"
        )
        self._name: str | None = name
        self._node_id_allocator = NodeIdAllocator()
        self._options: Options = self._get_options(options, **kwargs)
        self._scope_buffer_allocator: BlockAllocator | None = None
        self._sync_id: int = 0
        self._sync_id_maximum: int = 32 << 26
        self._sync_id_minimum: int = 0

    ### SPECIAL METHODS ###

    def __getstate__(self) -> dict:
        state = self.__dict__.copy()
        del state["_completions"]
        del state["_lock"]
        del state["_moments"]
        return state

    def __setstate__(self, state: dict) -> None:
        self.__dict__.update(state)
        self._completions = contextvars.ContextVar("completions")
        self._lock = threading.RLock()
        self._moments = contextvars.ContextVar("moments")

    ### PRIVATE METHODS ###

    def _add_requests(self, *requests: Request) -> None:
        with contextlib.ExitStack() as stack:
            current_requests = (
                self._get_request_context() or stack.enter_context(self.at())
            ).requests
            for request in requests:
                current_requests.append((request, None))

    def _add_request_with_completion(
        self, request: Request, on_completion: Callable[["Context"], None] | None
    ) -> Completion:
        with contextlib.ExitStack() as stack:
            current_requests = (
                self._get_request_context() or stack.enter_context(self.at())
            ).requests
            moment = self._get_moment()
            if moment is None:
                raise ContextError
            completion = Completion(context=self, moment=moment)
            current_requests.append((request, completion))
            if on_completion:
                stack.enter_context(completion)
                on_completion(self)
        return completion

    def _allocate_id(
        self,
        type_: Type[ContextObject],
        calculation_rate: CalculationRate | None = None,
        count: int = 1,
        permanent: bool = False,
    ) -> int:
        id_: int | None = None
        if type_ is Node:
            if permanent:
                id_ = self._node_id_allocator.allocate_permanent_node_id()
            else:
                id_ = self._node_id_allocator.allocate_node_id()
        elif type_ is Buffer:
            id_ = self._buffer_allocator.allocate(count)
        elif type_ is Bus:
            if calculation_rate is CalculationRate.AUDIO:
                id_ = self._audio_bus_allocator.allocate(count)
            elif calculation_rate is CalculationRate.CONTROL:
                id_ = self._control_bus_allocator.allocate(count)
            else:
                raise ValueError(calculation_rate)
        elif type_ is ScopeBuffer and self._scope_buffer_allocator:
            id_ = self._scope_buffer_allocator.allocate(count)
        else:
            raise ValueError(type_)
        if id_ is None:
            raise AllocationError
        return id_

    @staticmethod
    def _apply_completions(
        pairs: list[tuple[Request, Completion | None]],
    ) -> list[Request]:
        requests: list[Request] = []
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
        calculation_rate: CalculationRate | None = None,
    ) -> None:
        raise NotImplementedError

    def _get_allocator(
        self,
        type_: Type[ContextObject],
        calculation_rate: CalculationRate | None = None,
    ) -> BlockAllocator | NodeIdAllocator:
        if type_ is Node:
            return self._node_id_allocator
        if type_ is Buffer:
            return self._buffer_allocator
        if type_ is Bus:
            if calculation_rate is CalculationRate.AUDIO:
                return self._audio_bus_allocator
            elif calculation_rate is CalculationRate.CONTROL:
                return self._control_bus_allocator
        if type_ is ScopeBuffer and self._scope_buffer_allocator:
            return self._scope_buffer_allocator
        raise ValueError

    def _get_completions(self) -> list[Completion]:
        self._completions.set(completions := self._completions.get([]))
        return completions

    def _get_moments(self) -> list[Moment]:
        self._moments.set(moments := self._moments.get([]))
        return moments

    def _get_moment(self) -> Moment | None:
        if not (moments := self._get_moments()):
            return None
        return moments[-1]

    def _get_next_sync_id(self) -> int:
        with self._lock:
            sync_id = self._sync_id
            self._sync_id += 1
            if self._sync_id > self._sync_id_maximum:
                self._sync_id = self._sync_id_minimum
            return sync_id

    def _get_options(self, options: Options | None, **kwargs) -> Options:
        return dataclasses.replace(options or Options(), **kwargs)

    def _get_request_context(self) -> Completion | Moment | None:
        moments = self._get_moments()
        completions = self._get_completions()
        if completions:
            return completions[-1]
        if moments:
            return moments[-1]
        return None

    def _pop_completion(self) -> None:
        self._get_completions().pop()

    def _pop_moment(self) -> None:
        self._get_moments().pop()

    def _push_completion(self, completion: Completion) -> None:
        self._get_completions().append(completion)

    def _push_moment(self, moment: Moment) -> None:
        self._get_moments().append(moment)

    @abc.abstractmethod
    def _resolve_node(self, node: Node | SupportsInt | None) -> int:
        raise NotImplementedError

    def _setup_allocators(self, owned: bool = False) -> None:
        # audio buses
        audio_bus_minimum, audio_bus_maximum = self.options.get_audio_bus_ids(
            self.client_id
        )
        self._audio_bus_allocator = BlockAllocator(
            heap_minimum=audio_bus_minimum, heap_maximum=audio_bus_maximum
        )
        # control buses
        control_bus_minimum, control_bus_maximum = self.options.get_control_bus_ids(
            self.client_id
        )
        self._control_bus_allocator = BlockAllocator(
            heap_minimum=control_bus_minimum, heap_maximum=control_bus_maximum
        )
        # buffers
        buffer_minimum, buffer_maximum = self.options.get_buffer_ids(self.client_id)
        self._buffer_allocator = BlockAllocator(
            heap_minimum=buffer_minimum, heap_maximum=buffer_maximum
        )
        # node IDs
        self._node_id_allocator = NodeIdAllocator(
            initial_node_id=self.options.initial_node_id, client_id=self.client_id
        )
        # scope buffers
        self._scope_buffer_allocator = (
            BlockAllocator(heap_minimum=0, heap_maximum=128) if owned else None
        )
        # sync IDs
        self._sync_id_minimum, self._sync_id_maximum = self.options.get_sync_ids(
            self.client_id
        )
        self._sync_id = self._sync_id_minimum

    @abc.abstractmethod
    def _validate_can_request(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _validate_moment_timestamp(self, seconds: float | None) -> None:
        raise NotImplementedError

    ### PUBLIC METHODS ###

    def add_buffer(
        self,
        *,
        channel_count: int | None = None,
        channel_indices: list[int] | None = None,
        file_path: PathLike | None = None,
        frame_count: int | None = None,
        starting_frame: int | None = None,
        on_completion: Callable[["Context"], Any] | None = None,
    ) -> Buffer:
        """
        Add a new buffer to the context.

        Emit ``/b_alloc``, ``/b_allocRead`` or ``/b_allocReadChannel`` requests
        depending on parameters.

        :param channel_count: The channel count of the new buffer. Cannot be used when
            reading from file paths.
        :param channel_indices: The channels to read from a file when reading from a
            file.
        :param file_path: The (optional) file to read from.
        :param frame_count: The frame count of the new buffer.
        :param starting_frame: The frame to start reading from when reading from a file.
        :param on_completion: A callable with the buffer's context as the only argument.
            Permits building an "on completion" argument to this method's request
            without an active moment.
        """
        self._validate_can_request()
        if not (frame_count or file_path):
            raise ValueError
        if channel_count and channel_indices:
            raise ValueError
        if channel_count and file_path:
            raise ValueError
        id_ = self._allocate_id(Buffer)
        if file_path and channel_indices:
            request: Request = AllocateReadBufferChannel(
                buffer_id=id_,
                channel_indices=channel_indices,
                path=file_path,
                frame_count=frame_count or 0,
                starting_frame=starting_frame or 0,
            )
        elif file_path:
            request = AllocateReadBuffer(
                buffer_id=id_,
                path=file_path,
                frame_count=frame_count or 0,
                starting_frame=starting_frame or 0,
            )
        elif frame_count:
            request = AllocateBuffer(
                buffer_id=id_, channel_count=channel_count or 1, frame_count=frame_count
            )
        else:
            raise ValueError
        completion = self._add_request_with_completion(request, on_completion)
        return Buffer(context=self, id_=id_, completion=completion)

    def add_buffer_group(
        self,
        *,
        channel_count: int | None = None,
        count: int = 1,
        frame_count: int | None = None,
    ) -> BufferGroup:
        """
        Add a group of new buffers to the context.

        Emit ``/b_alloc`` requests.

        :param channel_count: The channel count of the new buffers.
        :param count: The number of buffers to add.
        :param frame_count: The frame count of the new buffers.
        """
        self._validate_can_request()
        if not (channel_count and frame_count):
            raise ValueError
        if count < 1:
            raise ValueError
        id_ = self._allocate_id(Buffer, count=count)
        requests: list[Request] = []
        for i in range(count):
            requests.append(
                AllocateBuffer(
                    buffer_id=id_ + i,
                    channel_count=channel_count,
                    frame_count=frame_count,
                )
            )
        self._add_requests(*requests)
        return BufferGroup(
            context=self,
            id_=id_,
            count=count,
        )

    def add_bus(
        self, calculation_rate: CalculationRateLike = CalculationRate.CONTROL
    ) -> Bus:
        """
        Add a new bus to the context.

        Emit no requests.

        :param calculation_rate: The calculation rate of the new bus.
        """
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
    ) -> BusGroup:
        """
        Add a group of new buses to the context.

        Emit no requests.

        :param calculation_rate: The calculation rate of the new bus.
        :param count: The number of buses to add.
        """
        self._validate_can_request()
        rate = CalculationRate.from_expr(calculation_rate)
        if rate not in (CalculationRate.AUDIO, CalculationRate.CONTROL):
            raise InvalidCalculationRate(rate)
        if count < 1:
            raise ValueError
        id_ = self._allocate_id(Bus, calculation_rate=rate, count=count)
        return BusGroup(
            calculation_rate=rate,
            context=self,
            count=count,
            id_=id_,
        )

    def add_group(
        self,
        *,
        add_action: AddActionLike = AddAction.ADD_TO_HEAD,
        target_node: SupportsInt | None = None,
        parallel: bool = False,
        permanent: bool = False,
    ) -> Group:
        """
        Add a new group node to the context.

        Emit ``/g_new`` or ``/p_new`` requests depending on parameters.

        :param add_action: The :term:`add action` to use when placing the new group.
        :param target_node: The node to place the new group relative to.
        :param parallel: Flag for parallel vs non-parallel groups.
        :param permanent: Flag for using a permanent node ID.
        """
        self._validate_can_request()
        add_action_ = AddAction.from_expr(add_action)
        if isinstance(target_node, Node):
            if add_action_ not in target_node._valid_add_actions:
                raise ValueError(add_action_)
        target_node_id = self._resolve_node(target_node)
        id_ = self._allocate_id(Node, permanent=permanent)
        items = [(id_, add_action_, target_node_id)]
        if parallel:
            request: Request = NewParallelGroup(items=items)
        else:
            request = NewGroup(items=items)
        self._add_requests(request)
        return Group(context=self, id_=id_, parallel=parallel)

    def add_scope_buffer(self) -> ScopeBuffer:
        """
        Add a new scope buffer to the context.
        """
        self._validate_can_request()
        id_ = self._allocate_id(ScopeBuffer)
        return ScopeBuffer(context=self, id_=id_)

    def add_synth(
        self,
        synthdef: SynthDef,
        *,
        add_action: AddActionLike = AddAction.ADD_TO_HEAD,
        target_node: SupportsInt | None = None,
        permanent: bool = False,
        **settings: SupportsFloat | str | Sequence[SupportsFloat | str],
    ) -> Synth:
        """
        Add a new synth node to the context.

        Emit ``/s_new`` requests.

        :param synthdef: The :term:`SynthDef` to use for the new synth.
        :param add_action: The :term:`add action` to use when placing the new synth.
        :param target_node: The node to place the new synth relative to.
        :param permanent: Flag for using a permanent node ID.
        :param settings: The new synth's control settings.
        """
        self._validate_can_request()
        add_action_ = AddAction.from_expr(add_action)
        if isinstance(target_node, Node):
            if add_action_ not in target_node._valid_add_actions:
                raise ValueError(add_action_)
        target_node_id = self._resolve_node(target_node)
        synthdef_kwargs: dict[int | str, float | str | tuple[float | str, ...]] = {}
        for _, parameter in synthdef.indexed_parameters:
            if parameter.name not in settings:
                continue
            value = settings[parameter.name]
            if not isinstance(value, Sequence) or isinstance(value, str):
                value = (value,)
            if value == parameter.value:
                continue
            processed_values: list[float | str] = []
            for v in value:
                if isinstance(v, str):
                    if not BUS_PATTERN.match(v):
                        raise ValueError(v)
                    processed_values.append(v)
                else:
                    processed_values.append(float(v))
            if len(processed_values) == 1:
                synthdef_kwargs[parameter.name] = processed_values[0]
            else:
                synthdef_kwargs[parameter.name] = tuple(processed_values)
        id_ = self._allocate_id(Node, permanent=permanent)
        self._add_requests(
            NewSynth(
                add_action=add_action_,
                synth_id=id_,
                synthdef=synthdef,
                target_node_id=target_node_id,
                controls=synthdef_kwargs,
            )
        )
        return Synth(context=self, id_=id_, synthdef=synthdef)

    def add_synthdefs(
        self,
        *synthdefs: SynthDef,
        on_completion: Callable[["Context"], Any] | None = None,
    ) -> Completion:
        """
        Add one or more SynthDefs to the context.

        Emit ``/d_recv`` requests.

        :param synthdefs: The synthdefs to add.
        :param on_completion: A callable with the buffer's context as the only argument.
            Permits building an "on completion" argument to this method's request
            without an active moment.
        """
        self._validate_can_request()
        if not synthdefs:
            raise ValueError
        request = ReceiveSynthDefs(synthdefs=synthdefs)
        return self._add_request_with_completion(request, on_completion)

    def at(self, seconds=None) -> Moment:
        """
        Create a Moment.

        :param seconds: The timestamp of the new moment.
        """
        self._validate_moment_timestamp(seconds)
        return Moment(context=self, seconds=seconds)

    def clear_schedule(self) -> None:
        """
        Clear all scheduled bundles.

        Emit ``/clearSched`` requests.
        """
        self._validate_can_request()
        request = ClearSchedule()
        self._add_requests(request)

    def close_buffer(
        self,
        buffer: Buffer,
        on_completion: Callable[["Context"], Any] | None = None,
    ) -> Completion:
        """
        Close a buffer.

        Emit ``/b_close`` requests.

        :param buffer: The buffer to close.
        :param on_completion: A callable with the buffer's context as the only argument.
            Permits building an "on completion" argument to this method's request
            without an active moment.
        """
        self._validate_can_request()
        request = CloseBuffer(buffer_id=buffer.id_)
        return self._add_request_with_completion(request, on_completion)

    def copy_buffer(
        self,
        *,
        source_buffer: Buffer,
        target_buffer: Buffer,
        source_starting_frame: int,
        target_starting_frame: int,
        frame_count: int,
    ) -> None:
        """
        Copy a buffer.

        Emit ``/b_gen <buffer.id_> copy ...`` requests.

        :param source_buffer: The buffer to copy from.
        :param target_buffer: The buffer to copy to.
        :param source_starting_frame: The frame index in the source buffer to start
            reading from.
        :param target_starting_frame: The frame index in the target buffer to start
            writing at.
        :param frame_count: The number of frames to copy.
        """
        self._validate_can_request()
        request = CopyBuffer(
            frame_count=frame_count,
            source_buffer_id=source_buffer,
            source_starting_frame=source_starting_frame,
            target_buffer_id=target_buffer,
            target_starting_frame=target_starting_frame,
        )
        self._add_requests(request)

    def do_nothing(self) -> None:
        """
        Emit a no-op "nothing" command.
        """
        self._validate_can_request()
        self._add_requests(DoNothing())

    def fill_buffer(
        self, buffer: Buffer, starting_frame: int, frame_count: int, value: float
    ) -> None:
        """
        Fill a buffer with a single value.

        Emit ``/b_fill`` requests.

        :param buffer: The buffer to fill.
        :param starting_frame: The frame index to start filling at.
        :param frame_count: The number of frames to fill.
        :param value: The value to fill with.
        """
        self._validate_can_request()
        request = FillBuffer(
            buffer_id=buffer, items=[(starting_frame, frame_count, value)]
        )
        self._add_requests(request)

    def fill_bus_range(
        self, bus: Bus, count: int, value: float, use_shared_memory: bool = False
    ) -> None:
        """
        Fill a contiguous range of buses with a single value.

        Emit ``/c_fill`` requests.

        :param count: The number of buses to fill.
        :param value: The value to fill with.
        :param use_shared_memory: If true, use the shared memory interface.
            Skip bundling the request in any open moment.
        """
        self._validate_can_request()
        if bus.calculation_rate != CalculationRate.CONTROL:
            raise InvalidCalculationRate
        if use_shared_memory and (shared_memory := getattr(self, "_shared_memory")):
            shared_memory[int(bus) : int(bus) + count] = [value] * count
            return
        request = FillControlBusRange(items=[(int(bus), count, value)])
        self._add_requests(request)

    def free_buffer(
        self,
        buffer: Buffer,
        on_completion: Callable[["Context"], Any] | None = None,
    ) -> Completion:
        """
        Free a buffer.

        Emit ``/b_free`` requests.

        .. note::

            Freeing the first buffer of a buffer group will free the IDs of all buffers
            in the group, but will only issue a ``/b_free`` request for the first
            buffer.

        :param buffer: The buffer to free.
        :param on_completion: A callable with the buffer's context as the only argument.
            Permits building an "on completion" argument to this method's request
            without an active moment.
        """
        self._validate_can_request()
        request = FreeBuffer(buffer_id=buffer)
        return self._add_request_with_completion(request, on_completion)

    def free_buffer_group(self, buffer_group: BufferGroup) -> None:
        """
        Free a buffer grop.

        Emit ``/b_free`` requests.

        :param buffer_group: The buffer group to free.
        """
        self._validate_can_request()
        with contextlib.ExitStack() as stack:
            if not self._get_request_context():
                stack.enter_context(self.at())
            for buffer_ in buffer_group.buffers:
                self._add_requests(FreeBuffer(buffer_id=buffer_.id_))

    def free_bus(self, bus: Bus) -> None:
        """
        Free a bus.

        Emit no requests.

        .. note::

            Freeing the first bus of a bus group will free the IDs of the entire group.

        :param bus: The bus to free.
        """
        self._validate_can_request()
        self._free_id(Bus, bus.id_, calculation_rate=bus.calculation_rate)

    def free_bus_group(self, bus_group: BusGroup) -> None:
        """
        Free a bus group.

        Emit no requests.

        :param bus_group: The bus group to free.
        """
        self._validate_can_request()
        self._free_id(Bus, bus_group.id_, calculation_rate=bus_group.calculation_rate)

    def free_group_children(self, group: Group, synths_only: bool = False) -> None:
        """
        Free a group's children.

        Emit ``/g_deepFree`` or ``/g_freeAll`` requests depending on parameters.

        :param group: The group whose children will be freed.
        :param synths_only: Flag for freeing only child synths, or all children.
        """
        self._validate_can_request()
        if synths_only:
            request: Request = FreeGroupDeep(node_ids=[group.id_])
        else:
            request = FreeGroupChildren(node_ids=[group.id_])
        self._add_requests(request)

    def free_node(self, node: Node, force: bool = False) -> None:
        """
        Free a node.

        Emit ``/n_free`` for groups, for synths without a ``gate`` control, or when
        ``force`` is ``True``.

        Emit ``/n_set <node.id_> gate 0`` for synths with ``gate`` controls.

        :param node: The node to free.
        :param force: Flag for force-freeing, without releasing.
        """
        self._validate_can_request()
        request = ReleaseNode(
            node.id_,
            force=force,
            has_gate=isinstance(node, Synth) and "gate" in node.synthdef.parameters,
        )
        self._add_requests(request)

    def free_scope_buffer(self, scope_buffer: ScopeBuffer) -> None:
        """
        Free a scope buffer.

        :param scope_buffer: The scope buffer to free.
        """
        self._validate_can_request()
        self._free_id(ScopeBuffer, scope_buffer.id_)

    def free_synthdefs(self, *synthdefs: SynthDef) -> None:
        """
        Free one or more SynthDefs.

        Emit ``/d_free`` requests.

        :param synthdefs: The synthdefs to free.
        """
        self._validate_can_request()
        if not synthdefs:
            raise ValueError
        request = FreeSynthDef(synthdefs=synthdefs)
        self._add_requests(request)

    def free_all_synthdefs(self) -> None:
        """
        Free all SynthDefs.

        Emit ``/d_freeAll`` requests.
        """
        self._validate_can_request()
        request = FreeAllSynthDefs()
        self._add_requests(request)

    def generate_buffer(
        self,
        buffer: Buffer,
        command_name: Literal["sine1", "sine2", "sine3", "cheby"],
        amplitudes: Sequence[float],
        frequencies: Sequence[float] | None = None,
        phases: Sequence[float] | None = None,
        as_wavetable: bool = False,
        should_clear_first: bool = False,
        should_normalize: bool = False,
    ) -> None:
        """
        Generate a buffer.

        Emit ``/b_gen`` requests.

        :param buffer: The buffer to generate.
        :param command_name: The generation command name.
        :param amplitudes: A sequence of partial amplitudes.
        :param frequencies: A sequence of partial frequencies.
        :param phases: A sequence of partial phases.
        :param as_wavetable: Flag for generating the output in wavetable format.
        :param should_clear_first: Flag for clearing the buffer before generating.
        :param should_normalize: Flag for normalizing the generated output.
        """
        self._validate_can_request()
        if not amplitudes:
            raise ValueError
        if command_name == "sine2":
            if not frequencies:
                raise ValueError
            elif not (len(amplitudes) == len(frequencies)):
                raise ValueError
        elif command_name == "sine3":
            if not frequencies or not phases:
                raise ValueError
            elif not (len(amplitudes) == len(frequencies) == len(phases)):
                raise ValueError
        request = GenerateBuffer(
            buffer_id=buffer,
            command_name=command_name,
            amplitudes=amplitudes,
            frequencies=frequencies,
            phases=phases,
            as_wavetable=as_wavetable,
            should_clear_first=should_clear_first,
            should_normalize=should_normalize,
        )
        self._add_requests(request)

    def load_synthdefs(
        self,
        path: PathLike,
        on_completion: Callable[["Context"], Any] | None = None,
    ) -> Completion:
        """
        Load SynthDefs from a path.

        Emit ``/d_load`` requests.

        .. warning::

            At the time of this writing, supernova does not support globbing.

        :param path: The file path to load from. Globbing characters (e.g. ``*``) are
            permitted.
        :param on_completion: A callable with the buffer's context as the only argument.
            Permits building an "on completion" argument to this method's request
            without an active moment.
        """
        self._validate_can_request()
        request = LoadSynthDefs(path=path)
        return self._add_request_with_completion(request, on_completion)

    def load_synthdefs_directory(
        self,
        path: PathLike,
        on_completion: Callable[["Context"], Any] | None = None,
    ) -> Completion:
        """
        Load all SynthDefs from a directory.

        Emit ``/d_loadDir`` requests.

        :param path: The directory path to load from.
        :param on_completion: A callable with the buffer's context as the only argument.
            Permits building an "on completion" argument to this method's request
            without an active moment.
        """
        self._validate_can_request()
        request = LoadSynthDefDirectory(path=path)
        return self._add_request_with_completion(request, on_completion)

    def map_node(self, node: Node, **settings: Bus | str | None) -> None:
        """
        Map a node's controls to buses.

        Emit ``/n_map`` and ``/n_mapa`` requests.

        :param node: The node whose controls will be mapped.
        :param settings: A mapping of control names to buses (or to ``None`` to unmap
            the control).
        """
        self._validate_can_request()
        control, audio = {}, {}
        for key, value in settings.items():
            if isinstance(value, Bus):
                if value.calculation_rate is CalculationRate.AUDIO:
                    audio[key] = int(value)
                else:
                    control[key] = int(value)
            elif isinstance(value, str):
                if (match := BUS_PATTERN.match(value)) is None:
                    raise ValueError(value)
                rate, index = match.groups()
                if rate == "a":
                    audio[key] = int(index)
                else:
                    control[key] = int(index)
            elif value is None:
                control[key] = -1
        requests: list[Request] = []
        if control:
            requests.append(
                MapControlBusToNode(node_id=node, items=sorted(control.items()))
            )
        if audio:
            requests.append(
                MapAudioBusToNode(node_id=node, items=sorted(audio.items()))
            )
        self._add_requests(*requests)

    # TODO: map_node_range

    def move_node(
        self, node: Node, add_action: AddActionLike, target_node: Node
    ) -> None:
        """
        Move a node.

        Emit ``/n_after``, ``/n_before``, ``/g_head`` and ``/g_tail`` requests depending
        on parameters.

        :param node: The node to move.
        :param add_action: The :term:`add action` to use when moving the node.
        :param target_node: The target node to place the node relative to.
        """
        self._validate_can_request()
        add_action_ = AddAction.from_expr(add_action)
        items = [(node, target_node)]
        if add_action_ is AddAction.ADD_BEFORE:
            request: Request = MoveNodeBefore(items)
        elif add_action_ is AddAction.ADD_AFTER:
            request = MoveNodeAfter(items)
        elif add_action_ is AddAction.ADD_TO_TAIL:
            request = MoveNodeToGroupTail(items)
        elif add_action_ is AddAction.ADD_TO_HEAD:
            request = MoveNodeToGroupHead(items)
        else:
            raise ValueError
        self._add_requests(request)

    def normalize_buffer(
        self, buffer: Buffer, new_maximum: float = 1.0, as_wavetable: bool = False
    ) -> None:
        """
        Normalize a buffer.

        Emit ``/b_gen <buffer.id_> (w)?normalize`` requests depending on parameters.

        :param buffer: The buffer to normalize.
        :param new_maximum: The new maximum to normalize to.
        :param as_wavetable: Flag for treating the buffer contents as a wavetable.
        """
        self._validate_can_request()
        request = NormalizeBuffer(
            buffer_id=buffer.id_, new_maximum=new_maximum, as_wavetable=as_wavetable
        )
        self._add_requests(request)

    def order_nodes(
        self, target_node: Node, *nodes: Node, add_action: AddActionLike = None
    ) -> None:
        """
        Re-order nodes.

        Emit ``/n_order`` requests.

        :param target_node: The node to re-order the other nodes relative to.
        :param nodes: The nodes to re-order.
        :param add_action: The :term:`add action` to use when re-ordering the nodes.
        """
        self._validate_can_request()
        request = OrderNodes(
            add_action=add_action, target_node_id=target_node, node_ids=nodes
        )
        self._add_requests(request)

    def pause_node(self, node: Node) -> None:
        """
        Pause a node.

        Emit ``/n_run <node.id_> 0`` requests.

        :param node: The node to pause.
        """
        self._validate_can_request()
        request = RunNode(items=[(node, False)])
        self._add_requests(request)

    def read_buffer(
        self,
        buffer: Buffer,
        file_path: PathLike,
        *,
        buffer_starting_frame: int | None = None,
        channel_indices: list[int] | None = None,
        frame_count: int | None = None,
        leave_open: bool = False,
        starting_frame: int | None = None,
        on_completion: Callable[["Context"], Any] | None = None,
    ) -> Completion:
        """
        Read a file into a buffer.

        Emit ``/b_read`` or ``/b_readChannel`` requests, depending on parameters.

        :param buffer: The buffer to read into.
        :param file_path: The file path to read from.
        :param channel_indices: A list of channel indices to read from when reading from
            a file.
        :param frame_count: The number of frames to read.
        :param leave_open: Flag for leaving the file open (e.g. to continue reading via
            :py:class:`~supriya.ugens.diskio.DiskIn`) or close it.
        :param starting_frame: The starting frame in the buffer to begin reading into
            at.
        :param on_completion: A callable with the buffer's context as the only argument.
            Permits building an "on completion" argument to this method's request
            without an active moment.
        """
        self._validate_can_request()
        frame_count_ = frame_count or 0
        if channel_indices:
            request: Request = ReadBufferChannel(
                buffer_id=buffer.id_,
                path=file_path,
                frame_count=frame_count_ or -1,
                leave_open=leave_open,
                starting_frame_in_buffer=buffer_starting_frame or 0,
                starting_frame_in_file=starting_frame or 0,
                channel_indices=channel_indices,
            )
        else:
            request = ReadBuffer(
                buffer_id=buffer.id_,
                path=file_path,
                frame_count=frame_count_ or -1,
                leave_open=leave_open,
                starting_frame_in_buffer=buffer_starting_frame or 0,
                starting_frame_in_file=starting_frame or 0,
            )
        return self._add_request_with_completion(request, on_completion)

    @abc.abstractmethod
    def send(self, message: SequenceABC | SupportsOsc | str) -> None:
        """
        Send a message to the execution context.

        :param message: The message to send.
        """
        raise NotImplementedError

    def set_buffer(self, buffer: Buffer, index: int, value: float) -> None:
        """
        set a buffer sample.

        Emit ``/b_set`` requests.

        :param buffer: The buffer to modify.
        :param index: The sample index to write at.
        :param value: The value to write.
        """
        self._validate_can_request()
        request = SetBuffer(buffer_id=buffer, items=[(index, value)])
        self._add_requests(request)

    def set_buffer_range(
        self, buffer: Buffer, index: int, values: Sequence[float]
    ) -> None:
        """
        set a buffer sample range.

        Emit ``/b_setn`` requests.

        :param buffer: The buffer to modify.
        :param index: The sample index to start writing at.
        :param values: The values to write.
        """
        self._validate_can_request()
        request = SetBufferRange(buffer_id=buffer, items=[(index, values)])
        self._add_requests(request)

    def set_bus(self, bus: Bus, value: float, use_shared_memory: bool = False) -> None:
        """
        set a control bus to a value.

        Emit ``/c_set`` requests.

        :param bus: The control bus to set.
        :param value: The value to set the control bus to.
        :param use_shared_memory: If true, use the shared memory interface.
            Skip bundling the request in any open moment.
        """
        self._validate_can_request()
        if bus.calculation_rate != CalculationRate.CONTROL:
            raise InvalidCalculationRate
        if use_shared_memory and (shared_memory := getattr(self, "_shared_memory")):
            shared_memory[int(bus)] = value
            return
        request = SetControlBus(items=[(int(bus), value)])
        self._add_requests(request)

    def set_bus_range(
        self, bus: Bus, values: Sequence[float], use_shared_memory: bool = False
    ) -> None:
        """
        set a range of control buses.

        Emit ``/c_setn`` requests.

        :param bus: The bus to start writing at.
        :param values: The values to write.
        :param use_shared_memory: If true, use the shared memory interface.
            Skip bundling the request in any open moment.
        """
        self._validate_can_request()
        if bus.calculation_rate != CalculationRate.CONTROL:
            raise InvalidCalculationRate
        if use_shared_memory and (shared_memory := getattr(self, "_shared_memory")):
            shared_memory[int(bus) : int(bus) + len(values)] = values
            return
        request = SetControlBusRange(items=[(int(bus), values)])
        self._add_requests(request)

    def set_node(
        self,
        node: Node,
        *indexed_settings: tuple[int, SupportsFloat | Sequence[SupportsFloat]],
        **settings: SupportsFloat | Sequence[SupportsFloat],
    ) -> None:
        """
        set a node's controls.

        Emit ``/n_set`` requests.

        :param node: The node whose controls will be set.
        :param indexed_settings: A sequence of control indices to values.
        :param settings: A mapping of control names to values.
        """
        self._validate_can_request()
        coerced_settings: dict[int | str, float | Sequence[float]] = {}
        for index, values in sorted(indexed_settings):
            if isinstance(values, Sequence):
                coerced_settings[index] = [float(value) for value in values]
            else:
                coerced_settings[index] = float(values)
        for key, values in sorted(settings.items()):
            if isinstance(values, Sequence):
                coerced_settings[key] = [float(value) for value in values]
            else:
                coerced_settings[key] = float(values)
        request = SetNodeControl(node_id=node.id_, items=list(coerced_settings.items()))
        self._add_requests(request)

    def set_node_range(
        self,
        node: Node,
        *indexed_settings: tuple[int, Sequence[SupportsFloat]],
        **settings: Sequence[SupportsFloat],
    ) -> None:
        """
        set a range of node controls.

        Emit ``/n_setn`` requests.

        :param node: The node whose controls will be set.
        :param indexed_settings: A sequence of control indices to values.
        :param settings: A mapping of control names to values.
        """
        self._validate_can_request()
        coerced_settings: dict[int | str, Sequence[float]] = {}
        for index, values in sorted(indexed_settings):
            coerced_settings[index] = [float(value) for value in values]
        for key, values in sorted(settings.items()):
            coerced_settings[key] = [float(value) for value in values]
        request = SetNodeControlRange(
            node_id=node.id_, items=list(coerced_settings.items())
        )
        self._add_requests(request)

    def unpause_node(self, node: Node) -> None:
        """
        Unpause a node.

        Emit ``/n_run <node.id_> 1`` requests.

        :param node: The node to unpause.
        """
        self._validate_can_request()
        request = RunNode(items=[(node, True)])
        self._add_requests(request)

    def write_buffer(
        self,
        buffer: Buffer,
        file_path: PathLike,
        *,
        frame_count: int | None = None,
        header_format: HeaderFormatLike = "aiff",
        leave_open: bool = False,
        sample_format: SampleFormatLike = "int24",
        starting_frame: int | None = None,
        on_completion: Callable[["Context"], Any] | None = None,
    ) -> Completion:
        """
        Write a buffer to disk.

        Emit ``/b_write`` requests.

        :param buffer: The buffer to write to disk.
        :param file_path: The file path to write into.
        :param frame_count: The number of frames to write.
        :param header_format: The header format to use, e.g. ``AIFF`` or ``WAVE``.
        :param leave_open: Flag for leaving the file open (e.g. to continue writing via
            :py:class:`~supriya.ugens.diskio.DiskOut`) or close it.
        :param sample_format: The sample format to use, e.g. ``INT24`` or ``FLOAT``.
        :param starting_frame: The starting frame in the buffer to start writing from.
        :param on_completion: A callable with the buffer's context as the only argument.
            Permits building an "on completion" argument to this method's request
            without an active moment.
        """
        self._validate_can_request()
        request = WriteBuffer(
            buffer_id=buffer.id_,
            path=file_path,
            frame_count=frame_count if frame_count is not None else -1,
            header_format=header_format,
            leave_open=leave_open,
            sample_format=sample_format,
            starting_frame=starting_frame or 0,
        )
        return self._add_request_with_completion(request, on_completion)

    def zero_buffer(
        self,
        buffer: Buffer,
        on_completion: Callable[["Context"], Any] | None = None,
    ) -> Completion:
        """
        set a buffer's contents to zero.

        Emit ``/b_zero`` requests.

        :param buffer: The buffer to zero.
        :param on_completion: A callable with the buffer's context as the only argument.
            Permits building an "on completion" argument to this method's request
            without an active moment.
        """
        self._validate_can_request()
        request = ZeroBuffer(buffer_id=buffer)
        return self._add_request_with_completion(request, on_completion)

    ### PUBLIC PROPERTIES ###

    @property
    def audio_input_bus_group(self) -> BusGroup:
        """
        Get the context's audio output buses.
        """
        return BusGroup(
            context=self,
            id_=self.options.output_bus_channel_count,
            calculation_rate=cast(CalculationRate, CalculationRate.AUDIO),
            count=self.options.input_bus_channel_count,
        )

    @property
    def audio_output_bus_group(self) -> BusGroup:
        """
        Get the context's audio input buses.
        """
        return BusGroup(
            context=self,
            id_=0,
            calculation_rate=cast(CalculationRate, CalculationRate.AUDIO),
            count=self.options.output_bus_channel_count,
        )

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
        return self.root_node

    @property
    def client_id(self) -> int:
        """
        Get the context's client ID.
        """
        return self._client_id

    @property
    def latency(self) -> float:
        """
        Get the context's latency.
        """
        return self._latency

    @property
    def name(self) -> str | None:
        """
        Get the context's optional name.
        """
        return self._name

    @property
    def options(self) -> Options:
        """
        Get the context's scsynth options.
        """
        return self._options

    @property
    def root_node(self) -> RootNode:
        """
        Get the context's root node.
        """
        return RootNode(context=self, id_=0)
