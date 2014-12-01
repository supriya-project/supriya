# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Filter import Filter


class Resonz(Filter):
    r'''

    ::

        >>> resonz = ugentools.Resonz.ar(
        ...     bwr=1,
        ...     frequency=440,
        ...     source=source,
        ...     )
        >>> resonz
        Resonz.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'frequency',
        'bwr',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        bwr=1,
        frequency=440,
        source=None,
        ):
        Filter.__init__(
            self,
            calculation_rate=calculation_rate,
            bwr=bwr,
            frequency=frequency,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        bwr=1,
        frequency=440,
        source=None,
        ):
        r'''Constructs an audio-rate Resonz.

        ::

            >>> resonz = ugentools.Resonz.ar(
            ...     bwr=1,
            ...     frequency=440,
            ...     source=source,
            ...     )
            >>> resonz
            Resonz.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bwr=bwr,
            frequency=frequency,
            source=source,
            )
        return ugen

    # def coeffs(): ...

    @classmethod
    def kr(
        cls,
        bwr=1,
        frequency=440,
        source=None,
        ):
        r'''Constructs a control-rate Resonz.

        ::

            >>> resonz = ugentools.Resonz.kr(
            ...     bwr=1,
            ...     frequency=440,
            ...     source=source,
            ...     )
            >>> resonz
            Resonz.kr()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bwr=bwr,
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
    def bwr(self):
        r'''Gets `bwr` input of Resonz.

        ::

            >>> resonz = ugentools.Resonz.ar(
            ...     bwr=1,
            ...     frequency=440,
            ...     source=source,
            ...     )
            >>> resonz.bwr
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('bwr')
        return self._inputs[index]

    @property
    def frequency(self):
        r'''Gets `frequency` input of Resonz.

        ::

            >>> resonz = ugentools.Resonz.ar(
            ...     bwr=1,
            ...     frequency=440,
            ...     source=source,
            ...     )
            >>> resonz.frequency
            440.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of Resonz.

        ::

            >>> resonz = ugentools.Resonz.ar(
            ...     bwr=1,
            ...     frequency=440,
            ...     source=source,
            ...     )
            >>> resonz.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]