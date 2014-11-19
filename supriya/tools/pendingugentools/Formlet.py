# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Filter import Filter


class Formlet(Filter):
    r'''

    ::

        >>> formlet = ugentools.Formlet.(
        ...     attack_time=1,
        ...     decay_time=1,
        ...     frequency=440,
        ...     source=None,
        ...     )
        >>> formlet

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'frequency',
        'attack_time',
        'decay_time',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        attack_time=1,
        decay_time=1,
        frequency=440,
        source=None,
        ):
        Filter.__init__(
            self,
            calculation_rate=calculation_rate,
            attack_time=attack_time,
            decay_time=decay_time,
            frequency=frequency,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        attack_time=1,
        decay_time=1,
        frequency=440,
        source=None,
        ):
        r'''Constructs an audio-rate Formlet.

        ::

            >>> formlet = ugentools.Formlet.ar(
            ...     attack_time=1,
            ...     decay_time=1,
            ...     frequency=440,
            ...     source=None,
            ...     )
            >>> formlet

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            attack_time=attack_time,
            decay_time=decay_time,
            frequency=frequency,
            source=source,
            )
        return ugen

    # def coeffs(): ...

    @classmethod
    def kr(
        cls,
        attack_time=1,
        decay_time=1,
        frequency=440,
        source=None,
        ):
        r'''Constructs a control-rate Formlet.

        ::

            >>> formlet = ugentools.Formlet.kr(
            ...     attack_time=1,
            ...     decay_time=1,
            ...     frequency=440,
            ...     source=None,
            ...     )
            >>> formlet

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            attack_time=attack_time,
            decay_time=decay_time,
            frequency=frequency,
            source=source,
            )
        return ugen

    # def magResponse(): ...

    # def magResponse2(): ...

    # def magResponse5(): ...

    # def magResponseN(): ...

    # def scopeResponse(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def attack_time(self):
        r'''Gets `attack_time` input of Formlet.

        ::

            >>> formlet = ugentools.Formlet.ar(
            ...     attack_time=1,
            ...     decay_time=1,
            ...     frequency=440,
            ...     source=None,
            ...     )
            >>> formlet.attack_time

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('attack_time')
        return self._inputs[index]

    @property
    def decay_time(self):
        r'''Gets `decay_time` input of Formlet.

        ::

            >>> formlet = ugentools.Formlet.ar(
            ...     attack_time=1,
            ...     decay_time=1,
            ...     frequency=440,
            ...     source=None,
            ...     )
            >>> formlet.decay_time

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('decay_time')
        return self._inputs[index]

    @property
    def frequency(self):
        r'''Gets `frequency` input of Formlet.

        ::

            >>> formlet = ugentools.Formlet.ar(
            ...     attack_time=1,
            ...     decay_time=1,
            ...     frequency=440,
            ...     source=None,
            ...     )
            >>> formlet.frequency

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of Formlet.

        ::

            >>> formlet = ugentools.Formlet.ar(
            ...     attack_time=1,
            ...     decay_time=1,
            ...     frequency=440,
            ...     source=None,
            ...     )
            >>> formlet.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]