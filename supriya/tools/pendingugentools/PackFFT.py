# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PackFFT(PV_ChainUGen):
    r'''

    ::

        >>> pack_fft = ugentools.PackFFT.(
        ...     )
        >>> pack_fft

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
        bufsize=None,
        chain=None,
        frombin=0,
        magsphases=None,
        tobin=None,
        zeroothers=0,
        ):
        r'''Constructs a PackFFT.

        ::

            >>> pack_fft = ugentools.PackFFT.new(
            ...     bufsize=None,
            ...     chain=None,
            ...     frombin=0,
            ...     magsphases=None,
            ...     tobin=None,
            ...     zeroothers=0,
            ...     )
            >>> pack_fft

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bufsize=bufsize,
            chain=chain,
            frombin=frombin,
            magsphases=magsphases,
            tobin=tobin,
            zeroothers=zeroothers,
            )
        return ugen
