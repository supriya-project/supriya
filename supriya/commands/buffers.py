import collections
from collections.abc import Sequence
from typing import NamedTuple

import supriya.osc
from supriya import HeaderFormat, SampleFormat, utils
from supriya.enums import RequestId

from .bases import Request, RequestBundle, Response


class BufferAllocateRequest(Request):
    """
    A /b_alloc request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.BufferAllocateRequest(
        ...     buffer_id=23,
        ...     frame_count=512,
        ...     channel_count=2,
        ... )
        >>> request
        BufferAllocateRequest(
            buffer_id=23,
            channel_count=2,
            frame_count=512,
        )

    ::

        >>> request.to_osc()
        OscMessage('/b_alloc', 23, 512, 2)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.BUFFER_ALLOCATE

    ### INITIALIZER ###

    def __init__(
        self, buffer_id=None, frame_count=None, channel_count=None, callback=None
    ):
        Request.__init__(self)
        self._buffer_id = int(buffer_id)
        self._frame_count = frame_count
        if channel_count is not None:
            channel_count = int(channel_count)
            assert 0 < channel_count
        self._channel_count = channel_count
        if callback is not None:
            assert isinstance(callback, (Request, RequestBundle))
        self._callback = callback

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        buffer_id = int(self.buffer_id)
        frame_count = int(self.frame_count)
        channel_count = int(self.channel_count)
        contents = [request_id, buffer_id, frame_count, channel_count]
        if self.callback:
            contents.append(self.callback.to_osc())
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def channel_count(self):
        return self._channel_count

    @property
    def callback(self):
        return self._callback

    @property
    def frame_count(self):
        return self._frame_count

    @property
    def response_patterns(self):
        return ["/done", "/b_alloc", self.buffer_id], None


class BufferAllocateReadRequest(BufferAllocateRequest):
    """
    A /b_allocRead request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.BufferAllocateReadRequest(
        ...     buffer_id=23,
        ...     file_path="pulse_44100sr_16bit_octo.wav",
        ... )
        >>> print(request)
        BufferAllocateReadRequest(
            buffer_id=23,
            file_path='pulse_44100sr_16bit_octo.wav',
        )

    ::

        >>> request.to_osc()
        OscMessage('/b_allocRead', 23, '...pulse_44100sr_16bit_octo.wav', 0, -1)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.BUFFER_ALLOCATE_READ

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        callback=None,
        file_path=None,
        frame_count=None,
        starting_frame=None,
    ):
        import supriya.nonrealtime

        BufferAllocateRequest.__init__(
            self, buffer_id=buffer_id, frame_count=frame_count, callback=callback
        )
        if not supriya.nonrealtime.Session.is_session_like(file_path):
            file_path = str(file_path)
        self._file_path = file_path
        if starting_frame is not None:
            starting_frame = int(starting_frame)
            assert 0 <= starting_frame
        self._starting_frame = starting_frame

    ### PRIVATE METHODS ###

    def _get_osc_message_contents(self, *, with_placeholders=False):
        request_id = self.request_name
        buffer_id = int(self.buffer_id)
        frame_count = self.frame_count
        if frame_count is None:
            frame_count = -1
        starting_frame = self.starting_frame
        if starting_frame is None:
            starting_frame = 0
        contents = [request_id, buffer_id, self.file_path, starting_frame, frame_count]
        return contents

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        contents = self._get_osc_message_contents()
        if self.callback:
            contents.append(self.callback.to_osc())
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def callback(self):
        return self._callback

    @property
    def file_path(self):
        return self._file_path

    @property
    def frame_count(self):
        return self._frame_count

    @property
    def response_patterns(self):
        return ["/done", "/b_allocRead", self.buffer_id], None

    @property
    def starting_frame(self):
        return self._starting_frame


