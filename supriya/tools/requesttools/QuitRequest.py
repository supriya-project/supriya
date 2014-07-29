# -*- encoding: utf-8 -*-
from supriya.tools import osctools
from supriya.tools.requesttools.Request import Request


class QuitRequest(Request):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        ):
        Request.__init__(self)

    ### PUBLIC METHODS ###

    def to_osc_message(self):
        request_id = int(self.request_id)
        message = osctools.OscMessage(
            request_id,
            )
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def response_specification(self):
        from supriya.tools import responsetools
        return {
            responsetools.DoneResponse: {
                'action': ('/quit',),
                },
#            responsetools.FailResponse: {
#                'failed_command': '/quit',
#                }
            }

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.QUIT