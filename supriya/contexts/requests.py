"""
Classes for modeling requests to :term:`scsynth`.
"""

import asyncio
import dataclasses
import logging
from abc import ABC, abstractmethod
from concurrent.futures import Future
from os import PathLike
from typing import (
    TYPE_CHECKING,
    Literal,
    Sequence,
    SupportsInt,
)

from uqbar.objects import new

from ..enums import AddAction, HeaderFormat, RequestName, SampleFormat
from ..osc import OscArgument, OscBundle, OscMessage
from ..typing import AddActionLike, HeaderFormatLike, SampleFormatLike, SupportsOsc
from ..ugens import SynthDef, compile_synthdefs
from .responses import Response

if TYPE_CHECKING:
    import supriya.contexts.realtime

    from .core import Context


logger = logging.getLogger(__name__)


class Requestable(ABC):
    """
    Abstract base for request-like classes.
    """

    ### PRIVATE METHODS ###

    @abstractmethod
    def _get_response_patterns_and_requestable(
        self, context: "Context"
    ) -> tuple[
        Sequence[float | str] | None,
        Sequence[float | str] | None,
        "Requestable",
    ]:
        raise NotImplementedError

    ### PUBLIC METHODS ###

    def communicate(
        self, server: "supriya.contexts.realtime.Server", timeout: float = 1.0
    ) -> Response | None:
        (
            success_pattern,
            failure_pattern,
            requestable,
        ) = self._get_response_patterns_and_requestable(server)
        if not success_pattern:
            server.send(self)
            return None
        future: Future[Response] = Future()
        server._osc_protocol.register(
            pattern=success_pattern,
            failure_pattern=failure_pattern,
            procedure=lambda message: future.set_result(Response.from_osc(message)),
            once=True,
        )
        server.send(requestable)
        return future.result(timeout=timeout)

    async def communicate_async(
        self, server: "supriya.contexts.realtime.AsyncServer", timeout: float = 1.0
    ) -> Response | None:
        (
            success_pattern,
            failure_pattern,
            requestable,
        ) = self._get_response_patterns_and_requestable(server)
        if not success_pattern:
            server.send(self)
            return None
        future: asyncio.Future[Response] = asyncio.get_running_loop().create_future()
        osc_callback = server._osc_protocol.register(
            pattern=success_pattern,
            failure_pattern=failure_pattern,
            procedure=lambda message: future.set_result(Response.from_osc(message)),
            once=True,
        )
        server.send(requestable)
        try:
            await asyncio.wait_for(future, timeout=timeout)
        except asyncio.TimeoutError:
            # No response received, so make sure to cleanup
            server._osc_protocol.unregister(osc_callback)
            raise
        return future.result()

    @abstractmethod
    def to_osc(self) -> OscBundle | OscMessage:
        raise NotImplementedError


@dataclasses.dataclass
class Request(Requestable):
    """
    Abstract base for request classes.
    """

    ### PRIVATE METHODS ###

    def _get_response_patterns(
        self,
    ) -> tuple[Sequence[float | str] | None, Sequence[float | str] | None]:
        return None, None

    def _get_response_patterns_and_requestable(
        self, context: "Context"
    ) -> tuple[
        Sequence[float | str] | None,
        Sequence[float | str] | None,
        "Requestable",
    ]:
        success_pattern, failure_pattern = self._get_response_patterns()
        return success_pattern, failure_pattern, self

    ### PUBLIC METHODS ###

    @classmethod
    def merge(cls, requests: list["Request"]) -> list["Request"]:
        return requests


@dataclasses.dataclass
class RequestBundle(Requestable):
    """
    A bundle of requestables to be executed at a timestamp.
    """

    contents: Sequence[Requestable]
    timestamp: float | None = None

    ### PRIVATE METHODS ###

    def _get_response_patterns_and_requestable(
        self, context: "Context"
    ) -> tuple[
        Sequence[float | str] | None,
        Sequence[float | str] | None,
        "Requestable",
    ]:
        sync_id = context._get_next_sync_id()
        request_bundle: "RequestBundle" = new(
            self, contents=list(self.contents) + [Sync(sync_id=sync_id)]
        )
        response_pattern: list[float | str] = ["/synced", sync_id]
        return response_pattern, None, request_bundle

    ### PUBLIC METHODS ###

    def to_osc(self) -> OscBundle:
        return OscBundle(
            contents=[x.to_osc() for x in self.contents], timestamp=self.timestamp
        )


@dataclasses.dataclass
class AllocateBuffer(Request):
    """
    A ``/b_alloc`` request.

    ::

        >>> from supriya.contexts.requests import AllocateBuffer, NormalizeBuffer
        >>> request = AllocateBuffer(
        ...     buffer_id=1,
        ...     frame_count=512,
        ...     channel_count=1,
        ...     on_completion=NormalizeBuffer(buffer_id=1),
        ... )
        >>> request.to_osc()
        OscMessage('/b_alloc', 1, 512, 1, OscMessage('/b_gen', 1, 'normalize', 1.0))
    """

    buffer_id: SupportsInt
    frame_count: int
    channel_count: int = 1
    on_completion: SupportsOsc | None = None

    def _get_response_patterns(
        self,
    ) -> tuple[Sequence[float | str] | None, Sequence[float | str] | None]:
        return ["/done", "/b_alloc", int(self.buffer_id)], None

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = [
            int(self.buffer_id),
            int(self.frame_count),
            int(self.channel_count),
        ]
        if self.on_completion:
            contents.append(self.on_completion.to_osc())
        return OscMessage(RequestName.BUFFER_ALLOCATE, *contents)


@dataclasses.dataclass
class AllocateReadBuffer(Request):
    """
    A ``/b_allocRead`` request.

    ::

        >>> from supriya.contexts.requests import AllocateReadBuffer, NormalizeBuffer
        >>> request = AllocateReadBuffer(
        ...     buffer_id=1,
        ...     path="path/to/audio.wav",
        ...     starting_frame=32,
        ...     frame_count=512,
        ...     on_completion=NormalizeBuffer(buffer_id=1),
        ... )
        >>> request.to_osc()
        OscMessage('/b_allocRead', 1, 'path/to/audio.wav', 32, 512, OscMessage('/b_gen', 1, 'normalize', 1.0))
    """

    buffer_id: SupportsInt
    path: PathLike
    starting_frame: int = 0
    frame_count: int = 0
    on_completion: SupportsOsc | None = None

    def _get_response_patterns(
        self,
    ) -> tuple[Sequence[float | str] | None, Sequence[float | str] | None]:
        return ["/done", "/b_allocRead", int(self.buffer_id)], None

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = [
            int(self.buffer_id),
            str(self.path),
            int(self.starting_frame),
            int(self.frame_count),
        ]
        if self.on_completion:
            contents.append(self.on_completion.to_osc())
        return OscMessage(RequestName.BUFFER_ALLOCATE_READ, *contents)


