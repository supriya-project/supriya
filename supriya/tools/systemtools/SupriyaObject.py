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
    """
    Abstract base class from which many custom classes inherit.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        """
        Is true when ID of `expr` equals ID of Supriya object.
        Otherwise false.

        Returns boolean.
        """
        return id(self) == id(expr)

    def __format__(self, format_specification=''):
        """
        Formats Supriya object.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        """
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatAgent(self).get_storage_format()
        return str(self)

    def __getstate__(self):
        """
        Gets state of Supriya object.

        Returns dictionary.
        """
        if hasattr(self, '__dict__'):
            state = vars(self).copy()
        else:
            state = {}
        for class_ in type(self).__mro__:
            for slot in getattr(class_, '__slots__', ()):
                try:
                    state[slot] = getattr(self, slot)
                except AttributeError:
                    pass
        return state

    def __hash__(self):
        """
        Hashes Supriya object.

        Required to be explicitely re-defined on Python 3 if __eq__ changes.

        Returns integer.
        """
        return super(SupriyaObject, self).__hash__()

    def __repr__(self):
        """
        Gets interpreter representation of Supriya object.

        Returns string.
        """
        from abjad.tools import systemtools
        return systemtools.StorageFormatAgent(self).get_repr_format()

    def __setstate__(self, state):
        """
        Sets state of Supriya object.

        Returns none.
        """
        for key, value in state.items():
            setattr(self, key, value)

    ### PRIVATE PROPERTIES ###

    def _get_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.FormatSpecification(
            client=self,
            repr_is_indented=True,
            )
