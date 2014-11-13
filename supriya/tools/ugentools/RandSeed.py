# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.WidthFirstUGen import WidthFirstUGen


class RandSeed(WidthFirstUGen):
    r'''Sets the synth's random generator seed.

    ::

        >>> trigger = ugentools.Impulse.ar()
        >>> rand_seed = ugentools.RandSeed.ar(
        ...     seed=1,
        ...     trigger=trigger,
        ...     )
        >>> rand_seed
        RandSeed.ar()

    '''
    ### CLASS VARIABLES ###

    __documentation_section__ = 'Noise UGens'

    __slots__ = ()

    _ordered_input_names = (
        'trigger',
        'seed',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        seed=56789,
        trigger=0,
        ):
        WidthFirstUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            seed=seed,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        seed=56789,
        trigger=0,
        ):
        r'''Constructs an audio-rate RandSeed.

        ::

            >>> trigger = ugentools.Impulse.ar()
            >>> rand_seed = ugentools.RandSeed.ar(
            ...     seed=1,
            ...     trigger=trigger,
            ...     )
            >>> rand_seed
            RandSeed.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            seed=seed,
            trigger=trigger,
            )
        return ugen

    @classmethod
    def ir(
        cls,
        seed=56789,
        trigger=0,
        ):
        r'''Constructs a scalar-rate RandSeed.

        ::

            >>> rand_seed = ugentools.RandSeed.ir(
            ...     seed=1,
            ...     )
            >>> rand_seed
            RandSeed.ir()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.SCALAR
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            seed=seed,
            trigger=trigger,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        seed=56789,
        trigger=0,
        ):
        r'''Constructs a control-rate RandSeed.

        ::

            >>> trigger = ugentools.Impulse.kr()
            >>> rand_seed = ugentools.RandSeed.kr(
            ...     seed=1,
            ...     trigger=trigger,
            ...     )
            >>> rand_seed
            RandSeed.kr()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            seed=seed,
            trigger=trigger,
            )
        return ugen