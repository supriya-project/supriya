# -*- encoding: utf-8 -*-
from supriya.library.responselib.ServerResponse import ServerResponse


class DoneResponse(ServerResponse):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_action',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        action=None,
        ):
        self._action = action

    ### PUBLIC PROPERTIES ###

    @property
    def action(self):
        return self._action
