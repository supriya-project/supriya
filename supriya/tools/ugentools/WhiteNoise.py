# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class WhiteNoise(UGen):
    r'''A white noise unit generator.

    ::

        >>> ugentools.WhiteNoise.ar()
        WhiteNoise.ar()

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
        r'''Creates an audio-calculation_rate white noise unit generator.

        ::

            >>> ugentools.WhiteNoise.ar()
            WhiteNoise.ar()

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
        r'''Creates a control-calculation_rate white noise unit generator.

        ::

            >>> ugentools.WhiteNoise.kr()
            WhiteNoise.kr()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            )
        return ugen