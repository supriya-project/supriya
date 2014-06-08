# -*- encoding: utf-8 -*-
from supriya.library.responselib.ServerResponse import ServerResponse


class NSetnItem(ServerResponse):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_control_values',
        '_starting_control_index_or_name',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        starting_control_index_or_name=None,
        control_values=None,
        ):
        self._control_values = control_values
        self._starting_control_index_or_name = starting_control_index_or_name

    ### PUBLIC PROPERTIES ###

    @property
    def control_values(self):
        return self._control_values

    @property
    def starting_control_index_or_name(self):
        return self._starting_control_index_or_name
