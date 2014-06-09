# -*- encoding: utf-8 -*-
import abc


AbstractBase = abc.ABCMeta(
    'AbstractBase',
    (),
    {
        '__metaclass__': abc.ABCMeta,
        '__module__': __name__,
        '__slots__': (),
        },
    )


class SupriyaObject(AbstractBase):
    '''Abstract base class from which many custom classes inherit.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        return id(self) == id(expr)

    def __format__(self, format_specification=''):
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    def __getstate__(self):
        if hasattr(self, '__dict__'):
            return vars(self)
        state = {}
        for class_ in type(self).__mro__:
            for slot in getattr(class_, '__slots__', ()):
                state[slot] = getattr(self, slot, None)
        return state

    def __repr__(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.get_repr_format(self)

    def __setstate__(self, state):
        for key, value in state.items():
            setattr(self, key, value)

    ### PRIVATE PROPERTIES ###

    @property
    def _repr_specification(self):
        return self._storage_format_specification

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(self)
