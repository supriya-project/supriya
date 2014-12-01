# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class Demand(MultiOutUGen):
    r'''

    ::

        >>> demand = ugentools.Demand.ar(
        ...     demand_ugens=demand_ugens,
        ...     reset=reset,
        ...     trigger=trigger,
        ...     )
        >>> demand
        Demand.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'trigger',
        'reset',
        'demand_ugens',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        demand_ugens=None,
        reset=None,
        trigger=None,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            demand_ugens=demand_ugens,
            reset=reset,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        demand_ugens=demand_ugens,
        reset=reset,
        trigger=trigger,
        ):
        r'''Constructs an audio-rate Demand.

        ::

            >>> demand = ugentools.Demand.ar(
            ...     demand_ugens=demand_ugens,
            ...     reset=reset,
            ...     trigger=trigger,
            ...     )
            >>> demand
            Demand.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            demand_ugens=demand_ugens,
            reset=reset,
            trigger=trigger,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        demand_ugens=demand_ugens,
        reset=reset,
        trigger=trigger,
        ):
        r'''Constructs a control-rate Demand.

        ::

            >>> demand = ugentools.Demand.kr(
            ...     demand_ugens=demand_ugens,
            ...     reset=reset,
            ...     trigger=trigger,
            ...     )
            >>> demand
            Demand.kr()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            demand_ugens=demand_ugens,
            reset=reset,
            trigger=trigger,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def demand_ugens(self):
        r'''Gets `demand_ugens` input of Demand.

        ::

            >>> demand = ugentools.Demand.ar(
            ...     demand_ugens=demand_ugens,
            ...     reset=reset,
            ...     trigger=trigger,
            ...     )
            >>> demand.demand_ugens

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('demand_ugens')
        return self._inputs[index]

    @property
    def reset(self):
        r'''Gets `reset` input of Demand.

        ::

            >>> demand = ugentools.Demand.ar(
            ...     demand_ugens=demand_ugens,
            ...     reset=reset,
            ...     trigger=trigger,
            ...     )
            >>> demand.reset

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('reset')
        return self._inputs[index]

    @property
    def trigger(self):
        r'''Gets `trigger` input of Demand.

        ::

            >>> demand = ugentools.Demand.ar(
            ...     demand_ugens=demand_ugens,
            ...     reset=reset,
            ...     trigger=trigger,
            ...     )
            >>> demand.trigger

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]