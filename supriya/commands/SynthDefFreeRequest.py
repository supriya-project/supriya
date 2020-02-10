from supriya.commands.Request import Request
from supriya.enums import RequestId


class SynthDefFreeRequest(Request):
    """
    A /d_free request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.SynthDefFreeRequest(
        ...     synthdef='test',
        ...     )
        >>> request
        SynthDefFreeRequest(
            synthdef='test',
            )

    ::

        >>> request.to_osc()
        OscMessage('/d_free', 'test')

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.SYNTHDEF_FREE

    ### INITIALIZER ###

    def __init__(self, synthdef=None):
        import supriya.synthdefs

        Request.__init__(self)
        prototype = (str, supriya.synthdefs.SynthDef)
        assert isinstance(synthdef, prototype)
        self._synthdef = synthdef

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        import supriya.synthdefs

        request_id = self.request_name
        synthdef = self.synthdef
        if isinstance(synthdef, supriya.synthdefs.SynthDef):
            synthdef = synthdef.actual_name
        message = supriya.osc.OscMessage(request_id, synthdef)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def synthdef(self):
        return self._synthdef
