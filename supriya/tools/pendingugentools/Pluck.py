# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Pluck(UGen):
    r'''

    ::

        >>> pluck = ugentools.Pluck.(
        ...     coefficient=0.5,
        ...     decay_time=1,
        ...     delay_time=0.2,
        ...     maximum_delay_time=0.2,
        ...     source=None,
        ...     trigger=1,
        ...     )
        >>> pluck

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'trigger',
        'maximum_delay_time',
        'delay_time',
        'decay_time',
        'coefficient',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        coefficient=0.5,
        decay_time=1,
        delay_time=0.2,
        maximum_delay_time=0.2,
        source=None,
        trigger=1,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            coefficient=coefficient,
            decay_time=decay_time,
            delay_time=delay_time,
            maximum_delay_time=maximum_delay_time,
            source=source,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        coefficient=0.5,
        decay_time=1,
        delay_time=0.2,
        maximum_delay_time=0.2,
        source=None,
        trigger=1,
        ):
        r'''Constructs an audio-rate Pluck.

        ::

            >>> pluck = ugentools.Pluck.ar(
            ...     coefficient=0.5,
            ...     decay_time=1,
            ...     delay_time=0.2,
            ...     maximum_delay_time=0.2,
            ...     source=None,
            ...     trigger=1,
            ...     )
            >>> pluck

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            coefficient=coefficient,
            decay_time=decay_time,
            delay_time=delay_time,
            maximum_delay_time=maximum_delay_time,
            source=source,
            trigger=trigger,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        r'''Gets `source` input of Pluck.

        ::

            >>> pluck = ugentools.Pluck.ar(
            ...     coefficient=0.5,
            ...     decay_time=1,
            ...     delay_time=0.2,
            ...     maximum_delay_time=0.2,
            ...     source=None,
            ...     trigger=1,
            ...     )
            >>> pluck.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def trigger(self):
        r'''Gets `trigger` input of Pluck.

        ::

            >>> pluck = ugentools.Pluck.ar(
            ...     coefficient=0.5,
            ...     decay_time=1,
            ...     delay_time=0.2,
            ...     maximum_delay_time=0.2,
            ...     source=None,
            ...     trigger=1,
            ...     )
            >>> pluck.trigger

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]

    @property
    def maximum_delay_time(self):
        r'''Gets `maximum_delay_time` input of Pluck.

        ::

            >>> pluck = ugentools.Pluck.ar(
            ...     coefficient=0.5,
            ...     decay_time=1,
            ...     delay_time=0.2,
            ...     maximum_delay_time=0.2,
            ...     source=None,
            ...     trigger=1,
            ...     )
            >>> pluck.maximum_delay_time

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('maximum_delay_time')
        return self._inputs[index]

    @property
    def delay_time(self):
        r'''Gets `delay_time` input of Pluck.

        ::

            >>> pluck = ugentools.Pluck.ar(
            ...     coefficient=0.5,
            ...     decay_time=1,
            ...     delay_time=0.2,
            ...     maximum_delay_time=0.2,
            ...     source=None,
            ...     trigger=1,
            ...     )
            >>> pluck.delay_time

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('delay_time')
        return self._inputs[index]

    @property
    def decay_time(self):
        r'''Gets `decay_time` input of Pluck.

        ::

            >>> pluck = ugentools.Pluck.ar(
            ...     coefficient=0.5,
            ...     decay_time=1,
            ...     delay_time=0.2,
            ...     maximum_delay_time=0.2,
            ...     source=None,
            ...     trigger=1,
            ...     )
            >>> pluck.decay_time

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('decay_time')
        return self._inputs[index]

    @property
    def coefficient(self):
        r'''Gets `coefficient` input of Pluck.

        ::

            >>> pluck = ugentools.Pluck.ar(
            ...     coefficient=0.5,
            ...     decay_time=1,
            ...     delay_time=0.2,
            ...     maximum_delay_time=0.2,
            ...     source=None,
            ...     trigger=1,
            ...     )
            >>> pluck.coefficient

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('coefficient')
        return self._inputs[index]