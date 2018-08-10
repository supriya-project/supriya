import abc
import uqbar.objects
from typing import Optional


class SupriyaObject(metaclass=abc.ABCMeta):
    """
    Abstract base class from which many custom classes inherit.
    """

    ### CLASS VARIABLES ###

    __documentation_section__: Optional[str] = None

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __repr__(self):
        return uqbar.objects.get_repr(self, multiline=True)
