import supriya.osc
from supriya.commands.Request import Request


class QuitRequest(Request):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self):
        Request.__init__(self)

    ### PUBLIC METHODS ###

    def to_osc(self, with_textual_osc_command=False):
        if with_textual_osc_command:
            request_id = self.request_command
        else:
            request_id = int(self.request_id)
        message = supriya.osc.OscMessage(
            request_id,
            )
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def response_patterns(self):
        return [['/done', '/quit']]

    @property
    def request_id(self):
        import supriya.commands
        return supriya.commands.RequestId.QUIT