class BufferAllocateReadChannelRequest(BufferAllocateReadRequest):
    """
    A /b_allocRead request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.BufferAllocateReadChannelRequest(
        ...     buffer_id=23,
        ...     channel_indices=(3, 4),
        ...     file_path="pulse_44100sr_16bit_octo.wav",
        ... )
        >>> print(request)
        BufferAllocateReadChannelRequest(
            buffer_id=23,
            channel_indices=(3, 4),
            file_path='pulse_44100sr_16bit_octo.wav',
        )

    ::

        >>> request.to_osc()
        OscMessage('/b_allocReadChannel', 23, '...pulse_44100sr_16bit_octo.wav', 0, -1, 3, 4)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.BUFFER_ALLOCATE_READ_CHANNEL

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        channel_indices=None,
        callback=None,
        file_path=None,
        frame_count=None,
        starting_frame=None,
    ):
        BufferAllocateReadRequest.__init__(
            self,
            buffer_id=buffer_id,
            callback=callback,
            file_path=file_path,
            frame_count=frame_count,
            starting_frame=starting_frame,
        )
        if channel_indices is None:
            channel_indices = -1
        if not isinstance(channel_indices, Sequence):
            channel_indices = (channel_indices,)
        channel_indices = tuple(int(_) for _ in channel_indices)
        if channel_indices != (-1,):
            assert all(0 <= _ for _ in channel_indices)
        self._channel_indices = channel_indices

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        contents = self._get_osc_message_contents()
        contents.extend(self.channel_indices)
        if self.callback:
            contents.append(self.callback.to_osc())
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def channel_indices(self):
        return self._channel_indices

    @property
    def response_patterns(self):
        return ["/done", "/b_allocReadChannel", self.buffer_id], None


class BufferCloseRequest(Request):
    """
    A /b_close request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.BufferCloseRequest(
        ...     buffer_id=23,
        ... )
        >>> request
        BufferCloseRequest(
            buffer_id=23,
        )

    ::

        >>> request.to_osc()
        OscMessage('/b_close', 23)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.BUFFER_CLOSE

    ### INITIALIZER ###

    def __init__(self, buffer_id=None):
        Request.__init__(self)
        self._buffer_id = int(buffer_id)

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        buffer_id = int(self.buffer_id)
        message = supriya.osc.OscMessage(request_id, buffer_id)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def response_patterns(self):
        return ["/done", "/b_close", self.buffer_id], None


class BufferCopyRequest(Request):
    """
    A `/b_gen copy` request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.BufferCopyRequest(
        ...     source_buffer_id=23,
        ...     target_buffer_id=666,
        ... )
        >>> print(request)
        BufferCopyRequest(
            source_buffer_id=23,
            target_buffer_id=666,
        )

    ::

        >>> request.to_osc()
        OscMessage('/b_gen', 666, 'copy', 0, 23, 0, -1)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.BUFFER_GENERATE

    ### INITIALIZER ###

    def __init__(
        self,
        frame_count=None,
        source_buffer_id=None,
        source_starting_frame=None,
        target_buffer_id=None,
        target_starting_frame=None,
    ):
        Request.__init__(self)
        self._source_buffer_id = int(source_buffer_id)
        self._target_buffer_id = int(target_buffer_id)
        if frame_count is not None:
            frame_count = int(frame_count)
            assert -1 <= frame_count
        self._frame_count = frame_count
        if source_starting_frame is not None:
            source_starting_frame = int(source_starting_frame)
            assert 0 <= source_starting_frame
        self._source_starting_frame = source_starting_frame
        if target_starting_frame is not None:
            target_starting_frame = int(target_starting_frame)
            assert 0 <= target_starting_frame
        self._target_starting_frame = target_starting_frame

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        frame_count = self.frame_count
        if frame_count is None:
            frame_count = -1
        source_starting_frame = self.source_starting_frame
        if source_starting_frame is None:
            source_starting_frame = 0
        target_starting_frame = self.target_starting_frame
        if target_starting_frame is None:
            target_starting_frame = 0
        contents = [
            request_id,
            self.target_buffer_id,
            "copy",
            target_starting_frame,
            self.source_buffer_id,
            source_starting_frame,
            frame_count,
        ]
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def frame_count(self):
        return self._frame_count

    @property
    def response_patterns(self):
        return ["/done", "/b_gen", self.target_buffer_id], None

    @property
    def source_buffer_id(self):
        return self._source_buffer_id

    @property
    def source_starting_frame(self):
        return self._source_starting_frame

    @property
    def target_buffer_id(self):
        return self._target_buffer_id

    @property
    def target_starting_frame(self):
        return self._target_starting_frame


class BufferFillRequest(Request):
    """
    A /b_fill request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.BufferFillRequest(
        ...     buffer_id=23,
        ...     index_count_value_triples=(
        ...         (0, 8, 0.1),
        ...         (11, 4, 0.2),
        ...     ),
        ... )
        >>> request
        BufferFillRequest(
            buffer_id=23,
            index_count_value_triples=(
                (0, 8, 0.1),
                (11, 4, 0.2),
            ),
        )

    ::

        >>> request.to_osc()
        OscMessage('/b_fill', 23, 0, 8, 0.1, 11, 4, 0.2)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.BUFFER_FILL

    ### INITIALIZER ###

    def __init__(self, buffer_id=None, index_count_value_triples=None):
        Request.__init__(self)
        self._buffer_id = int(buffer_id)
        triples = []
        for index, count, value in index_count_value_triples:
            triple = (int(index), int(count), float(value))
            triples.append(triple)
        triples = tuple(triples)
        self._index_count_value_triples = triples

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        buffer_id = int(self.buffer_id)
        contents = [request_id, buffer_id]
        for index, count, value in self.index_count_value_triples:
            contents.append(int(index))
            contents.append(int(count))
            contents.append(float(value))
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def index_count_value_triples(self):
        return self._index_count_value_triples