@dataclasses.dataclass
class AllocateReadBufferChannel(Request):
    """
    A ``/b_allocReadChannel`` request.

    ::

        >>> from supriya.contexts.requests import AllocateReadBufferChannel, NormalizeBuffer
        >>> request = AllocateReadBufferChannel(
        ...     buffer_id=1,
        ...     path="path/to/audio.wav",
        ...     channel_indices=[1, 2],
        ...     starting_frame=32,
        ...     frame_count=512,
        ...     on_completion=NormalizeBuffer(buffer_id=1),
        ... )
        >>> request.to_osc()
        OscMessage('/b_allocReadChannel', 1, 'path/to/audio.wav', 32, 512, 1, 2, OscMessage('/b_gen', 1, 'normalize', 1.0))
    """

    buffer_id: SupportsInt
    path: PathLike
    channel_indices: Sequence[int]
    starting_frame: int = 0
    frame_count: int = 0
    on_completion: SupportsOsc | None = None

    def _get_response_patterns(
        self,
    ) -> tuple[Sequence[float | str] | None, Sequence[float | str] | None]:
        return ["/done", "/b_allocReadChannel", int(self.buffer_id)], None

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = [
            int(self.buffer_id),
            str(self.path),
            int(self.starting_frame),
            int(self.frame_count),
            *(int(channel_index) for channel_index in self.channel_indices),
        ]
        if self.on_completion:
            contents.append(self.on_completion.to_osc())
        return OscMessage(RequestName.BUFFER_ALLOCATE_READ_CHANNEL, *contents)


@dataclasses.dataclass
class AutoReassignSynthID(Request):
    """
    A ``/s_noid`` request.

    ::

        >>> from supriya.contexts.requests import AutoReassignSynthID
        >>> request = AutoReassignSynthID(synth_ids=[1, 2, 3])
        >>> request.to_osc()
        OscMessage('/s_noid', 1, 2, 3)
    """

    synth_ids: Sequence[SupportsInt]

    def to_osc(self) -> OscMessage:
        return OscMessage(
            RequestName.SYNTH_NOID, *(int(synth_id) for synth_id in self.synth_ids)
        )


@dataclasses.dataclass
class ClearSchedule(Request):
    """
    A ``/clearSched`` request.

    ::

        >>> from supriya.contexts.requests import ClearSchedule
        >>> request = ClearSchedule()
        >>> request.to_osc()
        OscMessage('/clearSched')
    """

    def to_osc(self) -> OscMessage:
        return OscMessage(RequestName.CLEAR_SCHEDULE)


@dataclasses.dataclass
class CloseBuffer(Request):
    """
    A ``/b_close`` request.

    ::

        >>> from supriya.contexts.requests import CloseBuffer, FreeNode
        >>> request = CloseBuffer(buffer_id=1, on_completion=FreeNode(node_ids=[1]))
        >>> request.to_osc()
        OscMessage('/b_close', 1, OscMessage('/n_free', 1))
    """

    buffer_id: SupportsInt
    on_completion: Requestable | None = None

    def _get_response_patterns(
        self,
    ) -> tuple[Sequence[float | str] | None, Sequence[float | str] | None]:
        return ["/done", "/b_close", int(self.buffer_id)], None

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = [int(self.buffer_id)]
        if self.on_completion:
            contents.append(self.on_completion.to_osc())
        return OscMessage(RequestName.BUFFER_CLOSE, *contents)


@dataclasses.dataclass
class CopyBuffer(Request):
    """
    A ``/b_gen`` ``copy`` request.

    ::

        >>> from supriya.contexts.requests import CopyBuffer
        >>> request = CopyBuffer(
        ...     source_buffer_id=1,
        ...     target_buffer_id=2,
        ...     frame_count=512,
        ...     source_starting_frame=0,
        ...     target_starting_frame=128,
        ... )
        >>> request.to_osc()
        OscMessage('/b_gen', 2, 'copy', 128, 1, 0, 512)
    """

    source_buffer_id: SupportsInt
    target_buffer_id: SupportsInt
    frame_count: int = -1
    source_starting_frame: int = 0
    target_starting_frame: int = 0

    def _get_response_patterns(
        self,
    ) -> tuple[Sequence[float | str] | None, Sequence[float | str] | None]:
        return ["/done", "/b_gen", int(self.target_buffer_id)], None

    def to_osc(self) -> OscMessage:
        return OscMessage(
            RequestName.BUFFER_GENERATE,
            int(self.target_buffer_id),
            "copy",
            int(self.target_starting_frame),
            int(self.source_buffer_id),
            int(self.source_starting_frame),
            int(self.frame_count),
        )


@dataclasses.dataclass
class DoNothing(Request):
    """
    A "nothing" request.

    ::

        >>> from supriya.contexts.requests import DoNothing
        >>> request = DoNothing()
        >>> request.to_osc()
        OscMessage(0)
    """

    def to_osc(self) -> OscMessage:
        return OscMessage(0)


@dataclasses.dataclass
class DumpOsc(Request):
    """
    A ``/dumpOSC`` request.

    ::

        >>> from supriya.contexts.requests import DumpOsc
        >>> request = DumpOsc(True)
        >>> request.to_osc()
        OscMessage('/dumpOSC', 1)
    """

    code: int

    def to_osc(self) -> OscMessage:
        return OscMessage(RequestName.DUMP_OSC, int(self.code))


@dataclasses.dataclass
class DumpTree(Request):
    """
    A ``/g_dumpTree`` request.

    ::

        >>> from supriya.contexts.requests import DumpTree
        >>> request = DumpTree(items=[(0, True)])
        >>> request.to_osc()
        OscMessage('/g_dumpTree', 0, 1)
    """

    items: Sequence[tuple[SupportsInt, bool]]

    def to_osc(self) -> OscMessage:
        contents = []
        for node_id, flag in self.items:
            contents.extend([int(node_id), int(flag)])
        return OscMessage(RequestName.GROUP_DUMP_TREE, *contents)


@dataclasses.dataclass
class FillBuffer(Request):
    """
    A ``/b_fill`` request.

    ::

        >>> from supriya.contexts.requests import FillBuffer
        >>> request = FillBuffer(
        ...     buffer_id=1,
        ...     items=[(32, 64, 0.5)],
        ... )
        >>> request.to_osc()
        OscMessage('/b_fill', 1, 32, 64, 0.5)
    """

    buffer_id: SupportsInt
    items: Sequence[tuple[int, int, float]]

    @classmethod
    def merge(cls, requests: list["Request"]) -> list["Request"]:
        items_by_buffer_id: dict[int, list[tuple[int, int, float]]] = {}
        for request in requests:
            if isinstance(request, cls):
                items_by_buffer_id.setdefault(int(request.buffer_id), []).extend(
                    request.items
                )
        return [
            cls(buffer_id=buffer_id, items=items)
            for buffer_id, items in sorted(items_by_buffer_id.items())
        ]

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = [int(self.buffer_id)]
        for index, count, value in self.items:
            contents.extend([int(index), int(count), float(value)])
        return OscMessage(RequestName.BUFFER_FILL, *contents)


@dataclasses.dataclass
class FillControlBusRange(Request):
    """
    A ``/c_fill`` request.

    ::

        >>> from supriya.contexts.requests import FillControlBusRange
        >>> request = FillControlBusRange(
        ...     items=[(4, 12, 0.25), (32, 4, 440.0)],
        ... )
        >>> request.to_osc()
        OscMessage('/c_fill', 4, 12, 0.25, 32, 4, 440.0)
    """

    items: Sequence[tuple[SupportsInt, int, float]]

    @classmethod
    def merge(cls, requests: list["Request"]) -> list["Request"]:
        items: list[tuple[SupportsInt, int, float]] = []
        for request in requests:
            if not isinstance(request, cls):
                continue
            items.extend(request.items)
        return [cls(items=items)]

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = []
        for index, count, value in self.items:
            contents.extend([int(index), int(count), float(value)])
        return OscMessage(RequestName.CONTROL_BUS_FILL, *contents)


