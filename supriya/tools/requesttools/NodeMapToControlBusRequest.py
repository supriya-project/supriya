# -*- encoding: utf-8 -*-
from supriya.tools import osctools
from supriya.tools.requesttools.Request import Request


class NodeMapToControlBusRequest(Request):
    r'''A /n_map request.

    ::

        >>> from supriya.tools import requesttools
        >>> from supriya.tools import servertools
        >>> request = requesttools.NodeMapToControlBusRequest(
        ...     node_id=1000,
        ...     frequency=servertools.Bus(9, 'control'),
        ...     phase=servertools.Bus(10, 'control'),
        ...     amplitude=servertools.Bus(11, 'control'),
        ...     )
        >>> request
        NodeMapToControlBusRequest(
            node_id=1000,
            amplitude=11,
            frequency=9,
            phase=10
            )

    ::

        >>> message = request.to_osc_message()
        >>> message
        OscMessage(14, 1000, 'amplitude', 11, 'frequency', 9, 'phase', 10)

    ::

        >>> message.address == \
        ...     requesttools.RequestId.NODE_MAP_TO_CONTROL_BUS
        True

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_kwargs',
        '_node_id',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        node_id=None,
        **kwargs
        ):
        Request.__init__(self)
        self._node_id = node_id
        self._kwargs = dict(
            (name, int(value))
            for name, value in kwargs.items()
            )

    ### SPECIAL METHODS ###

    def __getattr__(self, name):
        if name in self._kwargs:
            return self._kwargs[name]
        return object.__getattr__(self, name)

    ### PRIVATE METHODS ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        manager = systemtools.StorageFormatManager
        keyword_argument_names = tuple(
            manager.get_keyword_argument_names(self))
        keyword_argument_names += tuple(sorted(self._kwargs.keys()))
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=keyword_argument_names,
            )

    ### PUBLIC METHODS ###

    def to_osc_message(self):
        request_id = int(self.request_id)
        node_id = int(self.node_id)
        contents = []
        for name, bus in sorted(self._kwargs.items()):
            contents.append(name)
            contents.append(int(bus))
        message = osctools.OscMessage(
            request_id,
            node_id,
            *contents
            )
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def node_id(self):
        return self._node_id

    @property
    def response_specification(self):
        return None

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.NODE_MAP_TO_CONTROL_BUS