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

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when ID of `expr` equals ID of Supriya object.
        Otherwise false.

        Returns boolean.
        '''
        return id(self) == id(expr)

    def __format__(self, format_specification=''):
        r'''Formats Supriya object.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    def __getstate__(self):
        r'''Gets state of Supriya object.

        Returns dictionary.
        '''
        if hasattr(self, '__dict__'):
            return vars(self)
        state = {}
        for class_ in type(self).__mro__:
            for slot in getattr(class_, '__slots__', ()):
                state[slot] = getattr(self, slot, None)
        return state

    def __hash__(self):
        r'''Hashes Supriya object.

        Required to be explicitely re-defined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return id(self)

    def __repr__(self):
        r'''Gets interpreter representation of Supriya object.

        Returns string.
        '''
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.get_repr_format(self)

    def __setstate__(self, state):
        r'''Sets state of Supriya object.

        Returns none.
        '''
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