@dataclasses.dataclass
class FillNode(Request):
    """
    A ``/n_fill`` request.

    ::

        >>> from supriya.contexts.requests import FillNode
        >>> request = FillNode(
        ...     node_id=1000,
        ...     items=[("frequency", 7, 432.0)]
        ... )
        >>> request.to_osc()
        OscMessage('/n_fill', 1000, 'frequency', 7, 432.0)
    """

    node_id: SupportsInt
    items: Sequence[tuple[int | str, int, float]]

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = [int(self.node_id)]
        for control, count, value in self.items:
            contents.extend(
                [
                    control if isinstance(control, str) else int(control),
                    int(count),
                    float(value),
                ]
            )
        return OscMessage(RequestName.NODE_FILL, *contents)


@dataclasses.dataclass
class FreeAllSynthDefs(Request):
    """
    A ``/d_freeAll`` request.

    ::

        >>> from supriya.contexts.requests import FreeAllSynthDefs
        >>> request = FreeAllSynthDefs()
        >>> request.to_osc()
        OscMessage('/d_freeAll')
    """

    def to_osc(self) -> OscMessage:
        return OscMessage(RequestName.SYNTHDEF_FREE_ALL)


@dataclasses.dataclass
class FreeBuffer(Request):
    """
    A ``/b_free`` request.

    ::

        >>> from supriya.contexts.requests import FreeBuffer, FreeNode
        >>> request = FreeBuffer(
        ...     buffer_id=1,
        ...     on_completion=FreeNode(node_ids=[1000]),
        ... )
        >>> request.to_osc()
        OscMessage('/b_free', 1, OscMessage('/n_free', 1000))
    """

    buffer_id: SupportsInt
    on_completion: Requestable | None = None

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = [int(self.buffer_id)]
        if self.on_completion:
            contents.append(self.on_completion.to_osc())
        return OscMessage(RequestName.BUFFER_FREE, *contents)


@dataclasses.dataclass
class FreeGroupChildren(Request):
    """
    A ``/g_freeAll`` request.

    ::

        >>> from supriya.contexts.requests import FreeGroupChildren
        >>> request = FreeGroupChildren(node_ids=[1])
        >>> request.to_osc()
        OscMessage('/g_freeAll', 1)
    """

    node_ids: Sequence[SupportsInt]

    def to_osc(self) -> OscMessage:
        return OscMessage(
            RequestName.GROUP_FREE_ALL, *(int(node_id) for node_id in self.node_ids)
        )


@dataclasses.dataclass
class FreeGroupDeep(Request):
    """
    A ``/g_deepFree`` request.

    ::

        >>> from supriya.contexts.requests import FreeGroupDeep
        >>> request = FreeGroupDeep(node_ids=[1])
        >>> request.to_osc()
        OscMessage('/g_deepFree', 1)
    """

    node_ids: Sequence[SupportsInt]

    def to_osc(self) -> OscMessage:
        return OscMessage(
            RequestName.GROUP_DEEP_FREE, *(int(node_id) for node_id in self.node_ids)
        )


@dataclasses.dataclass
class FreeNode(Request):
    """
    A ``/n_free`` request.

    ::

        >>> from supriya.contexts.requests import FreeNode
        >>> request = FreeNode(node_ids=[1000, 1001])
        >>> request.to_osc()
        OscMessage('/n_free', 1000, 1001)
    """

    node_ids: Sequence[SupportsInt]

    def _get_response_patterns(
        self,
    ) -> tuple[Sequence[float | str] | None, Sequence[float | str] | None]:
        return ["/n_end", int(self.node_ids[-1])], None

    def to_osc(self) -> OscMessage:
        return OscMessage(
            RequestName.NODE_FREE, *(int(node_id) for node_id in self.node_ids)
        )


@dataclasses.dataclass
class FreeSynthDef(Request):
    """
    A ``/d_free`` request.

    ::

        >>> from supriya.contexts.requests import FreeSynthDef
        >>> request = FreeSynthDef(synthdefs=["supriya:default"])
        >>> request.to_osc()
        OscMessage('/d_free', 'supriya:default')
    """

    synthdefs: Sequence[SynthDef | str]

    def to_osc(self) -> OscMessage:
        contents = []
        for x in self.synthdefs:
            if isinstance(x, SynthDef):
                contents.append(x.effective_name)
            else:
                contents.append(x)
        return OscMessage(RequestName.SYNTHDEF_FREE, *contents)


@dataclasses.dataclass
class GenerateBuffer(Request):
    """
    A ``/b_gen`` request, for use with ``sine1``, ``sine2``, ``sine3`` and ``cheby`` commands.

    ::

        >>> from supriya.contexts.requests import GenerateBuffer
        >>> request = GenerateBuffer(
        ...     buffer_id=1,
        ...     command_name="sine3",
        ...     amplitudes=[1, 2, 3],
        ...     frequencies=[4, 5, 6],
        ...     phases=[0.25, 0.5, 0.75],
        ...     should_normalize=True,
        ... )
        >>> request.to_osc()
        OscMessage('/b_gen', 1, 'sine3', 1, 4.0, 1.0, 0.25, 5.0, 2.0, 0.5, 6.0, 3.0, 0.75)
    """

    buffer_id: SupportsInt
    command_name: Literal["sine1", "sine2", "sine3", "cheby"]
    amplitudes: Sequence[float]
    frequencies: Sequence[float] | None
    phases: Sequence[float] | None
    as_wavetable: bool = False
    should_clear_first: bool = False
    should_normalize: bool = False

    def _get_response_patterns(
        self,
    ) -> tuple[Sequence[float | str] | None, Sequence[float | str] | None]:
        return ["/done", "/b_gen", int(self.buffer_id)], None

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = [
            int(self.buffer_id),
            self.command_name,
            (
                self.should_normalize
                | (self.as_wavetable * 2)
                | (self.should_clear_first * 4)
            ),
        ]
        sequences = []
        if self.frequencies:
            sequences.append(self.frequencies)
        sequences.append(self.amplitudes)
        if self.phases:
            sequences.append(self.phases)
        for values in zip(*sequences):
            for value in values:
                contents.append(float(value))
        return OscMessage(RequestName.BUFFER_GENERATE, *contents)


@dataclasses.dataclass
class GetBuffer(Request):
    """
    A ``/b_get`` request.

    ::

        >>> from supriya.contexts.requests import GetBuffer
        >>> request = GetBuffer(
        ...     buffer_id=1,
        ...     indices=[0, 4, 8],
        ... )
        >>> request.to_osc()
        OscMessage('/b_get', 1, 0, 4, 8)
    """

    buffer_id: SupportsInt
    indices: Sequence[int]

    def _get_response_patterns(
        self,
    ) -> tuple[Sequence[float | str] | None, Sequence[float | str] | None]:
        return ["/b_set", int(self.buffer_id)], None

    def to_osc(self) -> OscMessage:
        return OscMessage(
            RequestName.BUFFER_GET,
            int(self.buffer_id),
            *(int(index) for index in self.indices),
        )


@dataclasses.dataclass
class GetBufferRange(Request):
    """
    A ``/b_getn`` request.

    ::

        >>> from supriya.contexts.requests import GetBufferRange
        >>> request = GetBufferRange(
        ...     buffer_id=1,
        ...     items=[(0, 4), (32, 8)],
        ... )
        >>> request.to_osc()
        OscMessage('/b_getn', 1, 0, 4, 32, 8)
    """

    buffer_id: SupportsInt
    items: Sequence[tuple[int, int]]

    def _get_response_patterns(
        self,
    ) -> tuple[Sequence[float | str] | None, Sequence[float | str] | None]:
        return ["/b_setn", int(self.buffer_id)], None

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = [int(self.buffer_id)]
        for index, count in self.items:
            contents.extend([int(index), int(count)])
        return OscMessage(RequestName.BUFFER_GET_CONTIGUOUS, *contents)


