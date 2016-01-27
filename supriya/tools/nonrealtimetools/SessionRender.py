# -*- encoding: utf-8 -*-
from supriya.tools import soundfiletools
from supriya.tools.systemtools import SupriyaValueObject


class SessionRender(SupriyaValueObject):

    __slots__ = (
        '_debug',
        '_header_format',
        '_sample_format',
        '_sample_rate',
        '_server_options',
        '_session',
        '_duration',
        )

    def __init__(
        self,
        session,
        duration=None,
        sample_rate=44100,
        header_format=soundfiletools.HeaderFormat.AIFF,
        sample_format=soundfiletools.SampleFormat.INT24,
        debug=False,
        **server_options
        ):
        from supriya.tools import nonrealtimetools
        assert isinstance(session, nonrealtimetools.Session)
        self._header_format = soundfiletools.HeaderFormat.from_expr(header_format)
        self._sample_format = soundfiletools.SampleFormat.from_expr(sample_format)
        self._sample_rate = int(sample_rate)
        self._server_options = tuple(sorted(server_options.items()))
        self.duration = duration
