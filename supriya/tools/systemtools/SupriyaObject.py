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
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatAgent(self).get_storage_format()
        return str(self)

    def __repr__(self):
        #from abjad.tools import systemtools
        #return systemtools.StorageFormatAgent(self).get_repr_format()
        import supriya.utils
        return supriya.utils.get_object_repr(self, multiline=True)

    ### PRIVATE PROPERTIES ###

    def _get_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.FormatSpecification(
            client=self,
            repr_is_indented=True,
            )