class BufferFreeRequest(Request):
    """
    A /b_free request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.BufferFreeRequest(
        ...     buffer_id=23,
        ... )
        >>> request
        BufferFreeRequest(
            buffer_id=23,
        )

    ::

        >>> request.to_osc()
        OscMessage('/b_free', 23)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.BUFFER_FREE

    ### INITIALIZER ###

    def __init__(self, buffer_id=None, callback=None):
        Request.__init__(self)
        self._buffer_id = int(buffer_id)
        if callback is not None:
            assert isinstance(callback, (Request, RequestBundle))
        self._callback = callback

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        buffer_id = int(self.buffer_id)
        contents = [request_id, buffer_id]
        if self.callback:
            contents.append(self.callback.to_osc())
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def callback(self):
        return self._callback


class BufferGenerateRequest(Request):
    """
    A /b_gen request.

    This requests models the 'cheby', 'sine1', 'sine2' and 'sine3' /b_gen
    commands.

    Use BufferCopyRequest for `/b_gen copy` and BufferNormalizeRequest for
    `/b_gen normalize` and `/b_gen wnormalize`.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.BufferGenerateRequest(
        ...     amplitudes=(1.0, 0.5, 0.25),
        ...     as_wavetable=True,
        ...     buffer_id=23,
        ...     command_name="sine3",
        ...     frequencies=(1, 2, 3),
        ...     phases=(0, 0.5, 0),
        ...     should_clear_first=True,
        ...     should_normalize=True,
        ... )
        >>> print(request)
        BufferGenerateRequest(
            amplitudes=(1.0, 0.5, 0.25),
            as_wavetable=True,
            buffer_id=23,
            command_name='sine3',
            frequencies=(1.0, 2.0, 3.0),
            phases=(0.0, 0.5, 0.0),
            should_clear_first=True,
            should_normalize=True,
        )

    ::

        >>> request.to_osc()
        OscMessage('/b_gen', 23, 'sine3', 7, 1.0, 1.0, 0.0, 2.0, 0.5, 0.5, 3.0, 0.25, 0.0)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.BUFFER_GENERATE

    ### INITIALIZER ###

    def __init__(
        self,
        amplitudes=None,
        as_wavetable=None,
        buffer_id=None,
        command_name=None,
        frequencies=None,
        phases=None,
        should_clear_first=None,
        should_normalize=None,
    ):
        Request.__init__(self)
        self._buffer_id = int(buffer_id)
        assert command_name in ("cheby", "sine1", "sine2", "sine3")
        self._command_name = command_name
        if as_wavetable is not None:
            as_wavetable = bool(as_wavetable)
        self._as_wavetable = as_wavetable
        if should_clear_first is not None:
            should_clear_first = bool(should_clear_first)
        self._should_clear_first = should_clear_first
        if should_normalize is not None:
            should_normalize = bool(should_normalize)
        self._should_normalize = should_normalize
        self._frequencies = None
        self._phases = None
        if command_name in ("cheby", "sine1"):
            if not isinstance(amplitudes, Sequence):
                amplitudes = (amplitudes,)
            amplitudes = tuple(float(_) for _ in amplitudes)
            assert len(amplitudes)
            self._amplitudes = amplitudes
        if command_name == "sine2":
            amplitudes = tuple(float(_) for _ in amplitudes)
            frequencies = tuple(float(_) for _ in frequencies)
            assert 0 < len(amplitudes)
            assert len(amplitudes) == len(frequencies)
            self._amplitudes = amplitudes
            self._frequencies = frequencies
        if command_name == "sine3":
            amplitudes = tuple(float(_) for _ in amplitudes)
            frequencies = tuple(float(_) for _ in frequencies)
            phases = tuple(float(_) for _ in phases)
            assert 0 < len(amplitudes)
            assert len(amplitudes) == len(frequencies) == len(phases)
            self._amplitudes = amplitudes
            self._frequencies = frequencies
            self._phases = phases

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        buffer_id = int(self.buffer_id)
        contents = [request_id, buffer_id, self.command_name, self.flags]
        if self.command_name in ("cheby", "sine1"):
            coefficients = self.amplitudes
        elif self.command_name == "sine2":
            coefficients = zip(self.frequencies, self.amplitudes)
            coefficients = tuple(coefficients)
        elif self.command_name == "sine3":
            coefficients = zip(self.frequencies, self.amplitudes, self.phases)
            coefficients = tuple(coefficients)
        coefficients = utils.flatten_iterable(coefficients)
        contents.extend(coefficients)
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC METHODS ###

    @classmethod
    def chebyshev(
        cls,
        amplitudes=None,
        as_wavetable=False,
        buffer_id=None,
        should_normalize=True,
        should_clear_first=True,
    ):
        command_name = "cheby"
        request = cls(
            amplitudes=amplitudes,
            as_wavetable=as_wavetable,
            buffer_id=buffer_id,
            command_name=command_name,
            should_clear_first=should_clear_first,
            should_normalize=should_normalize,
        )
        return request

    @classmethod
    def sine1(
        cls,
        amplitudes=None,
        as_wavetable=False,
        buffer_id=None,
        should_normalize=True,
        should_clear_first=True,
    ):
        command_name = "sine1"
        request = cls(
            amplitudes=amplitudes,
            as_wavetable=as_wavetable,
            buffer_id=buffer_id,
            command_name=command_name,
            should_clear_first=should_clear_first,
            should_normalize=should_normalize,
        )
        return request

    @classmethod
    def sine2(
        cls,
        amplitudes=None,
        as_wavetable=False,
        buffer_id=None,
        frequencies=None,
        should_normalize=True,
        should_clear_first=True,
    ):
        command_name = "sine2"
        request = cls(
            amplitudes=amplitudes,
            as_wavetable=as_wavetable,
            buffer_id=buffer_id,
            command_name=command_name,
            frequencies=frequencies,
            should_clear_first=should_clear_first,
            should_normalize=should_normalize,
        )
        return request

    @classmethod
    def sine3(
        cls,
        amplitudes=None,
        as_wavetable=False,
        buffer_id=None,
        frequencies=None,
        phases=None,
        should_normalize=True,
        should_clear_first=True,
    ):
        command_name = "sine3"
        request = cls(
            amplitudes=amplitudes,
            as_wavetable=as_wavetable,
            buffer_id=buffer_id,
            command_name=command_name,
            frequencies=frequencies,
            phases=phases,
            should_clear_first=should_clear_first,
            should_normalize=should_normalize,
        )
        return request

    ### PUBLIC PROPERTIES ###

    @property
    def amplitudes(self):
        return self._amplitudes

    @property
    def as_wavetable(self):
        return self._as_wavetable

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def command_name(self):
        return self._command_name

    @property
    def flags(self):
        flags = sum(
            (
                1 * int(bool(self.should_normalize)),
                2 * int(bool(self.as_wavetable)),
                4 * int(bool(self.should_clear_first)),
            )
        )
        return flags

    @property
    def frequencies(self):
        return self._frequencies

    @property
    def phases(self):
        return self._phases

    @property
    def response_patterns(self):
        return ["/done", "/b_gen", self.buffer_id], None

    @property
    def should_clear_first(self):
        return self._should_clear_first

    @property
    def should_normalize(self):
        return self._should_normalize


