from .bases import Response


class SynthDefRemovedResponse(Response):

    ### CLASS VARIABLES ###

    ### INITIALIZER ###

    def __init__(self, synthdef_name=None):
        Response.__init__(self)
        self._synthdef_name = synthdef_name

    ### PUBLIC METHODS ###

    @classmethod
    def from_osc_message(cls, osc_message):
        synthdef_name = osc_message.contents[0]
        response = cls(synthdef_name=synthdef_name)
        return response

    ### PUBLIC PROPERTIES ###

    @property
    def synthdef_name(self):
        return self._synthdef_name
