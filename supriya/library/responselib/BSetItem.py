# -*- encoding: utf-8 -*-
from supriya.library.responselib.ServerResponse import ServerResponse


class BSetItem(ServerResponse):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_sample_index',
        '_sample_value',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        sample_index=None,
        sample_value=None,
        ):
        self._sample_index = sample_index
        self._sample_value = sample_value

    ### PUBLIC PROPERTIES ###

    @property
    def sample_index(self):
        return self._sample_index

    @property
    def sample_value(self):
        return self._sample_value