class BufferGetContiguousRequest(Request):
    """
    A /b_getn request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.BufferGetContiguousRequest(
        ...     buffer_id=23,
        ...     index_count_pairs=[(0, 3), (8, 11)],
        ... )
        >>> request
        BufferGetContiguousRequest(
            buffer_id=23,
            index_count_pairs=(
                (0, 3),
                (8, 11),
            ),
        )

    ::

        >>> request.to_osc()
        OscMessage('/b_getn', 23, 0, 3, 8, 11)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.BUFFER_GET_CONTIGUOUS

    ### INITIALIZER ###

    def __init__(self, buffer_id=None, index_count_pairs=None):
        Request.__init__(self)
        self._buffer_id = int(buffer_id)
        self._index_count_pairs = tuple(
            (int(index), int(count)) for index, count in index_count_pairs
        )

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        buffer_id = int(self.buffer_id)
        contents = [request_id, buffer_id]
        if self.index_count_pairs:
            for index, count in self.index_count_pairs:
                contents.append(index)
                contents.append(count)
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def index_count_pairs(self):
        return self._index_count_pairs

    @property
    def response_patterns(self):
        return ["/b_setn", self.buffer_id], ["/fail", "/b_getn"]


class BufferGetRequest(Request):
    """
    A /b_get request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.BufferGetRequest(
        ...     buffer_id=23,
        ...     indices=(0, 4, 8, 16),
        ... )
        >>> request
        BufferGetRequest(
            buffer_id=23,
            indices=(0, 4, 8, 16),
        )

    ::

        >>> request.to_osc()
        OscMessage('/b_get', 23, 0, 4, 8, 16)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.BUFFER_GET

    ### INITIALIZER ###

    def __init__(self, buffer_id=None, indices=None):
        Request.__init__(self)
        self._buffer_id = int(buffer_id)
        self._indices = tuple(int(index) for index in indices)

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        buffer_id = int(self.buffer_id)
        contents = [request_id, buffer_id]
        if self.indices:
            for index in self.indices:
                contents.append(index)
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def indices(self):
        return self._indices

    @property
    def response_patterns(self):
        return ["/b_set", self.buffer_id], ["/fail", "/b_get"]


