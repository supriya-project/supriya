# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaValueObject import SupriyaValueObject


class DoneResponse(SupriyaValueObject):

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