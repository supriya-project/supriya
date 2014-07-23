# -*- encoding: utf-8 -*-
import abc
from supriya.tools.systemtools.SupriyaValueObject import SupriyaValueObject


class Request(SupriyaValueObject):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _prototype = None

    ### INITIALIZER ###

    def __init__(
        self,
        ):
        pass

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def to_osc_message(self):
        raise NotImplementedError