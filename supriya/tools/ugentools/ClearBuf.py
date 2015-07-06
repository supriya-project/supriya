# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.CalculationRate import CalculationRate
from supriya.tools.ugentools.WidthFirstUGen import WidthFirstUGen


class ClearBuf(WidthFirstUGen):
    r'''

    ::

        >>> clear_buf = ugentools.ClearBuf.new(
        ...     buffer_id=23,
        ...     )
        >>> clear_buf
        ClearBuf.ir()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Buffer UGens'

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        )

    _valid_calculation_rates = (
        CalculationRate.SCALAR
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=None,
        ):
        WidthFirstUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        buffer_id=None,
        ):
        r'''Constructs a ClearBuf.

        ::

            >>> clear_buf = ugentools.ClearBuf.new(
            ...     buffer_id=23,
            ...     )
            >>> clear_buf
            ClearBuf.ir()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = CalculationRate.SCALAR
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of ClearBuf.

        ::

            >>> clear_buf = ugentools.ClearBuf.new(
            ...     buffer_id=23,
            ...     )
            >>> clear_buf.buffer_id
            23

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return int(self._inputs[index])