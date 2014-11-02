# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.BufInfoUGenBase import BufInfoUGenBase


class BufRateScale(BufInfoUGenBase):
    r'''Buffer sample rate scale info unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> ugentools.BufRateScale.kr(buffer_id=0)
        BufRateScale.kr()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Info UGens'

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        rate=None,
        ):
        BufInfoUGenBase.__init__(
            self,
            buffer_id=buffer_id,
            rate=rate,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of BufRateScale.

        ::

            >>> buffer_id = 23
            >>> buf_rate_scale = ugentools.BufRateScale.kr(
            ...     buffer_id=buffer_id,
            ...     )
            >>> buf_rate_scale.buffer_id
            23.0

        Returns input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]