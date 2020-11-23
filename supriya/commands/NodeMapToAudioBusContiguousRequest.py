from supriya.enums import RequestId

from .bases import Request


class NodeMapToAudioBusContiguousRequest(Request):

    ### CLASS VARIABLES ###

    request_id = RequestId.NODE_MAP_TO_AUDIO_BUS_CONTIGUOUS

    ### INITIALIZER ###

    def __init__(self):
        Request.__init__(self)
        raise NotImplementedError

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        raise NotImplementedError
