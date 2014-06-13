# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class Id(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_server',
        '_value',
        )

    ### INITIALIZER ###

    def __init__(self, server, value):
        self._server = server
        self._value = value

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
    def server(self):
        return self._server

    @property
    def value(self):
        return self._value
