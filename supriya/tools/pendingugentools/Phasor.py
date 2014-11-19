# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Phasor(UGen):
    r'''

    ::

        >>> phasor = ugentools.Phasor.(
        ...     end=1,
        ...     rate=1,
        ...     reset_pos=0,
        ...     start=0,
        ...     trigger=0,
        ...     )
        >>> phasor

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'trigger',
        'rate',
        'start',
        'end',
        'reset_pos',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        end=1,
        rate=1,
        reset_pos=0,
        start=0,
        trigger=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            end=end,
            rate=rate,
            reset_pos=reset_pos,
            start=start,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        end=1,
        rate=1,
        reset_pos=0,
        start=0,
        trigger=0,
        ):
        r'''Constructs an audio-rate Phasor.

        ::

            >>> phasor = ugentools.Phasor.ar(
            ...     end=1,
            ...     rate=1,
            ...     reset_pos=0,
            ...     start=0,
            ...     trigger=0,
            ...     )
            >>> phasor

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            end=end,
            rate=rate,
            reset_pos=reset_pos,
            start=start,
            trigger=trigger,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        end=1,
        rate=1,
        reset_pos=0,
        start=0,
        trigger=0,
        ):
        r'''Constructs a control-rate Phasor.

        ::

            >>> phasor = ugentools.Phasor.kr(
            ...     end=1,
            ...     rate=1,
            ...     reset_pos=0,
            ...     start=0,
            ...     trigger=0,
            ...     )
            >>> phasor

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            end=end,
            rate=rate,
            reset_pos=reset_pos,
            start=start,
            trigger=trigger,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def trigger(self):
        r'''Gets `trigger` input of Phasor.

        ::

            >>> phasor = ugentools.Phasor.ar(
            ...     end=1,
            ...     rate=1,
            ...     reset_pos=0,
            ...     start=0,
            ...     trigger=0,
            ...     )
            >>> phasor.trigger

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]

    @property
    def rate(self):
        r'''Gets `rate` input of Phasor.

        ::

            >>> phasor = ugentools.Phasor.ar(
            ...     end=1,
            ...     rate=1,
            ...     reset_pos=0,
            ...     start=0,
            ...     trigger=0,
            ...     )
            >>> phasor.rate

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('rate')
        return self._inputs[index]

    @property
    def start(self):
        r'''Gets `start` input of Phasor.

        ::

            >>> phasor = ugentools.Phasor.ar(
            ...     end=1,
            ...     rate=1,
            ...     reset_pos=0,
            ...     start=0,
            ...     trigger=0,
            ...     )
            >>> phasor.start

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('start')
        return self._inputs[index]

    @property
    def end(self):
        r'''Gets `end` input of Phasor.

        ::

            >>> phasor = ugentools.Phasor.ar(
            ...     end=1,
            ...     rate=1,
            ...     reset_pos=0,
            ...     start=0,
            ...     trigger=0,
            ...     )
            >>> phasor.end

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('end')
        return self._inputs[index]

    @property
    def reset_pos(self):
        r'''Gets `reset_pos` input of Phasor.

        ::

            >>> phasor = ugentools.Phasor.ar(
            ...     end=1,
            ...     rate=1,
            ...     reset_pos=0,
            ...     start=0,
            ...     trigger=0,
            ...     )
            >>> phasor.reset_pos

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('reset_pos')
        return self._inputs[index]