class BufferInfoResponse(Response):

    ### CLASS VARIABLES ###

    class Item(NamedTuple):
        buffer_id: int
        frame_count: int
        channel_count: int
        sample_rate: int

    ### INITIALIZER ###

    def __init__(self, items=None):
        self._items = tuple(items or ())

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        return self._items[item]

    def __len__(self):
        return len(self._items)

    ### PUBLIC METHODS ###

    @classmethod
    def from_osc_message(cls, osc_message):
        """
        Create response(s) from OSC message.

        ::

            >>> message = supriya.osc.OscMessage("/b_info", 1100, 512, 1, 44100.0)
            >>> supriya.commands.BufferInfoResponse.from_osc_message(message)
            BufferInfoResponse(
                items=(
                    Item(buffer_id=1100, frame_count=512, channel_count=1, sample_rate=44100.0),
                ),
            )

        """
        # TODO: Return one single thing
        items = []
        for group in cls._group_items(osc_message.contents, 4):
            item = cls.Item(*group)
            items.append(item)
        return cls(items=items)

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self[0].buffer_id

    @property
    def items(self):
        return self._items


class BufferNormalizeRequest(Request):
    """
    A `/b_gen normalize` request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.BufferNormalizeRequest(
        ...     buffer_id=23,
        ... )
        >>> print(request)
        BufferNormalizeRequest(
            buffer_id=23,
        )

    ::

        >>> request.to_osc()
        OscMessage('/b_gen', 23, 'normalize', 1.0)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.BUFFER_GENERATE

    ### INITIALIZER ###

    def __init__(self, as_wavetable=None, buffer_id=None, new_maximum=1.0):
        Request.__init__(self)
        if as_wavetable is not None:
            as_wavetable = bool(as_wavetable)
        self._as_wavetable = as_wavetable
        self._buffer_id = int(buffer_id)
        self._new_maximum = float(new_maximum)

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        buffer_id = int(self.buffer_id)
        command_name = "normalize"
        if self.as_wavetable:
            command_name = "wnormalize"
        contents = [request_id, buffer_id, command_name, self.new_maximum]
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def as_wavetable(self):
        return self._as_wavetable

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def new_maximum(self):
        return self._new_maximum

    @property
    def response_patterns(self):
        return ["/done", "/b_gen", self.buffer_id], None


class BufferQueryRequest(Request):
    """
    A /b_query request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.BufferQueryRequest(buffer_ids=(1, 23, 41))
        >>> request
        BufferQueryRequest(
            buffer_ids=(1, 23, 41),
        )

    ::

        >>> request.to_osc()
        OscMessage('/b_query', 1, 23, 41)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.BUFFER_QUERY

    ### INITIALIZER ###

    def __init__(self, buffer_ids=None):
        Request.__init__(self)
        if buffer_ids:
            buffer_ids = tuple(int(buffer_id) for buffer_id in buffer_ids)
        self._buffer_ids = buffer_ids

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        contents = [request_id]
        for buffer_id in self.buffer_ids:
            contents.append(buffer_id)
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_ids(self):
        return self._buffer_ids

    @property
    def response_patterns(self):
        if 1 == len(self.buffer_ids):
            return ["/b_info", self.buffer_ids[0]], None
        return None, None


