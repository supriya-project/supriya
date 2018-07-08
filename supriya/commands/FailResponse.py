from supriya.commands.Response import Response


class FailResponse(Response):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_failed_command',
        '_failure_reason',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        failed_command=None,
        failure_reason=None,
        osc_message=None,
    ):
        Response.__init__(self, osc_message=osc_message)
        self._failed_command = failed_command
        self._failure_reason = failure_reason

    ### PUBLIC METHODS ###

    @classmethod
    def from_osc_message(cls, osc_message):
        failed_command = osc_message.contents[0]
        failure_reason = osc_message.contents[1:]
        if failure_reason:
            failure_reason = tuple(failure_reason)
        response = cls(
            failed_command=failed_command,
            failure_reason=failure_reason,
            )
        return response

    ### PUBLIC PROPERTIES ###

    @property
    def failed_command(self):
        return self._failed_command

    @property
    def failure_reason(self):
        return self._failure_reason
