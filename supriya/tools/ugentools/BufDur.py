# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.BufInfoUGenBase import BufInfoUGenBase


class BufDur(BufInfoUGenBase):
    r'''Buffer duration info unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> ugentools.BufDur.kr(buffer_id=0)
        BufDur.kr()

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
        r'''Gets `buffer_id` input of BufDur.

        ::

            >>> buffer_id = 23
            >>> buf_dur = ugentools.BufDur.kr(
            ...     buffer_id=buffer_id,
            ...     )
            >>> buf_dur.buffer_id
            23.0

        Returns input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]