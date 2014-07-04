# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaValueObject import SupriyaValueObject


class BufferSetContiguousItem(SupriyaValueObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_sample_values',
        '_starting_sample_index',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        starting_sample_index=None,
        sample_values=None
        ):
        self._sample_values = sample_values
        self._starting_sample_index = starting_sample_index

    ### PUBLIC PROPERTIES ###

    @property
    def sample_values(self):
        return self._sample_values

    @property
    def starting_sample_index(self):
        return self._starting_sample_index
