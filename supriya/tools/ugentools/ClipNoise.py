# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class ClipNoise(UGen):
    r'''A clipped noise unit generator.

    ::

        >>> ugentools.ClipNoise.ar()
        ClipNoise.ar()

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
        r'''Constructs an audio-rate clipped noise unit generator.

        ::

            >>> ugentools.ClipNoise.ar()
            ClipNoise.ar()

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
        r'''Constructs a control-rate clipped noise unit generator.

        ::

            >>> ugentools.ClipNoise.kr()
            ClipNoise.kr()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            )
        return ugen