@dataclasses.dataclass
class GetControlBus(Request):
    """
    A ``/c_get`` request.

    ::

        >>> from supriya.contexts.requests import GetControlBus
        >>> request = GetControlBus(bus_ids=[1, 2, 3])
        >>> request.to_osc()
        OscMessage('/c_get', 1, 2, 3)
    """

    bus_ids: Sequence[SupportsInt]

    def _get_response_patterns(
        self,
    ) -> tuple[Sequence[float | str] | None, Sequence[float | str] | None]:
        return ["/c_set", int(self.bus_ids[0])], None

    def to_osc(self) -> OscMessage:
        return OscMessage(
            RequestName.CONTROL_BUS_GET, *(int(bus_id) for bus_id in self.bus_ids)
        )


@dataclasses.dataclass
class GetControlBusRange(Request):
    """
    A ``/c_getn`` request.

    ::

        >>> from supriya.contexts.requests import GetControlBusRange
        >>> request = GetControlBusRange(items=[(0, 4), (8, 16)])
        >>> request.to_osc()
        OscMessage('/c_getn', 0, 4, 8, 16)
    """

    items: Sequence[tuple[SupportsInt, int]]

    def _get_response_patterns(
        self,
    ) -> tuple[Sequence[float | str] | None, Sequence[float | str] | None]:
        return ["/c_setn", int(self.items[0][0])], None

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = []
        for index, count in self.items:
            contents.extend([int(index), int(count)])
        return OscMessage(RequestName.CONTROL_BUS_GET_CONTIGUOUS, *contents)


@dataclasses.dataclass
class GetSynthControl(Request):
    """
    A ``/s_get`` request.

    ::

        >>> from supriya.contexts.requests import GetSynthControl
        >>> request = GetSynthControl(
        ...     synth_id=1000,
        ...     controls=["frequency", "amplitude"],
        ... )
        >>> request.to_osc()
        OscMessage('/s_get', 1000, 'frequency', 'amplitude')
    """

    synth_id: SupportsInt
    controls: Sequence[int | str]

    def _get_response_patterns(
        self,
    ) -> tuple[Sequence[float | str] | None, Sequence[float | str] | None]:
        return ["/n_set", int(self.synth_id)], None

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = [int(self.synth_id)]
        for control in self.controls:
            contents.append(control if isinstance(control, str) else int(control))
        return OscMessage(RequestName.SYNTH_GET, *contents)


@dataclasses.dataclass
class GetSynthControlRange(Request):
    """
    A ``/s_getn`` request.

    ::

        >>> from supriya.contexts.requests import GetSynthControlRange
        >>> request = GetSynthControlRange(
        ...     synth_id=1000,
        ...     items=[("frequency", 8)],
        ... )
        >>> request.to_osc()
        OscMessage('/s_getn', 1000, 'frequency', 8)
    """

    synth_id: SupportsInt
    items: Sequence[tuple[int | str, int]]

    def _get_response_patterns(
        self,
    ) -> tuple[Sequence[float | str] | None, Sequence[float | str] | None]:
        return ["/n_setn", int(self.synth_id), self.items[0][0]], None

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = [int(self.synth_id)]
        for control, count in self.items:
            contents.extend(
                [control if isinstance(control, str) else int(control), int(count)]
            )
        return OscMessage(RequestName.SYNTH_GET_CONTIGUOUS, *contents)


@dataclasses.dataclass
class LoadSynthDefs(Request):
    """
    A ``/d_load`` request.

    ::

        >>> from supriya.contexts.requests import LoadSynthDefs, NewGroup
        >>> request = LoadSynthDefs(
        ...     path="path/to/synthdef-*.scsyndef",
        ...     on_completion=NewGroup(items=[(1000, "add to tail", 1)]),
        ... )
        >>> request.to_osc()
        OscMessage('/d_load', 'path/to/synthdef-*.scsyndef', OscMessage('/g_new', 1000, 1, 1))
    """

    path: PathLike
    on_completion: Requestable | None = None

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = [str(self.path)]
        if self.on_completion:
            contents.append(self.on_completion.to_osc())
        return OscMessage(RequestName.SYNTHDEF_LOAD, *contents)


@dataclasses.dataclass
class LoadSynthDefDirectory(Request):
    """
    A ``/d_loadDir`` request.

    ::

        >>> from supriya.contexts.requests import LoadSynthDefDirectory, NewGroup
        >>> request = LoadSynthDefDirectory(
        ...     path="path/to/synthdefs/",
        ...     on_completion=NewGroup(items=[(1000, "add to tail", 1)]),
        ... )
        >>> request.to_osc()
        OscMessage('/d_loadDir', 'path/to/synthdefs/', OscMessage('/g_new', 1000, 1, 1))
    """

    path: PathLike
    on_completion: Requestable | None = None

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = [str(self.path)]
        if self.on_completion:
            contents.append(self.on_completion.to_osc())
        return OscMessage(RequestName.SYNTHDEF_LOAD_DIR, *contents)


@dataclasses.dataclass
class MapAudioBusToNode(Request):
    """
    A ``/n_mapa`` request.

    ::

        >>> from supriya.contexts.requests import MapAudioBusToNode
        >>> request = MapAudioBusToNode(
        ...     node_id=1000,
        ...     items=[("frequency", 0)],
        ... )
        >>> request.to_osc()
        OscMessage('/n_mapa', 1000, 'frequency', 0)
    """

    node_id: SupportsInt
    items: Sequence[tuple[int | str, SupportsInt]]

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = [int(self.node_id)]
        for index_or_name, bus_index in self.items:
            contents.extend(
                [
                    (
                        index_or_name
                        if isinstance(index_or_name, str)
                        else int(index_or_name)
                    ),
                    int(bus_index),
                ]
            )
        return OscMessage(RequestName.NODE_MAP_TO_AUDIO_BUS, *contents)


@dataclasses.dataclass
class MapAudioBusRangeToNode(Request):
    """
    A ``/n_mapan`` request.

    ::

        >>> from supriya.contexts.requests import MapAudioBusRangeToNode
        >>> request = MapAudioBusRangeToNode(
        ...     node_id=1000,
        ...     items=[("frequency", 0, 4)]
        ... )
        >>> request.to_osc()
        OscMessage('/n_mapan', 1000, 'frequency', 0, 4)
    """

    node_id: SupportsInt
    items: Sequence[tuple[int | str, SupportsInt, int]]

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = [int(self.node_id)]
        for index_or_name, bus_index, count in self.items:
            contents.extend(
                [
                    (
                        index_or_name
                        if isinstance(index_or_name, str)
                        else int(index_or_name)
                    ),
                    int(bus_index),
                    int(count),
                ]
            )
        return OscMessage(RequestName.NODE_MAP_TO_AUDIO_BUS_CONTIGUOUS, *contents)


@dataclasses.dataclass
class MapControlBusToNode(Request):
    """
    A ``/n_map`` request.

    ::

        >>> from supriya.contexts.requests import MapControlBusToNode
        >>> request = MapControlBusToNode(
        ...     node_id=1000,
        ...     items=[("frequency", 0)],
        ... )
        >>> request.to_osc()
        OscMessage('/n_map', 1000, 'frequency', 0)
    """

    node_id: SupportsInt
    items: Sequence[tuple[int | str, SupportsInt]]

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = [int(self.node_id)]
        for index_or_name, bus_index in self.items:
            contents.extend(
                [
                    (
                        index_or_name
                        if isinstance(index_or_name, str)
                        else int(index_or_name)
                    ),
                    int(bus_index),
                ]
            )
        return OscMessage(RequestName.NODE_MAP_TO_CONTROL_BUS, *contents)


