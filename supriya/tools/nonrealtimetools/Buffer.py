# -*- encoding: utf-8 -*-
import bisect
from supriya.tools import requesttools
from supriya.tools.nonrealtimetools.SessionObject import SessionObject


class Buffer(SessionObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_buffer_group',
        '_channel_count',
        '_duration',
        '_events',
        '_frame_count',
        '_session',
        '_session_id',
        '_start_offset',
        '_file_path',
        '_starting_frame',
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
        from supriya.tools import nonrealtimetools
        SessionObject.__init__(self, session)
        self._events = {}
        self._session_id = int(session_id)
        if buffer_group is not None:
            assert isinstance(buffer_group, nonrealtimetools.BufferGroup)
        self._buffer_group = buffer_group
        start_offset = start_offset or 0
        self._start_offset = float(start_offset)
        if duration is None:
            duration = float('inf')
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
        event_type = requesttools.BufferCloseRequest
        event_kwargs = dict(
            buffer_id=self,
            )
        self._set_event(event_type, event_kwargs, offset=offset)

    def copy_from(
        self,
        source_buffer_id,
        frame_count=None,
        source_starting_frame=None,
        target_starting_frame=None,
        offset=None,
        ):
        event_type = requesttools.BufferCopyRequest
        event_kwargs = dict(
            frame_count=frame_count,
            source_buffer_id=source_buffer_id,
            source_starting_frame=source_starting_frame,
            target_buffer_id=self,
            target_starting_frame=target_starting_frame,
            )
        self._set_event(event_type, event_kwargs, offset=offset)

    def copy_to(
        self,
        target_buffer_id,
        frame_count=None,
        source_starting_frame=None,
        target_starting_frame=None,
        offset=None,
        ):
        event_type = requesttools.BufferCopyRequest
        event_kwargs = dict(
            frame_count=frame_count,
            source_buffer_id=self,
            source_starting_frame=source_starting_frame,
            target_buffer_id=target_buffer_id,
            target_starting_frame=target_starting_frame,
            )
        self._set_event(event_type, event_kwargs, offset=offset)

    def fill(
        self,
        index_count_value_triples=None,
        offset=None,
        ):
        event_type = requesttools.BufferFillRequest
        event_kwargs = dict(
            buffer_id=self,
            index_count_value_triples=index_count_value_triples,
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
        event_type = requesttools.BufferGenerateRequest
        event_kwargs = dict(
            amplitudes=tuple(float(_) for _ in amplitudes),
            as_wavetable=bool(as_wavetable),
            buffer_id=self,
            command_name='cheby',
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
        event_type = requesttools.BufferGenerateRequest
        event_kwargs = dict(
            amplitudes=tuple(float(_) for _ in amplitudes),
            as_wavetable=bool(as_wavetable),
            buffer_id=self,
            command_name='sine1',
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
        event_type = requesttools.BufferGenerateRequest
        event_kwargs = dict(
            amplitudes=tuple(float(_) for _ in amplitudes),
            as_wavetable=bool(as_wavetable),
            buffer_id=self,
            command_name='sine2',
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
        event_type = requesttools.BufferGenerateRequest
        event_kwargs = dict(
            amplitudes=tuple(float(_) for _ in amplitudes),
            as_wavetable=bool(as_wavetable),
            buffer_id=self,
            command_name='sine3',
            frequencies=tuple(float(_) for _ in frequencies),
            phases=tuple(float(_) for _ in phases),
            should_clear_first=bool(should_clear_first),
            should_normalize=bool(should_normalize),
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
        event_type = requesttools.BufferReadRequest
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

    def set(
        self,
        index_value_pairs=None,
        offset=None,
        ):
        event_type = requesttools.BufferSetRequest
        event_kwargs = dict(
            buffer_id=self,
            index_value_pairs=index_value_pairs,
            )
        self._set_event(event_type, event_kwargs, offset=offset)

    def set_contiguous(
        self,
        index_values_pairs=None,
        offset=None,
        ):
        event_type = requesttools.BufferSetContiguousRequest
        event_kwargs = dict(
            buffer_id=self,
            index_values_pairs=index_values_pairs,
            )
        self._set_event(event_type, event_kwargs, offset=offset)

    def write(
        self,
        file_path,
        frame_count=None,
        header_format='aiff',
        leave_open=False,
        sample_format='int24',
        starting_frame=None,
        offset=None,
        ):
        event_type = requesttools.BufferWriteRequest
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
        event_type = requesttools.BufferZeroRequest
        event_kwargs = dict(
            buffer_id=self,
            )
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
