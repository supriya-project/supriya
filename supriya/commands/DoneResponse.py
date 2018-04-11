from supriya.commands.Response import Response


class DoneResponse(Response):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_action',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        action=None,
        osc_message=None,
        ):
        Response.__init__(
            self,
            osc_message=osc_message,
            )
        self._action = action

    ### PUBLIC PROPERTIES ###

    @property
    def action(self):
        return self._action