class BufferReadRequest(Request):
    """
    A /b_read request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.BufferReadRequest(
        ...     buffer_id=23,
        ...     file_path="pulse_44100sr_16bit_octo.wav",
        ... )
        >>> print(request)
        BufferReadRequest(
            buffer_id=23,
            file_path='pulse_44100sr_16bit_octo.wav',
        )

    ::

        >>> request.to_osc()
        OscMessage('/b_read', 23, '...pulse_44100sr_16bit_octo.wav', 0, -1, 0, 0)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.BUFFER_READ

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        callback=None,
        file_path=None,
        frame_count=None,
        leave_open=None,
        starting_frame_in_buffer=None,
        starting_frame_in_file=None,
    ):
        import supriya.nonrealtime

        Request.__init__(self)
        self._buffer_id = int(buffer_id)
        if callback is not None:
            assert isinstance(callback, (Request, RequestBundle))
        self._callback = callback
        if not supriya.nonrealtime.Session.is_session_like(file_path):
            file_path = str(file_path)
        self._file_path = file_path
        if frame_count is not None:
            frame_count = int(frame_count)
            assert -1 <= frame_count
        self._frame_count = frame_count
        if leave_open is not None:
            leave_open = bool(leave_open)
        self._leave_open = leave_open
        if starting_frame_in_buffer is not None:
            starting_frame_in_buffer = int(starting_frame_in_buffer)
            assert 0 <= starting_frame_in_buffer
        self._starting_frame_in_buffer = starting_frame_in_buffer
        if starting_frame_in_file is not None:
            starting_frame_in_file = int(starting_frame_in_file)
            assert 0 <= starting_frame_in_file
        self._starting_frame_in_file = starting_frame_in_file

    ### PRIVATE METHODS ###

    def _get_osc_message_contents(self, *, with_placeholders=False):
        request_id = self.request_name
        buffer_id = int(self.buffer_id)
        starting_frame_in_buffer = self.starting_frame_in_buffer
        if starting_frame_in_buffer is None:
            starting_frame_in_buffer = 0
        frame_count = self.frame_count
        if frame_count is None:
            frame_count = -1
        starting_frame_in_file = self.starting_frame_in_file
        if starting_frame_in_file is None:
            starting_frame_in_file = 0
        leave_open = int(bool(self.leave_open))
        contents = [
            request_id,
            buffer_id,
            self.file_path,
            starting_frame_in_file,
            frame_count,
            starting_frame_in_buffer,
            leave_open,
        ]
        return contents

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        contents = self._get_osc_message_contents()
        if self.callback:
            contents.append(self.callback.to_osc())
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def callback(self):
        return self._callback

    @property
    def file_path(self):
        return self._file_path

    @property
    def frame_count(self):
        return self._frame_count

    @property
    def leave_open(self):
        return self._leave_open

    @property
    def response_patterns(self):
        return ["/done", "/b_read", self.buffer_id], None

    @property
    def starting_frame_in_buffer(self):
        return self._starting_frame_in_buffer

    @property
    def starting_frame_in_file(self):
        return self._starting_frame_in_file


class BufferReadChannelRequest(BufferReadRequest):
    """
    A /b_readChannel request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.BufferReadChannelRequest(
        ...     buffer_id=23,
        ...     channel_indices=(3, 4),
        ...     file_path="pulse_44100sr_16bit_octo.wav",
        ... )
        >>> print(request)
        BufferReadChannelRequest(
            buffer_id=23,
            channel_indices=(3, 4),
            file_path='pulse_44100sr_16bit_octo.wav',
        )

    ::

        >>> request.to_osc()
        OscMessage('/b_readChannel', 23, '...pulse_44100sr_16bit_octo.wav', 0, -1, 0, 0, 3, 4)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.BUFFER_READ_CHANNEL

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        channel_indices=None,
        callback=None,
        file_path=None,
        frame_count=None,
        leave_open=None,
        starting_frame_in_buffer=None,
        starting_frame_in_file=None,
    ):
        BufferReadRequest.__init__(
            self,
            buffer_id=buffer_id,
            callback=callback,
            file_path=file_path,
            frame_count=frame_count,
            leave_open=leave_open,
            starting_frame_in_buffer=starting_frame_in_buffer,
            starting_frame_in_file=starting_frame_in_file,
        )
        if not isinstance(channel_indices, Sequence):
            channel_indices = (channel_indices,)
        channel_indices = tuple(channel_indices)
        assert all(0 <= _ for _ in channel_indices)
        self._channel_indices = channel_indices

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        contents = self._get_osc_message_contents()
        contents.extend(self.channel_indices)
        if self.callback:
            contents.append(self.callback.to_osc())
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def channel_indices(self):
        return self._channel_indices

    @property
    def response_patterns(self):
        return ["/done", "/b_readChannel", self.buffer_id], None


