import pathlib
import supriya.osc
from supriya.commands.Request import Request
from supriya.commands.RequestBundle import RequestBundle


class SynthDefLoadDirectoryRequest(Request):
    """
    A /d_loadDir request.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_callback',
        '_directory_path',
        )

    ### INITIALIZER ###

    def __init__(self, callback=None, directory_path=None):
        Request.__init__(self)
        if callback is not None:
            assert isinstance(callback, (Request, RequestBundle))
        self._callback = callback
        self._directory_path = pathlib.Path(directory_path).absolute()

    ### PUBLIC METHODS ###

    def to_osc_message(self, with_textual_osc_command=False):
        if with_textual_osc_command:
            request_id = self.request_command
        else:
            request_id = int(self.request_id)
        contents = [
            request_id,
            str(self.directory_path),
            ]
        if self.callback:
            contents.append(bytearray(self.callback.to_datagram()))
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def callback(self):
        return self._callback

    @property
    def response_patterns(self):
        return [['/done', '/d_loadDir']]

    @property
    def request_id(self):
        import supriya.commands
        return supriya.commands.RequestId.SYNTHDEF_LOAD_DIR

    @property
    def directory_path(self):
        return self._directory_path
