# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class BusId(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_index',
        '_length',
        '_server',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        index=0,
        length=1,
        server=None,
        ):
        self._index = int(index)
        self._length = int(length)
        self._server = server

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
    def index(self):
        return self._index

    @property
    def length(self):
        return self._length

    @property
    def server(self):
        return self._server
