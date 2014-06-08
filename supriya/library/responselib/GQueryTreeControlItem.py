# -*- encoding: utf-8 -*-
from supriya.library.responselib.ServerResponse import ServerResponse


class GQueryTreeControlItem(ServerResponse):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_control_value',
        '_control_name_or_index',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        control_name_or_index=None,
        control_value=None,
        ):
        self._control_value = control_value
        self._control_name_or_index = control_name_or_index

    ### PUBLIC PROPERTIES ###

    @property
    def control_name_or_index(self):
        return self._control_name_or_index

    @property
    def control_value(self):
        return self._control_value
