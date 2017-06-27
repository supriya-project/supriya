from supriya.tools import servertools


class Mixer:

    __slots__ = (
        '_is_allowing_multiple',
        '_mixer_channels',
        '_mixer_channels_by_name',
        '_server',
        )

    def __init__(self, server):
        assert isinstance(server, servertools.Server)
        self._is_allowing_multiple = False
        self._mixer_channels = []
        self._mixer_channels_by_name = {}
        self._server = server

    def allow_multiple(self, state):
        self._is_allowing_multiple = bool(state)
