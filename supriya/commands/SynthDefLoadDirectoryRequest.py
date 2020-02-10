import pathlib

import supriya.osc
from supriya.commands.Request import Request
from supriya.commands.RequestBundle import RequestBundle
from supriya.enums import RequestId


class SynthDefLoadDirectoryRequest(Request):
    """
    A /d_loadDir request.
    """

    ### CLASS VARIABLES ###

    request_id = RequestId.SYNTHDEF_LOAD_DIR

    ### INITIALIZER ###

    def __init__(self, callback=None, directory_path=None):
        Request.__init__(self)
        if callback is not None:
            assert isinstance(callback, (Request, RequestBundle))
        self._callback = callback
        self._directory_path = pathlib.Path(directory_path).absolute()

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        contents = [request_id, str(self.directory_path)]
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
        return ["/done", "/d_loadDir"], None

    @property
    def directory_path(self):
        return self._directory_path
