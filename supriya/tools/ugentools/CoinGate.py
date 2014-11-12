# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class CoinGate(UGen):
    r'''A probabilistic trigger gate.

    ::

        >>> trigger = ugentools.Impulse.ar()
        >>> coin_gate = ugentools.CoinGate.ar(
        ...     probability=0.5,
        ...     trigger=trigger,
        ...     )
        >>> coin_gate
        CoinGate.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Noise UGens'

    __slots__ = ()

    _ordered_input_names = (
        'probability',
        'trigger',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        probability=None,
        trigger=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            probability=probability,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        probability=None,
        trigger=None,
        ):
        r'''Constructs an audio-rate probabilitic trigger gate.

        ::

            >>> trigger = ugentools.Impulse.ar()
            >>> coin_gate = ugentools.CoinGate.ar(
            ...     probability=[0.9, 0.1],
            ...     trigger=trigger,
            ...     )
            >>> coin_gate
            UGenArray({2})

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            probability=probability,
            trigger=trigger,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        probability=None,
        trigger=None,
        ):
        r'''Constructs a control-rate probabilitic trigger gate.

        ::

            >>> trigger = ugentools.Impulse.kr()
            >>> coin_gate = ugentools.CoinGate.kr(
            ...     probability=[0.9, 0.1],
            ...     trigger=trigger,
            ...     )
            >>> coin_gate
            UGenArray({2})

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            probability=probability,
            trigger=trigger,
            )
        return ugen