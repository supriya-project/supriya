import abc
import supriya.utils


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

    def __repr__(self):
        return supriya.utils.get_object_repr(self, multiline=True)
