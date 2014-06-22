# -*- encoding: utf-8 -*-
import abc
from supriya.tools.ugentools.InfoUGenBase import InfoUGenBase


class BufInfoUGenBase(InfoUGenBase):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'buffer_number',
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(
        self,
        buffer_number=None,
        rate=None,
        ):
        InfoUGenBase.__init__(
            self,
            buffer_number=buffer_number,
            rate=rate,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ir(cls, buffer_number=None):
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.SCALAR
        ugen = cls._new_expanded(
            buffer_number=buffer_number,
            rate=rate,
            )
        return ugen

    @classmethod
    def kr(cls, buffer_number=None):
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.CONTROL
        ugen = cls._new_expanded(
            buffer_number=buffer_number,
            rate=rate,
            )
        return ugen
