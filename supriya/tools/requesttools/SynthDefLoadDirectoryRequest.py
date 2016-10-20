# -*- encoding: utf-8 -*-
import os
from supriya.tools import osctools
from supriya.tools.requesttools.Request import Request


class SynthDefLoadDirectoryRequest(Request):
    """
    A /d_loadDir request.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_completion_message',
        '_directory_path',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        completion_message=None,
        directory_path=None,
        ):
        Request.__init__(self)
        Request.__init__(self)
        self._completion_message = completion_message
        self._directory_path = os.path.abspath(directory_path)

    ### PUBLIC METHODS ###

    def to_osc_message(self, with_textual_osc_command=False):
        if with_textual_osc_command:
            request_id = self.request_command
        else:
            request_id = int(self.request_id)
        contents = [
            request_id,
            self.directory_path,
            ]
        if self.completion_message:
            completion_message = self.completion_message.to_datagram()
            completion_message = bytearray(completion_message)
            contents.append(completion_message)
        message = osctools.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def completion_message(self):
        return self._completion_message

    @property
    def response_specification(self):
        from supriya.tools import responsetools
        return {
            responsetools.DoneResponse: {
                'action': ('/d_loadDir',),
                },
            }

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.SYNTHDEF_LOAD_DIR

    @property
    def directory_path(self):
        return self._directory_path
