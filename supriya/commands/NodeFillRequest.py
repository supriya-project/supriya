from .bases import Request
from supriya.enums import RequestId


class NodeFillRequest(Request):

    ### CLASS VARIABLES ###

    request_id = RequestId.NODE_FILL

    ### INITIALIZER ###

    def __init__(self):
        Request.__init__(self)
        raise NotImplementedError

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        raise NotImplementedError
