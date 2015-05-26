# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.UGen import UGen


class BrownNoise(UGen):
    r'''A brown noise unit generator.

    ::

        >>> ugentools.BrownNoise.ar()
        BrownNoise.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Noise UGens'

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        ):
        r'''Constructs an audio-rate brown noise unit generator.

        ::

            >>> ugentools.BrownNoise.ar()
            BrownNoise.ar()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        ):
        r'''Constructs a control-rate brown noise unit generator.

        ::

            >>> ugentools.BrownNoise.kr()
            BrownNoise.kr()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            )
        return ugen