@dataclasses.dataclass
class MapControlBusRangeToNode(Request):
    """
    A ``/n_mapn`` request.

    ::

        >>> from supriya.contexts.requests import MapControlBusRangeToNode
        >>> request = MapControlBusRangeToNode(
        ...     node_id=1000,
        ...     items=[("frequency", 0, 4)]
        ... )
        >>> request.to_osc()
        OscMessage('/n_mapn', 1000, 'frequency', 0, 4)
    """

    node_id: SupportsInt
    items: Sequence[tuple[int | str, SupportsInt, int]]

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = [int(self.node_id)]
        for index_or_name, bus_index, count in self.items:
            contents.extend(
                [
                    (
                        index_or_name
                        if isinstance(index_or_name, str)
                        else int(index_or_name)
                    ),
                    int(bus_index),
                    int(count),
                ]
            )
        return OscMessage(RequestName.NODE_MAP_TO_CONTROL_BUS_CONTIGUOUS, *contents)


@dataclasses.dataclass
class MoveNodeAfter(Request):
    """
    A ``/n_after`` request.

    ::

        >>> from supriya.contexts.requests import MoveNodeAfter
        >>> request = MoveNodeAfter(
        ...     items=[(2000, 1001), (3000, 2001)],
        ... )
        >>> request.to_osc()
        OscMessage('/n_after', 2000, 1001, 3000, 2001)
    """

    items: Sequence[tuple[SupportsInt, SupportsInt]]

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = []
        for node_id, target_node_id in self.items:
            contents.extend([int(node_id), int(target_node_id)])
        return OscMessage(RequestName.NODE_AFTER, *contents)


@dataclasses.dataclass
class MoveNodeBefore(Request):
    """
    A ``/n_before`` request.

    ::

        >>> from supriya.contexts.requests import MoveNodeBefore
        >>> request = MoveNodeBefore(
        ...     items=[(2000, 1001), (3000, 2001)],
        ... )
        >>> request.to_osc()
        OscMessage('/n_before', 2000, 1001, 3000, 2001)
    """

    items: Sequence[tuple[SupportsInt, SupportsInt]]

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = []
        for node_id, target_node_id in self.items:
            contents.extend([int(node_id), int(target_node_id)])
        return OscMessage(RequestName.NODE_BEFORE, *contents)


@dataclasses.dataclass
class MoveNodeToGroupHead(Request):
    """
    A ``/g_head`` request.

    ::

        >>> from supriya.contexts.requests import MoveNodeToGroupHead
        >>> request = MoveNodeToGroupHead(
        ...     items=[(1000, 1), (1001, 1)],
        ... )
        >>> request.to_osc()
        OscMessage('/g_head', 1, 1000, 1, 1001)
    """

    items: Sequence[tuple[SupportsInt, SupportsInt]]

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = []
        for node_id, target_group_id in self.items:
            contents.extend([int(target_group_id), int(node_id)])
        return OscMessage(RequestName.GROUP_HEAD, *contents)


@dataclasses.dataclass
class MoveNodeToGroupTail(Request):
    """
    A ``/g_tail`` request.

    ::

        >>> from supriya.contexts.requests import MoveNodeToGroupTail
        >>> request = MoveNodeToGroupTail(
        ...     items=[(1000, 1), (1001, 1)],
        ... )
        >>> request.to_osc()
        OscMessage('/g_tail', 1, 1000, 1, 1001)
    """

    items: Sequence[tuple[SupportsInt, SupportsInt]]

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = []
        for node_id, target_group_id in self.items:
            contents.extend([int(target_group_id), int(node_id)])
        return OscMessage(RequestName.GROUP_TAIL, *contents)


@dataclasses.dataclass
class NewGroup(Request):
    """
    A ``/g_new`` request.

    ::

        >>> from supriya.contexts.requests import NewGroup
        >>> request = NewGroup(
        ...     items=[(1000, "ADD_TO_TAIL", 1)],
        ... )
        >>> request.to_osc()
        OscMessage('/g_new', 1000, 1, 1)
    """

    items: Sequence[tuple[SupportsInt, AddActionLike, SupportsInt]]

    @classmethod
    def merge(cls, requests: list["Request"]) -> list["Request"]:
        items: list[tuple[SupportsInt, AddActionLike, SupportsInt]] = []
        for request in requests:
            if not isinstance(request, cls):
                continue
            items.extend(request.items)
        return [cls(items=items)]

    def to_osc(self) -> OscMessage:
        contents = []
        for group_id, add_action, target_node_id in self.items:
            contents.extend(
                [
                    int(group_id),
                    int(AddAction.from_expr(add_action)),
                    int(target_node_id),
                ]
            )
        return OscMessage(RequestName.GROUP_NEW, *contents)


@dataclasses.dataclass
class NewParallelGroup(Request):
    """
    A ``/p_new`` request.

    ::

        >>> from supriya.contexts.requests import NewParallelGroup
        >>> request = NewParallelGroup(
        ...     items=[(1000, "ADD_TO_TAIL", 1)]
        ... )
        >>> request.to_osc()
        OscMessage('/p_new', 1000, 1, 1)
    """

    items: Sequence[tuple[SupportsInt, AddActionLike, SupportsInt]]

    @classmethod
    def merge(cls, requests: list["Request"]) -> list["Request"]:
        items: list[tuple[SupportsInt, AddActionLike, SupportsInt]] = []
        for request in requests:
            if not isinstance(request, cls):
                continue
            items.extend(request.items)
        return [cls(items=items)]

    def to_osc(self) -> OscMessage:
        contents = []
        for group_id, add_action, target_node_id in self.items:
            contents.extend(
                [
                    int(group_id),
                    int(AddAction.from_expr(add_action)),
                    int(target_node_id),
                ]
            )
        return OscMessage(RequestName.PARALLEL_GROUP_NEW, *contents)


@dataclasses.dataclass
class NewSynth(Request):
    """
    A ``/s_new`` request.

    ::

        >>> from supriya import default
        >>> from supriya.contexts.requests import NewSynth
        >>> request = NewSynth(
        ...     synthdef=default,
        ...     synth_id=1001,
        ...     add_action="ADD_TO_TAIL",
        ...     target_node_id=1000,
        ...     controls={
        ...         "frequency": 432.0,
        ...         "amplitude": 0.5,
        ...         "panning": "c0",
        ...     },
        ... )
        >>> request.to_osc()
        OscMessage('/s_new', 'supriya:default', 1001, 1, 1000, 'amplitude', 0.5, 'frequency', 432.0, 'panning', 'c0')
    """

    synthdef: SynthDef | str
    synth_id: SupportsInt
    add_action: AddActionLike
    target_node_id: SupportsInt
    controls: dict[int | str, float | str | tuple[float | str, ...]] | None = None

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = [
            (
                self.synthdef.effective_name
                if isinstance(self.synthdef, SynthDef)
                else self.synthdef
            ),
            int(self.synth_id),
            int(AddAction.from_expr(self.add_action)),
            int(self.target_node_id),
        ]
        for key, value in sorted((self.controls or {}).items()):
            contents.append(key if isinstance(key, str) else int(key))
            if isinstance(value, tuple):
                if len(value) == 1:
                    contents.append(value[0])
                else:
                    contents.append(value)
            elif isinstance(value, (float, str)):
                contents.append(value)
        return OscMessage(RequestName.SYNTH_NEW, *contents)


