from supriya.commands.Request import Request
from supriya.enums import RequestId


class GroupDumpTreeRequest(Request):

    ### CLASS VARIABLES ###

    __slots__ = ()

    request_id = RequestId.GROUP_DUMP_TREE

    ### INITIALIZER ###

    def __init__(self):
        Request.__init__(self)
        raise NotImplementedError

    ### PUBLIC METHODS ###

    def to_osc(self, with_request_name=False):
        raise NotImplementedError
