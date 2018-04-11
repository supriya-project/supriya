import abc
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class PseudoUGen(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError
