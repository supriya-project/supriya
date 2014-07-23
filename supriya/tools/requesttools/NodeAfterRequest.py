# -*- encoding: utf-8 -*-
from supriya.tools.requesttools.Request import Request


class NodeAfterRequest(Request):

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(
        self,
        ):
        pass

    ### PUBLIC METHODS ###

    def as_osc_message(self):
        from supriya.tools import servertools
        manager = servertools.RequestManager
        message = manager.make_node_after_message()
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def response_prototype(self):
        return None

    @property
    def request_number(self):
        from supriya.tools import servertools
        return servertools.RequestId.NODE_AFTER