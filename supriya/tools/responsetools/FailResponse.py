# -*- encoding: utf-8 -*-
from supriya.tools.responsetools.Response import Response


class FailResponse(Response):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_failed_command',
        '_failure_reason',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        failed_command=None,
        failure_reason=None,
        ):
        self._failed_command = failed_command
        self._failure_reason = failure_reason

    ### PUBLIC PROPERTIES ###

    @property
    def failed_command(self):
        return self._failed_command

    @property
    def failure_reason(self):
        return self._failure_reason
