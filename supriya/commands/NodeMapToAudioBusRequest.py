import supriya.osc
from supriya.enums import RequestId

from .bases import Request


class NodeMapToAudioBusRequest(Request):
    """
    A /n_mapa request.

    ::

        >>> import supriya.commands
        >>> import supriya.realtime
        >>> request = supriya.commands.NodeMapToAudioBusRequest(
        ...     node_id=1000,
        ...     frequency=supriya.realtime.Bus(9, 'audio'),
        ...     phase=supriya.realtime.Bus(10, 'audio'),
        ...     amplitude=supriya.realtime.Bus(11, 'audio'),
        ...     )
        >>> request
        NodeMapToAudioBusRequest(
            amplitude=<- Bus: 11 (audio)>,
            frequency=<- Bus: 9 (audio)>,
            node_id=1000,
            phase=<- Bus: 10 (audio)>,
            )

    ::

        >>> request.to_osc()
        OscMessage('/n_mapa', 1000, 'amplitude', 11, 'frequency', 9, 'phase', 10)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.NODE_MAP_TO_AUDIO_BUS

    ### INITIALIZER ###

    def __init__(self, node_id=None, **kwargs):
        Request.__init__(self)
        self._node_id = node_id
        self._kwargs = dict((name, value) for name, value in kwargs.items())

    ### SPECIAL METHODS ###

    def __getattr__(self, name):
        if name in self._kwargs:
            return self._kwargs[name]
        return object.__getattr__(self, name)

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        node_id = self._sanitize_node_id(self.node_id, with_placeholders)
        contents = []
        for name, bus in sorted(self._kwargs.items()):
            contents.append(name)
            contents.append(int(bus))
        message = supriya.osc.OscMessage(request_id, node_id, *contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def node_id(self):
        return self._node_id