class BufferSetContiguousRequest(Request):
    """
    A /b_setn request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.BufferSetContiguousRequest(
        ...     buffer_id=23,
        ...     index_values_pairs=((0, (1, 2, 3)), (10, (17.1, 18.2))),
        ... )
        >>> request
        BufferSetContiguousRequest(
            buffer_id=23,
            index_values_pairs=(
                (0, (1.0, 2.0, 3.0)),
                (10, (17.1, 18.2)),
            ),
        )

    ::

        >>> request.to_osc()
        OscMessage('/b_setn', 23, 0, 3, 1.0, 2.0, 3.0, 10, 2, 17.1, 18.2)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.BUFFER_SET_CONTIGUOUS

    ### INITIALIZER ###

    def __init__(self, buffer_id=None, index_values_pairs=None):
        Request.__init__(self)
        self._buffer_id = int(buffer_id)
        if index_values_pairs:
            pairs = []
            for index, values in index_values_pairs:
                index = int(index)
                values = tuple(float(value) for value in values)
                pair = (index, values)
                pairs.append(pair)
            pairs = tuple(pairs)
        self._index_values_pairs = pairs

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        buffer_id = int(self.buffer_id)
        contents = [request_id, buffer_id]
        if self.index_values_pairs:
            for index, values in self.index_values_pairs:
                if not values:
                    continue
                contents.append(index)
                contents.append(len(values))
                for value in values:
                    contents.append(value)
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def index_values_pairs(self):
        return self._index_values_pairs


class BufferSetContiguousResponse(Response, Sequence):

    ### CLASS VARIABLES ###

    class Item(NamedTuple):
        sample_values: int
        starting_sample_index: int

    ### INITIALIZER ###

    def __init__(self, items=None, buffer_id=None):
        self._buffer_id = buffer_id
        self._items = items

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        return self._items[item]

    def __len__(self):
        return len(self._items)

    ### PUBLIC METHODS ###

    def as_dict(self):
        result = collections.OrderedDict()
        for item in self:
            result[item.starting_sample_index] = item.sample_values
        return result

    @classmethod
    def from_osc_message(cls, osc_message):
        """
        Create response from OSC message.

        ::

            >>> message = supriya.osc.OscMessage(
            ...     "/b_setn", 1, 0, 8, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
            ... )
            >>> supriya.commands.BufferSetContiguousResponse.from_osc_message(message)
            BufferSetContiguousResponse(
                buffer_id=1,
                items=(
                    Item(sample_values=(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0), starting_sample_index=0),
                ),
            )

        """
        buffer_id, remainder = osc_message.contents[0], osc_message.contents[1:]
        items = []
        while remainder:
            starting_sample_index = remainder[0]
            sample_count = remainder[1]
            sample_values = tuple(remainder[2 : 2 + sample_count])
            item = cls.Item(
                starting_sample_index=starting_sample_index, sample_values=sample_values
            )
            items.append(item)
            remainder = remainder[2 + sample_count :]
        items = tuple(items)
        response = cls(buffer_id=buffer_id, items=items)
        return response

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def items(self):
        return self._items


class BufferSetRequest(Request):
    """
    A /b_set request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.BufferSetRequest(
        ...     buffer_id=23,
        ...     index_value_pairs=(
        ...         (0, 1.0),
        ...         (10, 13.2),
        ...         (17, 19.3),
        ...     ),
        ... )
        >>> request
        BufferSetRequest(
            buffer_id=23,
            index_value_pairs=(
                (0, 1.0),
                (10, 13.2),
                (17, 19.3),
            ),
        )

    ::

        >>> request.to_osc()
        OscMessage('/b_set', 23, 0, 1.0, 10, 13.2, 17, 19.3)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.BUFFER_SET

    ### INITIALIZER ###

    def __init__(self, buffer_id=None, index_value_pairs=None):
        Request.__init__(self)
        self._buffer_id = int(buffer_id)
        if index_value_pairs:
            pairs = []
            for index, value in index_value_pairs:
                index = int(index)
                value = float(value)
                pair = (index, value)
                pairs.append(pair)
            pairs = tuple(pairs)
        self._index_value_pairs = index_value_pairs

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        buffer_id = int(self.buffer_id)
        contents = [request_id, buffer_id]
        if self.index_value_pairs:
            for index, value in self.index_value_pairs:
                contents.append(index)
                contents.append(value)
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def index_value_pairs(self):
        return self._index_value_pairs


