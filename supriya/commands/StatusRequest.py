import supriya.osc
from supriya.commands.Request import Request


class StatusRequest(Request):
    """
    A /status request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.StatusRequest()
        >>> request
        StatusRequest()

    ::

        >>> message = request.to_osc_message()
        >>> message
        OscMessage(2)

    ::

        >>> message.address == supriya.commands.RequestId.STATUS
        True

    """

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
        message = supriya.osc.OscMessage(
            request_id,
            )
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def request_id(self):
        import supriya.commands
        return supriya.commands.RequestId.STATUS