@dataclasses.dataclass
class NormalizeBuffer(Request):
    """
    A ``/b_gen`` ``normalize`` (or ``wnormalize``) request.

    ::

        >>> from supriya.contexts.requests import NormalizeBuffer
        >>> request = NormalizeBuffer(
        ...     buffer_id=1,
        ...     new_maximum=0.999,
        ... )
        >>> request.to_osc()
        OscMessage('/b_gen', 1, 'normalize', 0.999)
    """

    buffer_id: SupportsInt
    new_maximum: float = 1.0
    as_wavetable: bool = False

    def _get_response_patterns(
        self,
    ) -> tuple[Sequence[float | str] | None, Sequence[float | str] | None]:
        return ["/done", "/b_gen", int(self.buffer_id)], None

    def to_osc(self) -> OscMessage:
        return OscMessage(
            RequestName.BUFFER_GENERATE,
            int(self.buffer_id),
            "wnormalize" if self.as_wavetable else "normalize",
            float(self.new_maximum),
        )


@dataclasses.dataclass
class OrderNodes(Request):
    """
    A ``/n_order`` request.

    ::

        >>> from supriya.contexts.requests import OrderNodes
        >>> request = OrderNodes(
        ...     add_action="ADD_AFTER",
        ...     target_node_id=1000,
        ...     node_ids=[1003, 1002, 1001],
        ... )
        >>> request.to_osc()
        OscMessage('/n_order', 3, 1000, 1003, 1002, 1001)
    """

    add_action: AddActionLike
    target_node_id: SupportsInt
    node_ids: Sequence[SupportsInt]

    def to_osc(self) -> OscMessage:
        return OscMessage(
            RequestName.NODE_ORDER,
            int(AddAction.from_expr(self.add_action)),
            int(self.target_node_id),
            *(int(node_id) for node_id in self.node_ids),
        )


@dataclasses.dataclass
class QueryBuffer(Request):
    """
    A ``/b_query`` request.

    ::

        >>> from supriya.contexts.requests import QueryBuffer
        >>> request = QueryBuffer(buffer_ids=[1, 2, 3])
        >>> request.to_osc()
        OscMessage('/b_query', 1, 2, 3)
    """

    buffer_ids: Sequence[int]

    def _get_response_patterns(
        self,
    ) -> tuple[Sequence[float | str] | None, Sequence[float | str] | None]:
        # TODO: We should be able to gather multiple responses
        return ["/b_info", self.buffer_ids[-1]], None

    def to_osc(self) -> OscMessage:
        return OscMessage(
            RequestName.BUFFER_QUERY, *(int(buffer_id) for buffer_id in self.buffer_ids)
        )


@dataclasses.dataclass
class QueryNode(Request):
    """
    A ``/n_query`` request.

    ::

        >>> from supriya.contexts.requests import QueryNode
        >>> request = QueryNode(node_ids=[1000, 1001])
        >>> request.to_osc()
        OscMessage('/n_query', 1000, 1001)
    """

    node_ids: Sequence[SupportsInt]

    def _get_response_patterns(
        self,
    ) -> tuple[Sequence[float | str] | None, Sequence[float | str] | None]:
        # TODO: We should be able to gather multiple responses
        return ["/n_info", int(self.node_ids[-1])], None

    def to_osc(self) -> OscMessage:
        return OscMessage(
            RequestName.NODE_QUERY, *(int(node_id) for node_id in self.node_ids)
        )


@dataclasses.dataclass
class QueryStatus(Request):
    """
    A ``/status`` request.

    ::

        >>> from supriya.contexts.requests import QueryStatus
        >>> request = QueryStatus()
        >>> request.to_osc()
        OscMessage('/status')
    """

    def _get_response_patterns(
        self,
    ) -> tuple[Sequence[float | str] | None, Sequence[float | str] | None]:
        return ["/status.reply"], None

    def to_osc(self) -> OscMessage:
        return OscMessage(RequestName.STATUS)


@dataclasses.dataclass
class QueryTree(Request):
    """
    A ``/g_queryTree`` request.

    ::

        >>> from supriya.contexts.requests import QueryTree
        >>> request = QueryTree(items=[(0, True)])
        >>> request.to_osc()
        OscMessage('/g_queryTree', 0, 1)
    """

    items: Sequence[tuple[SupportsInt, bool]]

    def _get_response_patterns(
        self,
    ) -> tuple[Sequence[float | str] | None, Sequence[float | str] | None]:
        # TODO: We should be able to gather multiple responses
        return [
            "/g_queryTree.reply",
            int(self.items[-1][1]),
            int(self.items[-1][0]),
        ], None

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = []
        for node_id, flag in self.items:
            contents.extend([int(node_id), int(bool(flag))])
        return OscMessage(RequestName.GROUP_QUERY_TREE, *contents)


@dataclasses.dataclass
class QueryVersion(Request):
    """
    A ``/version`` request.

    ::

        >>> from supriya.contexts.requests import QueryVersion
        >>> request = QueryVersion()
        >>> request.to_osc()
        OscMessage('/version')
    """

    def _get_response_patterns(
        self,
    ) -> tuple[Sequence[float | str] | None, Sequence[float | str] | None]:
        return ["/version.reply"], None

    def to_osc(self) -> OscMessage:
        return OscMessage(RequestName.VERSION)


@dataclasses.dataclass
class Quit(Request):
    """
    A ``/quit`` request.

    ::

        >>> from supriya.contexts.requests import Quit
        >>> request = Quit()
        >>> request.to_osc()
        OscMessage('/quit')
    """

    def _get_response_patterns(
        self,
    ) -> tuple[Sequence[float | str] | None, Sequence[float | str] | None]:
        return ["/done", "/quit"], None

    def to_osc(self) -> OscMessage:
        return OscMessage(RequestName.QUIT)


@dataclasses.dataclass
class ReadBuffer(Request):
    """
    A ``/b_read`` request.

    ::

        >>> from supriya.contexts.requests import NormalizeBuffer, ReadBuffer
        >>> request = ReadBuffer(
        ...     buffer_id=1,
        ...     path="path/to/audio.wav",
        ...     on_completion=NormalizeBuffer(buffer_id=1),
        ... )
        >>> request.to_osc()
        OscMessage('/b_read', 1, 'path/to/audio.wav', 0, -1, 0, 0, OscMessage('/b_gen', 1, 'normalize', 1.0))
    """

    buffer_id: SupportsInt
    path: PathLike
    frame_count: int = -1
    leave_open: bool = False
    starting_frame_in_buffer: int = 0
    starting_frame_in_file: int = 0
    on_completion: Requestable | None = None

    def _get_response_patterns(
        self,
    ) -> tuple[Sequence[float | str] | None, Sequence[float | str] | None]:
        return ["/done", "/b_read", int(self.buffer_id)], None

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = [
            int(self.buffer_id),
            str(self.path),
            int(self.starting_frame_in_file),
            int(self.frame_count),
            int(self.starting_frame_in_buffer),
            int(bool(self.leave_open)),
        ]
        if self.on_completion:
            contents.append(self.on_completion.to_osc())
        return OscMessage(RequestName.BUFFER_READ, *contents)


