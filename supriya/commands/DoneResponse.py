from .bases import Response


class DoneResponse(Response):

    ### INITIALIZER ###

    def __init__(self, action=None):
        self._action = action

    ### PUBLIC METHODS ###

    @classmethod
    def from_osc_message(cls, osc_message):
        arguments = osc_message.contents
        response = cls(action=tuple(arguments))
        return response

    ### PUBLIC PROPERTIES ###

    @property
    def action(self):
        return self._action
