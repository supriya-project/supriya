# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Trig1(UGen):
    r'''

    ::

        >>> trig_1 = ugentools.Trig1.(
        ...     duration=0.1,
        ...     source=None,
        ...     )
        >>> trig_1

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'duration',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        duration=0.1,
        source=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            duration=duration,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        duration=0.1,
        source=None,
        ):
        r'''Constructs an audio-rate Trig1.

        ::

            >>> trig_1 = ugentools.Trig1.ar(
            ...     duration=0.1,
            ...     source=None,
            ...     )
            >>> trig_1

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            duration=duration,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        duration=0.1,
        source=None,
        ):
        r'''Constructs a control-rate Trig1.

        ::

            >>> trig_1 = ugentools.Trig1.kr(
            ...     duration=0.1,
            ...     source=None,
            ...     )
            >>> trig_1

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            duration=duration,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self):
        r'''Gets `duration` input of Trig1.

        ::

            >>> trig_1 = ugentools.Trig1.ar(
            ...     duration=0.1,
            ...     source=None,
            ...     )
            >>> trig_1.duration

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('duration')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of Trig1.

        ::

            >>> trig_1 = ugentools.Trig1.ar(
            ...     duration=0.1,
            ...     source=None,
            ...     )
            >>> trig_1.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]