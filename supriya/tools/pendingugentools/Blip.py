# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Blip(UGen):
    r'''

    ::

        >>> blip = ugentools.Blip.ar(
        ...     frequency=440,
        ...     numharm=200,
        ...     )
        >>> blip
        Blip.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'frequency',
        'numharm',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        frequency=440,
        numharm=200,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            frequency=frequency,
            numharm=numharm,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=440,
        numharm=200,
        ):
        r'''Constructs an audio-rate Blip.

        ::

            >>> blip = ugentools.Blip.ar(
            ...     frequency=440,
            ...     numharm=200,
            ...     )
            >>> blip
            Blip.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            numharm=numharm,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        frequency=440,
        numharm=200,
        ):
        r'''Constructs a control-rate Blip.

        ::

            >>> blip = ugentools.Blip.kr(
            ...     frequency=440,
            ...     numharm=200,
            ...     )
            >>> blip
            Blip.kr()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            numharm=numharm,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def frequency(self):
        r'''Gets `frequency` input of Blip.

        ::

            >>> blip = ugentools.Blip.ar(
            ...     frequency=440,
            ...     numharm=200,
            ...     )
            >>> blip.frequency
            440.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def numharm(self):
        r'''Gets `numharm` input of Blip.

        ::

            >>> blip = ugentools.Blip.ar(
            ...     frequency=440,
            ...     numharm=200,
            ...     )
            >>> blip.numharm
            200.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('numharm')
        return self._inputs[index]