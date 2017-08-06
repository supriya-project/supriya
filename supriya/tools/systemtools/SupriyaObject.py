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

    __slots__ = (
        '__weakref__',
        )

    ### SPECIAL METHODS ###

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

    def __repr__(self):
        """
        Gets interpreter representation of Supriya object.

        Returns string.
        """
        from abjad.tools import systemtools
        return systemtools.StorageFormatAgent(self).get_repr_format()

    ### PRIVATE PROPERTIES ###

    def _get_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.FormatSpecification(
            client=self,
            repr_is_indented=True,
            )