@dataclasses.dataclass
class ReadBufferChannel(Request):
    """
    A ``/b_readChannel`` request.

    ::

        >>> from supriya.contexts.requests import NormalizeBuffer, ReadBufferChannel
        >>> request = ReadBufferChannel(
        ...     buffer_id=1,
        ...     path="path/to/audio.wav",
        ...     channel_indices=[2, 4],
        ...     on_completion=NormalizeBuffer(buffer_id=1),
        ... )
        >>> request.to_osc()
        OscMessage('/b_readChannel', 1, 'path/to/audio.wav', 0, -1, 0, 0, 2, 4, OscMessage('/b_gen', 1, 'normalize', 1.0))
    """

    buffer_id: SupportsInt
    path: PathLike
    channel_indices: Sequence[int] | None = None
    frame_count: int = -1
    leave_open: bool = False
    starting_frame_in_buffer: int = 0
    starting_frame_in_file: int = 0
    on_completion: Requestable | None = None

    def _get_response_patterns(
        self,
    ) -> tuple[Sequence[float | str] | None, Sequence[float | str] | None]:
        return ["/done", "/b_readChannel", int(self.buffer_id)], None

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = [
            int(self.buffer_id),
            str(self.path),
            int(self.starting_frame_in_file),
            int(self.frame_count),
            int(self.starting_frame_in_buffer),
            int(bool(self.leave_open)),
            *(int(channel_index) for channel_index in self.channel_indices or []),
        ]
        if self.on_completion:
            contents.append(self.on_completion.to_osc())
        return OscMessage(RequestName.BUFFER_READ_CHANNEL, *contents)


@dataclasses.dataclass
class ReceiveSynthDefs(Request):
    r"""
    A ``/d_recv`` request.

    ::

        >>> from supriya import OscMessage, default
        >>> from supriya.contexts.requests import NewSynth, ReceiveSynthDefs
        >>> request = ReceiveSynthDefs(
        ...     synthdefs=[default],
        ...     on_completion=NewSynth(
        ...         synthdef=default,
        ...         synth_id=1000,
        ...         add_action="ADD_TO_TAIL",
        ...         target_node_id=1,
        ...     ),
        ... )
        >>> request.to_osc() == OscMessage(
        ...     "/d_recv", default.compile(), OscMessage('/s_new', 'supriya:default', 1000, 1, 1),
        ... )
        True
    """

    synthdefs: Sequence[SynthDef]
    on_completion: Requestable | None = None

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = [compile_synthdefs(*self.synthdefs)]
        if self.on_completion:
            contents.append(self.on_completion.to_osc())
        return OscMessage(RequestName.SYNTHDEF_RECEIVE, *contents)


@dataclasses.dataclass
class ReleaseNode(Request):
    node_id: SupportsInt
    has_gate: bool = False
    force: bool = False

    def to_osc(self) -> OscMessage:
        if not self.force and self.has_gate:
            return SetNodeControl(node_id=self.node_id, items=[("gate", 0)]).to_osc()
        return FreeNode(node_ids=[self.node_id]).to_osc()


@dataclasses.dataclass
class RunNode(Request):
    """
    A ``/n_run`` request.

    ::

        >>> from supriya.contexts.requests import RunNode
        >>> request = RunNode(items=[(1000, True)])
        >>> request.to_osc()
        OscMessage('/n_run', 1000, 1)
    """

    items: Sequence[tuple[SupportsInt, bool]]

    @classmethod
    def merge(cls, requests: list["Request"]) -> list["Request"]:
        items: list[tuple[SupportsInt, bool]] = []
        for request in requests:
            if not isinstance(request, cls):
                continue
            items.extend(request.items)
        return [cls(items=items)]

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = []
        for node_id, flag in self.items:
            contents.extend([int(node_id), int(flag)])
        return OscMessage(RequestName.NODE_RUN, *contents)


@dataclasses.dataclass
class SetBuffer(Request):
    """
    A ``/b_set`` request.

    ::

        >>> from supriya.contexts.requests import SetBuffer
        >>> request = SetBuffer(
        ...     buffer_id=1,
        ...     items=[(0, 0.5), (8, 0.25)],
        ... )
        >>> request.to_osc()
        OscMessage('/b_set', 1, 0, 0.5, 8, 0.25)
    """

    buffer_id: SupportsInt
    items: Sequence[tuple[int, float]]

    @classmethod
    def merge(cls, requests: list["Request"]) -> list["Request"]:
        items_by_buffer_id: dict[int, list[tuple[int, float]]] = {}
        for request in requests:
            if isinstance(request, cls):
                items_by_buffer_id.setdefault(int(request.buffer_id), []).extend(
                    request.items
                )
        return [
            cls(buffer_id=buffer_id, items=items)
            for buffer_id, items in sorted(items_by_buffer_id.items())
        ]

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = [int(self.buffer_id)]
        for index, value in self.items:
            contents.extend([int(index), float(value)])
        return OscMessage(RequestName.BUFFER_SET, *contents)


@dataclasses.dataclass
class SetBufferRange(Request):
    """
    A ``/b_setn`` request.

    ::

        >>> from supriya.contexts.requests import SetBufferRange
        >>> request = SetBufferRange(
        ...     buffer_id=1,
        ...     items=[(0, (0.1, 0.2, 0.3)), (8, (0.4, 0.5))],
        ... )
        >>> request.to_osc()
        OscMessage('/b_setn', 1, 0, 3, 0.1, 0.2, 0.3, 8, 2, 0.4, 0.5)
    """

    buffer_id: SupportsInt
    items: Sequence[tuple[int, Sequence[float]]]

    @classmethod
    def merge(cls, requests: list["Request"]) -> list["Request"]:
        items_by_buffer_id: dict[int, list[tuple[int, Sequence[float]]]] = {}
        for request in requests:
            if isinstance(request, cls):
                items_by_buffer_id.setdefault(int(request.buffer_id), []).extend(
                    request.items
                )
        return [
            cls(buffer_id=buffer_id, items=items)
            for buffer_id, items in sorted(items_by_buffer_id.items())
        ]

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = [int(self.buffer_id)]
        for index, values in self.items:
            contents.extend(
                [int(index), len(values), *(float(value) for value in values)]
            )
        return OscMessage(RequestName.BUFFER_SET_CONTIGUOUS, *contents)


@dataclasses.dataclass
class SetControlBus(Request):
    """
    A ``/c_set`` request.

    ::

        >>> from supriya.contexts.requests import SetControlBus
        >>> request = SetControlBus(items=[(0, 0.5), (4, 0.75)])
        >>> request.to_osc()
        OscMessage('/c_set', 0, 0.5, 4, 0.75)
    """

    items: Sequence[tuple[SupportsInt, float]]

    @classmethod
    def merge(cls, requests: list["Request"]) -> list["Request"]:
        items: list[tuple[SupportsInt, float]] = []
        for request in requests:
            if not isinstance(request, cls):
                continue
            items.extend(request.items)
        return [cls(items=items)]

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = []
        for index, value in self.items:
            contents.extend([int(index), float(value)])
        return OscMessage(RequestName.CONTROL_BUS_SET, *contents)


