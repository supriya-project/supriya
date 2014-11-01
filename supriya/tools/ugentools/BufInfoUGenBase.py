# -*- encoding: utf-8 -*-
import abc
from supriya.tools.ugentools.InfoUGenBase import InfoUGenBase


class BufInfoUGenBase(InfoUGenBase):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Info UGens'

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(
        self,
        buffer_id=None,
        rate=None,
        ):
        InfoUGenBase.__init__(
            self,
            buffer_id=buffer_id,
            rate=rate,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ir(cls, buffer_id=None):
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.SCALAR
        ugen = cls._new_expanded(
            buffer_id=buffer_id,
            rate=rate,
            )
        return ugen

    @classmethod
    def kr(cls, buffer_id=None):
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.CONTROL
        ugen = cls._new_expanded(
            buffer_id=buffer_id,
            rate=rate,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of BufInfoUGenBase.

        ::

            >>> buffer_id = None
            >>> buf_info_ugen_base = ugentools.BufInfoUGenBase.ar(
            ...     buffer_id=buffer_id,
            ...     )
            >>> buf_info_ugen_base.buffer_id

        Returns input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]