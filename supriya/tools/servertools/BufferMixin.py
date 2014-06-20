# -*- encoding: utf-8 -*-
import abc
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class BufferMixin(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __float__(self):
        return float(self.buffer_id)

    def __int__(self):
        return int(self.buffer_id)

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def buffer_id(self):
        return self._buffer_id
        raise NotImplementedError