class BufferSetResponse(Response, Sequence):

    ### CLASS VARIABLES ###

    class Item(NamedTuple):
        sample_index: int
        sample_value: float

    ### INITIALIZER ###

    def __init__(self, buffer_id=None, items=None):
        self._buffer_id = buffer_id
        self._items = items

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        return self._items[item]

    def __len__(self):
        return len(self._items)

    ### PUBLIC METHODS ###

    def as_dict(self):
        result = collections.OrderedDict()
        for item in self:
            result[item.sample_index] = item.sample_value
        return result

    @classmethod
    def from_osc_message(cls, osc_message):
        buffer_id, remainder = osc_message.contents[0], osc_message.contents[1:]
        items = []
        for group in cls._group_items(remainder, 2):
            item = cls.Item(*group)
            items.append(item)
        items = tuple(items)
        response = cls(buffer_id=buffer_id, items=items)
        return response

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def items(self):
        return self._items


class BufferWriteRequest(Request):
    """
    A /b_write request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.BufferWriteRequest(
        ...     buffer_id=23,
        ...     file_path="test.aiff",
        ...     header_format=supriya.HeaderFormat.AIFF,
        ...     sample_format=supriya.SampleFormat.INT24,
        ... )
        >>> request
        BufferWriteRequest(
            buffer_id=23,
            file_path='test.aiff',
            frame_count=-1,
            header_format=HeaderFormat.AIFF,
            sample_format=SampleFormat.INT24,
            starting_frame=0,
        )

    ::

        >>> request.to_osc()
        OscMessage('/b_write', 23, 'test.aiff', 'aiff', 'int24', -1, 0, 0)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.BUFFER_WRITE

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        callback=None,
        file_path=None,
        frame_count=None,
        header_format="aiff",
        leave_open=False,
        sample_format="int24",
        starting_frame=None,
    ):
        Request.__init__(self)
        self._buffer_id = int(buffer_id)
        if callback is not None:
            assert isinstance(callback, (Request, RequestBundle))
        self._callback = callback
        self._file_path = str(file_path)
        if frame_count is None:
            frame_count = -1
        frame_count = int(frame_count)
        assert -1 <= frame_count
        self._frame_count = frame_count
        self._header_format = HeaderFormat.from_expr(header_format)
        self._leave_open = bool(leave_open)
        self._sample_format = SampleFormat.from_expr(sample_format)
        if starting_frame is None:
            starting_frame = 0
        starting_frame = int(starting_frame)
        assert 0 <= starting_frame
        self._starting_frame = starting_frame

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        buffer_id = int(self.buffer_id)
        header_format = self.header_format.name.lower()
        sample_format = self.sample_format.name.lower()
        leave_open = int(bool(self.leave_open))
        contents = [
            request_id,
            buffer_id,
            self.file_path,
            header_format,
            sample_format,
            self.frame_count,
            self.starting_frame,
            leave_open,
        ]
        if self.callback:
            contents.append(self.callback.to_osc())
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def callback(self):
        return self._callback

    @property
    def file_path(self):
        return self._file_path

    @property
    def frame_count(self):
        return self._frame_count

    @property
    def header_format(self):
        return self._header_format

    @property
    def leave_open(self):
        return self._leave_open

    @property
    def response_patterns(self):
        return ["/done", "/b_write", self.buffer_id], None

    @property
    def sample_format(self):
        return self._sample_format

    @property
    def starting_frame(self):
        return self._starting_frame


class BufferZeroRequest(Request):
    """
    A /b_zero request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.BufferZeroRequest(
        ...     buffer_id=23,
        ... )
        >>> request
        BufferZeroRequest(
            buffer_id=23,
        )

    ::

        >>> request.to_osc()
        OscMessage('/b_zero', 23)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.BUFFER_ZERO

    ### INITIALIZER ###

    def __init__(self, buffer_id=None, callback=None):
        Request.__init__(self)
        self._buffer_id = int(buffer_id)
        if callback is not None:
            assert isinstance(callback, (Request, RequestBundle))
        self._callback = callback

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        buffer_id = int(self.buffer_id)
        contents = [request_id, buffer_id]
        if self.callback:
            contents.append(self.callback.to_osc())
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def callback(self):
        return self._callback

    @property
    def response_patterns(self):
        return ["/done", "/b_zero", self.buffer_id], None
