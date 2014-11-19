# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_BinScramble(PV_ChainUGen):
    r'''

    ::

        >>> pv_bin_scramble = ugentools.PV_BinScramble.(
        ...     )
        >>> pv_bin_scramble

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
        buffer_=None,
        trigger=0,
        width=0.2,
        wipe=0,
        ):
        r'''Constructs a PV_BinScramble.

        ::

            >>> pv_bin_scramble = ugentools.PV_BinScramble.new(
            ...     buffer_=None,
            ...     trigger=0,
            ...     width=0.2,
            ...     wipe=0,
            ...     )
            >>> pv_bin_scramble

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_=buffer_,
            trigger=trigger,
            width=width,
            wipe=wipe,
            )
        return ugen
