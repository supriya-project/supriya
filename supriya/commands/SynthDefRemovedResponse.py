from supriya.commands.Response import Response


class SynthDefRemovedResponse(Response):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_synthdef_name',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        synthdef_name=None,
        osc_message=None,
    ):
        Response.__init__(self, osc_message=osc_message)
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
