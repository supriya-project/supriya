# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Filter import Filter


class Ringz(Filter):
    r'''

    ::

        >>> ringz = ugentools.Ringz.(
        ...     decay_time=1,
        ...     frequency=440,
        ...     source=None,
        ...     )
        >>> ringz

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'frequency',
        'decay_time',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        decay_time=1,
        frequency=440,
        source=None,
        ):
        Filter.__init__(
            self,
            calculation_rate=calculation_rate,
            decay_time=decay_time,
            frequency=frequency,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        decay_time=1,
        frequency=440,
        source=None,
        ):
        r'''Constructs an audio-rate Ringz.

        ::

            >>> ringz = ugentools.Ringz.ar(
            ...     decay_time=1,
            ...     frequency=440,
            ...     source=None,
            ...     )
            >>> ringz

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            decay_time=decay_time,
            frequency=frequency,
            source=source,
            )
        return ugen

    # def coeffs(): ...

    @classmethod
    def kr(
        cls,
        decay_time=1,
        frequency=440,
        source=None,
        ):
        r'''Constructs a control-rate Ringz.

        ::

            >>> ringz = ugentools.Ringz.kr(
            ...     decay_time=1,
            ...     frequency=440,
            ...     source=None,
            ...     )
            >>> ringz

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
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
    def decay_time(self):
        r'''Gets `decay_time` input of Ringz.

        ::

            >>> ringz = ugentools.Ringz.ar(
            ...     decay_time=1,
            ...     frequency=440,
            ...     source=None,
            ...     )
            >>> ringz.decay_time

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('decay_time')
        return self._inputs[index]

    @property
    def frequency(self):
        r'''Gets `frequency` input of Ringz.

        ::

            >>> ringz = ugentools.Ringz.ar(
            ...     decay_time=1,
            ...     frequency=440,
            ...     source=None,
            ...     )
            >>> ringz.frequency

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of Ringz.

        ::

            >>> ringz = ugentools.Ringz.ar(
            ...     decay_time=1,
            ...     frequency=440,
            ...     source=None,
            ...     )
            >>> ringz.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]