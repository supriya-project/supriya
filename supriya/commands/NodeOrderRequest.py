from supriya.enums import RequestId

from .bases import Request


class NodeOrderRequest(Request):

    ### CLASS VARIABLES ###

    request_id = RequestId.NODE_ORDER

    ### INITIALIZER ###

    def __init__(self):
        Request.__init__(self)
        raise NotImplementedError

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        raise NotImplementedError