@dataclasses.dataclass
class SetControlBusRange(Request):
    """
    A ``/c_setn`` request.

    ::

        >>> from supriya.contexts.requests import SetControlBusRange
        >>> request = SetControlBusRange(
        ...     items=[(8, [1.1, 2.2, 3.3]), (16, [4.4, 5.5])],
        ... )
        >>> request.to_osc()
        OscMessage('/c_setn', 8, 3, 1.1, 2.2, 3.3, 16, 2, 4.4, 5.5)
    """

    items: Sequence[tuple[SupportsInt, Sequence[float]]]

    @classmethod
    def merge(cls, requests: list["Request"]) -> list["Request"]:
        items: list[tuple[SupportsInt, Sequence[float]]] = []
        for request in requests:
            if not isinstance(request, cls):
                continue
            items.extend(request.items)
        return [cls(items=items)]

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = []
        for index, values in self.items:
            contents.extend(
                [int(index), len(values), *(float(value) for value in values)]
            )
        return OscMessage(RequestName.CONTROL_BUS_SET_CONTIGUOUS, *contents)


@dataclasses.dataclass
class SetNodeControl(Request):
    """
    A ``/n_set`` request.

    ::

        >>> from supriya.contexts.requests import SetNodeControl
        >>> request = SetNodeControl(
        ...     node_id=1000,
        ...     items=[
        ...         ("frequency", 440.0),
        ...         ("amplitude", 1.0),
        ...         (3, 1.234),
        ...         ("positions", [0.5, 0.25, 0.75]),
        ...         (4, [0.1, 0.2]),
        ...     ],
        ... )
        >>> request.to_osc()
        OscMessage('/n_set', 1000, 'frequency', 440.0, 'amplitude', 1.0, 3, 1.234, 'positions', [0.5, 0.25, 0.75], 4, [0.1, 0.2])
    """

    node_id: SupportsInt
    items: Sequence[tuple[int | str, float | Sequence[float]]]

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = [int(self.node_id)]
        for control, values in self.items:
            contents.append(control if isinstance(control, str) else int(control))
            if isinstance(values, Sequence):
                contents.append([float(value) for value in values])
            else:
                contents.append(float(values))
        return OscMessage(RequestName.NODE_SET, *contents)


@dataclasses.dataclass
class SetNodeControlRange(Request):
    """
    A ``/n_setn`` request.

    ::

        >>> from supriya.contexts.requests import SetNodeControlRange
        >>> request = SetNodeControlRange(
        ...     node_id=1000,
        ...     items=[
        ...         ("frequency", (440.0, 441.0, 432.0)),
        ...         (3, (0.5, 0.25, 0.75)),
        ...     ],
        ... )
        >>> request.to_osc()
        OscMessage('/n_setn', 1000, 'frequency', 3, 440.0, 441.0, 432.0, 3, 3, 0.5, 0.25, 0.75)
    """

    node_id: SupportsInt
    items: Sequence[tuple[int | str, Sequence[float]]]

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = [int(self.node_id)]
        for control, values in self.items:
            contents.extend(
                [
                    control if isinstance(control, str) else int(control),
                    len(values),
                    *(float(value) for value in values),
                ]
            )
        return OscMessage(RequestName.NODE_SET_CONTIGUOUS, *contents)


@dataclasses.dataclass
class Sync(Request):
    """
    A ``/sync`` request.

    ::

        >>> from supriya.contexts.requests import Sync
        >>> request = Sync(42)
        >>> request.to_osc()
        OscMessage('/sync', 42)
    """

    sync_id: int

    def _get_response_patterns(
        self,
    ) -> tuple[Sequence[float | str] | None, Sequence[float | str] | None]:
        return ["/synced", self.sync_id], None

    def to_osc(self) -> OscMessage:
        return OscMessage(RequestName.SYNC, int(self.sync_id))


@dataclasses.dataclass
class ToggleErrorReporting(Request):
    """
    A ``/error`` request.

    ::

        >>> from supriya.contexts.requests import ToggleErrorReporting
        >>> request = ToggleErrorReporting(code=1)
        >>> request.to_osc()
        OscMessage('/error', 1)
    """

    code: Literal[0, 1, -1, -2]

    def to_osc(self) -> OscMessage:
        return OscMessage(RequestName.ERROR, int(self.code))


@dataclasses.dataclass
class ToggleNotifications(Request):
    """
    A ``/notify`` request.

    ::

        >>> from supriya.contexts.requests import ToggleNotifications
        >>> request = ToggleNotifications(True)
        >>> request.to_osc()
        OscMessage('/notify', 1)
    """

    should_notify: bool
    client_id: int | None = None

    def _get_response_patterns(
        self,
    ) -> tuple[Sequence[float | str] | None, Sequence[float | str] | None]:
        return ["/done", "/notify"], ["/fail", "/notify"]

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = [int(bool(self.should_notify))]
        if self.client_id is not None:
            contents.append(int(self.client_id))
        return OscMessage(RequestName.NOTIFY, *contents)


@dataclasses.dataclass
class TraceNode(Request):
    """
    A ``/n_trace`` request.

    ::

        >>> from supriya.contexts.requests import TraceNode
        >>> request = TraceNode(node_ids=[1, 2, 3])
        >>> request.to_osc()
        OscMessage('/n_trace', 1, 2, 3)
    """

    node_ids: Sequence[SupportsInt]

    def to_osc(self) -> OscMessage:
        return OscMessage(
            RequestName.NODE_TRACE, *(int(node_id) for node_id in self.node_ids)
        )


@dataclasses.dataclass
class WriteBuffer(Request):
    """
    A ``/b_write`` request.

    ::

        >>> from supriya.contexts.requests import FreeBuffer, WriteBuffer
        >>> request = WriteBuffer(
        ...     buffer_id=1,
        ...     path="path/to/audio.wav",
        ...     header_format="wav",
        ...     sample_format="int24",
        ...     on_completion=FreeBuffer(buffer_id=1)
        ... )
        >>> request.to_osc()
        OscMessage('/b_write', 1, 'path/to/audio.wav', 'wav', 'int24', -1, 0, 0, OscMessage('/b_free', 1))
    """

    buffer_id: SupportsInt
    path: PathLike
    header_format: HeaderFormatLike
    sample_format: SampleFormatLike
    frame_count: int = -1
    starting_frame: int = 0
    leave_open: bool = False
    on_completion: Requestable | None = None

    def _get_response_patterns(
        self,
    ) -> tuple[Sequence[float | str] | None, Sequence[float | str] | None]:
        return ["/done", "/b_write", int(self.buffer_id)], None

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = [
            int(self.buffer_id),
            str(self.path),
            HeaderFormat.from_expr(self.header_format).name.lower(),
            SampleFormat.from_expr(self.sample_format).name.lower(),
            int(self.frame_count),
            int(self.starting_frame),
            int(bool(self.leave_open)),
        ]
        if self.on_completion:
            contents.append(self.on_completion.to_osc())
        return OscMessage(RequestName.BUFFER_WRITE, *contents)


@dataclasses.dataclass
class ZeroBuffer(Request):
    """
    A ``/b_zero`` request.

    ::

        >>> from supriya.contexts.requests import FreeNode, ZeroBuffer
        >>> request = ZeroBuffer(
        ...     buffer_id=1,
        ...     on_completion=FreeNode(node_ids=[1000]),
        ... )
        >>> request.to_osc()
        OscMessage('/b_zero', 1, OscMessage('/n_free', 1000))
    """

    buffer_id: SupportsInt
    on_completion: Requestable | None = None

    def _get_response_patterns(
        self,
    ) -> tuple[Sequence[float | str] | None, Sequence[float | str] | None]:
        return ["/done", "/b_zero", int(self.buffer_id)], None

    def to_osc(self) -> OscMessage:
        contents: list[OscArgument] = [int(self.buffer_id)]
        if self.on_completion:
            contents.append(self.on_completion.to_osc())
        return OscMessage(RequestName.BUFFER_ZERO, *contents)
