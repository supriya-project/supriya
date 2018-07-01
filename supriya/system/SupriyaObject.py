import abc
import uqbar.objects


class SupriyaObject(abc.ABC):
    """
    Abstract base class from which many custom classes inherit.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __repr__(self):
        return uqbar.objects.get_repr(self, multiline=True)
