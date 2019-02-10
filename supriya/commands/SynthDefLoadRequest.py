import pathlib

import supriya.osc
from supriya.commands.Request import Request
from supriya.commands.RequestBundle import RequestBundle
from supriya.enums import RequestId


class SynthDefLoadRequest(Request):
    """
    A /d_load request.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_callback", "_synthdef_path")

    request_id = RequestId.SYNTHDEF_LOAD

    ### INITIALIZER ###

    def __init__(self, callback=None, synthdef_path=None):
        Request.__init__(self)
        if callback is not None:
            assert isinstance(callback, (Request, RequestBundle))
        self._callback = callback
        self._synthdef_path = pathlib.Path(synthdef_path).absolute()

    ### PUBLIC METHODS ###

    def to_osc(self, with_request_name=False):
        if with_request_name:
            request_id = self.request_name
        else:
            request_id = int(self.request_id)
        contents = [request_id, str(self.synthdef_path)]
        if self.callback:
            contents.append(self.callback.to_osc())
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def callback(self):
        return self._callback

    @property
    def response_patterns(self):
        return [["/done", "/d_load"]]

    @property
    def synthdef_path(self):
        return self._synthdef_path
