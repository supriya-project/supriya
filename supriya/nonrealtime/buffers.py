import bisect

import supriya.commands
from supriya.nonrealtime.bases import SessionObject


class Buffer(SessionObject):
    """
    A non-realtime buffer.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_buffer_group",
        "_channel_count",
        "_duration",
        "_events",
        "_frame_count",
        "_session",
        "_session_id",
        "_start_offset",
        "_file_path",
        "_starting_frame",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        session,
        session_id,
        buffer_group=None,
        channel_count=None,
        frame_count=1,
        duration=None,
        start_offset=None,
        file_path=None,
        starting_frame=None,
    ):
        SessionObject.__init__(self, session)
        self._events = {}
        self._session_id = int(session_id)
        if buffer_group is not None:
            assert isinstance(buffer_group, BufferGroup)
        self._buffer_group = buffer_group
        start_offset = start_offset or 0
        self._start_offset = float(start_offset)
        if duration is None:
            duration = float("inf")
        self._duration = duration
        if file_path is not None:
            starting_frame = int(starting_frame or 0)
        else:
            channel_count = int(channel_count or 1)
            frame_count = int(frame_count or 1)
        self._frame_count = frame_count
        self._channel_count = channel_count
        self._starting_frame = starting_frame
        self._file_path = file_path

    ### PRIVATE METHODS ###

    @SessionObject.require_offset
    def _set_event(self, item, value, offset=None):
        if offset < 0 or self.duration < offset:
            return
        events = self._events.setdefault(item, [])
        new_event = (offset, value)
        if not events:
            events.append(new_event)
            return
        index = bisect.bisect_left(events, new_event)
        if len(events) <= index:
            events.append(new_event)
        old_offset, old_value = events[index]
        if old_offset == offset:
            events[index] = (offset, value)
        else:
            events.insert(index, new_event)

    ### PUBLIC METHODS ###

    def close(self, offset=None):
        event_type = supriya.commands.BufferCloseRequest
        event_kwargs = dict(buffer_id=self)
        self._set_event(event_type, event_kwargs, offset=offset)

    def copy(
        self,
        target_buffer_id,
        frame_count=None,
        source_starting_frame=None,
        target_starting_frame=None,
        offset=None,
    ):
        event_type = supriya.commands.BufferCopyRequest
        event_kwargs = dict(
            frame_count=frame_count,
            source_buffer_id=self,
            source_starting_frame=source_starting_frame,
            target_buffer_id=target_buffer_id,
            target_starting_frame=target_starting_frame,
        )
        self._set_event(event_type, event_kwargs, offset=offset)

    def fill(self, index_count_value_triples=None, offset=None):
        event_type = supriya.commands.BufferFillRequest
        event_kwargs = dict(
            buffer_id=self, index_count_value_triples=index_count_value_triples
        )
        self._set_event(event_type, event_kwargs, offset=offset)

    def fill_via_chebyshev(
        self,
        amplitudes,
        as_wavetable=True,
        should_normalize=True,
        should_clear_first=True,
        offset=None,
    ):
        event_type = supriya.commands.BufferGenerateRequest
        event_kwargs = dict(
            amplitudes=tuple(float(_) for _ in amplitudes),
            as_wavetable=bool(as_wavetable),
            buffer_id=self,
            command_name="cheby",
            should_clear_first=bool(should_clear_first),
            should_normalize=bool(should_normalize),
        )
        self._set_event(event_type, event_kwargs, offset=offset)

    def fill_via_sine_1(
        self,
        amplitudes,
        as_wavetable=True,
        should_clear_first=True,
        should_normalize=True,
        offset=None,
    ):
        event_type = supriya.commands.BufferGenerateRequest
        event_kwargs = dict(
            amplitudes=tuple(float(_) for _ in amplitudes),
            as_wavetable=bool(as_wavetable),
            buffer_id=self,
            command_name="sine1",
            should_clear_first=bool(should_clear_first),
            should_normalize=bool(should_normalize),
        )
        self._set_event(event_type, event_kwargs, offset=offset)

    def fill_via_sine_2(
        self,
        amplitudes,
        frequencies,
        as_wavetable=True,
        should_clear_first=True,
        should_normalize=True,
        offset=None,
    ):
        event_type = supriya.commands.BufferGenerateRequest
        event_kwargs = dict(
            amplitudes=tuple(float(_) for _ in amplitudes),
            as_wavetable=bool(as_wavetable),
            buffer_id=self,
            command_name="sine2",
            frequencies=tuple(float(_) for _ in frequencies),
            should_clear_first=bool(should_clear_first),
            should_normalize=bool(should_normalize),
        )
        self._set_event(event_type, event_kwargs, offset=offset)

    def fill_via_sine_3(
        self,
        amplitudes,
        frequencies,
        phases,
        as_wavetable=True,
        should_clear_first=True,
        should_normalize=True,
        offset=None,
    ):
        event_type = supriya.commands.BufferGenerateRequest
        event_kwargs = dict(
            amplitudes=tuple(float(_) for _ in amplitudes),
            as_wavetable=bool(as_wavetable),
            buffer_id=self,
            command_name="sine3",
            frequencies=tuple(float(_) for _ in frequencies),
            phases=tuple(float(_) for _ in phases),
            should_clear_first=bool(should_clear_first),
            should_normalize=bool(should_normalize),
        )
        self._set_event(event_type, event_kwargs, offset=offset)

    def normalize(
        self, as_wavetable=None, buffer_id=None, new_maximum=1.0, offset=None
    ):
        event_type = supriya.commands.BufferNormalizeRequest
        event_kwargs = dict(
            buffer_id=self, new_maximum=new_maximum, as_wavetable=as_wavetable
        )
        self._set_event(event_type, event_kwargs, offset=offset)

    def read(
        self,
        file_path,
        channel_indices=None,
        frame_count=None,
        leave_open=None,
        starting_frame_in_buffer=None,
        starting_frame_in_file=None,
        offset=None,
    ):
        event_type = supriya.commands.BufferReadRequest
        # need to optionally coerce to BufferReadChannelRequest on compile
        event_kwargs = dict(
            buffer_id=self,
            file_path=file_path,
            channel_indices=channel_indices,
            frame_count=frame_count,
            leave_open=leave_open,
            starting_frame_in_buffer=starting_frame_in_buffer,
            starting_frame_in_file=starting_frame_in_file,
        )
        self._set_event(event_type, event_kwargs, offset=offset)

    def set(self, index_value_pairs=None, offset=None):
        event_type = supriya.commands.BufferSetRequest
        event_kwargs = dict(buffer_id=self, index_value_pairs=index_value_pairs)
        self._set_event(event_type, event_kwargs, offset=offset)

    def set_contiguous(self, index_values_pairs=None, offset=None):
        event_type = supriya.commands.BufferSetContiguousRequest
        event_kwargs = dict(buffer_id=self, index_values_pairs=index_values_pairs)
        self._set_event(event_type, event_kwargs, offset=offset)

    def write(
        self,
        file_path,
        frame_count=None,
        header_format="aiff",
        leave_open=False,
        sample_format="int24",
        starting_frame=None,
        offset=None,
    ):
        event_type = supriya.commands.BufferWriteRequest
        event_kwargs = dict(
            buffer_id=self,
            file_path=file_path,
            frame_count=frame_count,
            header_format=header_format,
            leave_open=leave_open,
            sample_format=sample_format,
            starting_frame=starting_frame,
        )
        self._set_event(event_type, event_kwargs, offset=offset)

    def zero(self, offset=None):
        event_type = supriya.commands.BufferZeroRequest
        event_kwargs = dict(buffer_id=self)
        self._set_event(event_type, event_kwargs, offset=offset)

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_group(self):
        return self._buffer_group

    @property
    def channel_count(self):
        return self._channel_count

    @property
    def duration(self):
        return self._duration

    @property
    def frame_count(self):
        return self._frame_count

    @property
    def session_id(self):
        return self._session_id

    @property
    def start_offset(self):
        return self._start_offset

    @property
    def starting_frame(self):
        return self._starting_frame

    @property
    def file_path(self):
        return self._file_path

    @property
    def stop_offset(self):
        if self.duration is None:
            return None
        return self.start_offset + self.duration


class BufferGroup(SessionObject):
    """
    A non-realtime buffer group.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_buffers", "_session")

    ### INITIALIZER ###

    def __init__(
        self,
        session,
        buffer_count=1,
        duration=None,
        channel_count=1,
        frame_count=1,
        start_offset=None,
    ):
        import supriya.nonrealtime

        SessionObject.__init__(self, session)
        buffer_count = int(buffer_count)
        assert 0 < buffer_count
        buffers = []
        start_id = len(self.session.buffers)
        for session_id in range(start_id, buffer_count + start_id):
            buffer_ = supriya.nonrealtime.Buffer(
                session,
                session_id=session_id,
                buffer_group=self,
                duration=duration,
                channel_count=channel_count,
                frame_count=frame_count,
                start_offset=start_offset,
            )
            buffers.append(buffer_)
        self._buffers = tuple(buffers)

    ### SPECIAL METHODS ###

    def __contains__(self, item):
        return self.buffers.__contains__(item)

    def __getitem__(self, item):
        if isinstance(item, int):
            return self._buffers[item]
        elif isinstance(item, slice):
            return tuple(self._buffers[item])

    def __iter__(self):
        for buffer in self._buffers:
            yield buffer

    def __len__(self):
        return len(self._buffers)

    ### PUBLIC METHODS ###

    def index(self, buffer_):
        return self._buffers.index(buffer_)

    ### PUBLIC PROPERTIES ###

    @property
    def buffers(self):
        return self._buffers

    @property
    def buffer_count(self):
        return len(self)

    @property
    def channel_count(self):
        return self._buffers[0].channel_count

    @property
    def duration(self):
        return self._buffers[0].duration

    @property
    def frame_count(self):
        return self._buffers[0].frame_count

    @property
    def start_offset(self):
        return self._buffers[0].start_offset

    @property
    def stop_offset(self):
        return self._buffers[0].stop_offset
