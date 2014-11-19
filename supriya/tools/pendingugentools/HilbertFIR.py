# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class HilbertFIR(UGen):
    r'''

    ::

        >>> hilbert_fir = ugentools.HilbertFIR.(
        ...     buffer_=None,
        ...     source=None,
        ...     )
        >>> hilbert_fir

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'buffer_',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_=None,
        source=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_=buffer_,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_=None,
        source=None,
        ):
        r'''Constructs an audio-rate HilbertFIR.

        ::

            >>> hilbert_fir = ugentools.HilbertFIR.ar(
            ...     buffer_=None,
            ...     source=None,
            ...     )
            >>> hilbert_fir

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_=buffer_,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        r'''Gets `source` input of HilbertFIR.

        ::

            >>> hilbert_fir = ugentools.HilbertFIR.ar(
            ...     buffer_=None,
            ...     source=None,
            ...     )
            >>> hilbert_fir.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def buffer_(self):
        r'''Gets `buffer_` input of HilbertFIR.

        ::

            >>> hilbert_fir = ugentools.HilbertFIR.ar(
            ...     buffer_=None,
            ...     source=None,
            ...     )
            >>> hilbert_fir.buffer_

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_')
        return self._inputs[index]