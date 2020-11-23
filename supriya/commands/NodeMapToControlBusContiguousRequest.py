from .bases import Request
from supriya.enums import RequestId


class NodeMapToControlBusContiguousRequest(Request):

    ### CLASS VARIABLES ###

    request_id = RequestId.NODE_MAP_TO_CONTROL_BUS_CONTIGUOUS

    ### INITIALIZER ###

    def __init__(self):
        Request.__init__(self)
        raise NotImplementedError

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        raise NotImplementedError
