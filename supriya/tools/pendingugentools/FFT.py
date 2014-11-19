# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class FFT(PV_ChainUGen):
    r'''

    ::

        >>> fft = ugentools.FFT.(
        ...     )
        >>> fft

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = ()

    _valid_calculation_rates = None

    ### INITIALIZER ###

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        active=1,
        buffer_=None,
        hop=0.5,
        source=None,
        winsize=0,
        wintype=0,
        ):
        r'''Constructs a FFT.

        ::

            >>> fft = ugentools.FFT.new(
            ...     active=1,
            ...     buffer_=None,
            ...     hop=0.5,
            ...     source=None,
            ...     winsize=0,
            ...     wintype=0,
            ...     )
            >>> fft

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            active=active,
            buffer_=buffer_,
            hop=hop,
            source=source,
            winsize=winsize,
            wintype=wintype,
            )
        return ugen
