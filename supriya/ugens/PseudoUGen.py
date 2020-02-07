import abc

from supriya.system import SupriyaObject


class PseudoUGen(SupriyaObject):

    ### CLASS VARIABLES ###

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError
