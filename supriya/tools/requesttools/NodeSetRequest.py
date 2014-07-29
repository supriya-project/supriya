# -*- encoding: utf-8 -*-
from supriya.tools import osctools
from supriya.tools.requesttools.Request import Request


class NodeSetRequest(Request):
    r'''A /n_set request.

    ::

        >>> from supriya.tools import requesttools
        >>> request = requesttools.NodeSetRequest(
        ...     1000,
        ...     frequency=443.1,
        ...     phase=0.5,
        ...     amplitude=0.1,
        ...     )
        >>> request
        NodeSetRequest(
            node_id=1000,
            amplitude=0.1,
            frequency=443.1,
            phase=0.5
            )

    ::

        >>> message = request.to_osc_message()
        >>> message
        OscMessage(15, 1000, 'amplitude', 0.1, 'frequency', 443.1, 'phase', 0.5)

    ::

        >>> message.address == requesttools.RequestId.NODE_SET
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
        self._kwargs = kwargs

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
        contents = [
            request_id,
            node_id,
            ]
        for key, value in sorted(self._kwargs.items()):
            contents.append(key)
            contents.append(value)
        message = osctools.OscMessage(*contents)
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
        return requesttools.RequestId.NODE_SET