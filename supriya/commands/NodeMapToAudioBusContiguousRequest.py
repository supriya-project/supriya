from supriya.commands.Request import Request
from supriya.enums import RequestId


class NodeMapToAudioBusContiguousRequest(Request):

    ### CLASS VARIABLES ###

    __slots__ = ()

    request_id = RequestId.NODE_MAP_TO_AUDIO_BUS_CONTIGUOUS

    ### INITIALIZER ###

    def __init__(self):
        Request.__init__(self)
        raise NotImplementedError

    ### PUBLIC METHODS ###

    def to_osc(self, with_request_name=False):
        raise NotImplementedError
