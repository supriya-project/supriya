# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class BufferProxy(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_buffer_',
        '_index',
        )

    ### INITIALIZER ###

    def __init__(self,
        buffer_=None,
        index=None,
        ):
        self._buffer_ = buffer_
        self._index = index

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.compare(self, expr)

    def __hash__(self):
        from abjad.tools import systemtools
        hash_values = systemtools.StorageFormatManager.get_hash_values(self)
        return hash(hash_values)

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_(self):
        return self._buffer_

    @property
    def index(self):
        return self._index
