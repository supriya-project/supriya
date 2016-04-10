# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class SupriyaValueObject(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        from abjad.tools.topleveltools import new
        return new(self)

    def __eq__(self, expr):
        from abjad.tools import systemtools
        return systemtools.TestManager.compare_objects(self, expr)

    def __hash__(self, expr):
        from abjad.tools import systemtools
        hash_values = systemtools.StorageFormatAgent(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            message = 'unhashable type: {}'.format(self)
            raise TypeError(message)
        return result
