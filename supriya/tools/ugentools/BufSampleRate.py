# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.BufInfoUGenBase import BufInfoUGenBase


class BufSampleRate(BufInfoUGenBase):
    r'''Buffer sample rate info unit generator.

    ::

        >>> ugentools.BufSampleRate.kr(buffer_id=0)
        BufSampleRate.kr()

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
        r'''Gets `buffer_id` input of BufSampleRate.

        ::

            >>> buffer_id = 23
            >>> buf_sample_rate = ugentools.BufSampleRate.kr(
            ...     buffer_id=buffer_id,
            ...     )
            >>> buf_sample_rate.buffer_id
            23.0

        Returns input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]