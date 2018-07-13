import supriya.osc
from supriya.commands.Request import Request


class ClearScheduleRequest(Request):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self):
        Request.__init__(self)

    ### PUBLIC METHODS ###

    def to_osc_message(self, with_textual_osc_command=False):
        if with_textual_osc_command:
            request_id = self.request_command
        else:
            request_id = int(self.request_id)
        contents = [request_id]
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def request_id(self):
        import supriya.commands
        return supriya.commands.RequestId.CLEAR_SCHEDULE
