# -*- enoding: utf-8 -*-
from supriya.nonrealtime.SessionObject import SessionObject


class BufferGroup(SessionObject):
    """
    A non-realtime buffer group.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Session Objects'

    __slots__ = (
        '_buffers',
        '_session',
        )

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
