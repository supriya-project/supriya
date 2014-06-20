# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class BufferProxy(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_buffer_id',
        '_channel_count',
        '_frame_count',
        '_sample_rate',
        '_server',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        channel_count=0,
        frame_count=0,
        sample_rate=0,
        server=None,
        ):
        from supriya.tools import servertools
        buffer_id = int(buffer_id)
        assert 0 <= buffer_id
        assert isinstance(server, servertools.Server)
        self._buffer_id = int(buffer_id)
        self._channel_count = int(channel_count)
        self._frame_count = int(frame_count)
        self._sample_rate = int(sample_rate)
        self._server = server

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.compare(self, expr)

    def __float__(self):
        return float(self.buffer_id)

    def __hash__(self):
        from abjad.tools import systemtools
        hash_values = systemtools.StorageFormatManager.get_hash_values(self)
        return hash(hash_values)

    def __int__(self):
        return int(self.buffer_id)

    ### PUBLIC METHODS ###

    def handle_response(self, response):
        from supriya.tools import responsetools
        assert response.buffer_id == self.buffer_id
        if isinstance(response, responsetools.BufferInfoResponse):
            self._channel_count = response.channel_count
            self._frame_count = response.frame_count
            self._sample_rate = response.sample_rate

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def channel_count(self):
        return self._channel_count

    @property
    def frame_count(self):
        return self._frame_count

    @property
    def sample_rate(self):
        return self._sample_rate

    @property
    def server(self):
        return self._server
