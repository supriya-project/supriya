# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Unpack1FFT(UGen):
    r'''

    ::

        >>> unpack_1_fft = ugentools.Unpack1FFT.(
        ...     )
        >>> unpack_1_fft

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
        binindex=None,
        bufsize=None,
        chain=None,
        whichmeasure=0,
        ):
        r'''Constructs a Unpack1FFT.

        ::

            >>> unpack_1_fft = ugentools.Unpack1FFT.new(
            ...     binindex=None,
            ...     bufsize=None,
            ...     chain=None,
            ...     whichmeasure=0,
            ...     )
            >>> unpack_1_fft

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            binindex=binindex,
            bufsize=bufsize,
            chain=chain,
            whichmeasure=whichmeasure,
            )
        return ugen
