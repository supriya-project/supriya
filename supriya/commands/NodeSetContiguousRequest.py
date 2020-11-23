from supriya.enums import RequestId

from .bases import Request


class NodeSetContiguousRequest(Request):

    ### CLASS VARIABLES ###

    request_id = RequestId.NODE_SET_CONTIGUOUS

    ### INITIALIZER ###

    def __init__(self):
        Request.__init__(self)
        raise NotImplementedError

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        raise NotImplementedError
