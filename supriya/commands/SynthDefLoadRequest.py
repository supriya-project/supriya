import pathlib

import supriya.osc
from .bases import Request
from .bases import RequestBundle
from supriya.enums import RequestId


class SynthDefLoadRequest(Request):
    """
    A /d_load request.
    """

    ### CLASS VARIABLES ###

    request_id = RequestId.SYNTHDEF_LOAD

    ### INITIALIZER ###

    def __init__(self, callback=None, synthdef_path=None):
        Request.__init__(self)
        if callback is not None:
            assert isinstance(callback, (Request, RequestBundle))
        self._callback = callback
        self._synthdef_path = pathlib.Path(synthdef_path).absolute()

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        contents = [request_id, str(self.synthdef_path)]
        if self.callback:
            contents.append(self.callback.to_osc(with_placeholders=with_placeholders))
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def callback(self):
        return self._callback

    @property
    def response_patterns(self):
        return ["/done", "/d_load"], None

    @property
    def synthdef_path(self):
        return self._synthdef_path
