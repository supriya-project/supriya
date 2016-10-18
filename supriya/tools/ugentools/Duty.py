# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.UGen import UGen
from supriya import *

class Duty(UGen):
    r'''A value is demanded of each UGen in the list and output according to a stream of duration values.

    ::

        >>> duty = ugentools.Duty.ar(
        ...     done_action=0,
        ...     duration=1,
        ...     level=1,
        ...     reset=0,
        ...     )
        >>> duty
        Duty.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'duration',
        'reset',
        'level',
        'done_action',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        done_action=0,
        duration=1,
        level=1,
        reset=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            done_action=done_action,
            duration=duration,
            level=level,
            reset=reset,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        done_action=0,
        duration=1,
        level=1,
        reset=0,
        ):
        r'''Constructs an audio-rate Duty.

        ::

            >>> duty = ugentools.Duty.ar(
            ...     done_action=0,
            ...     duration=1,
            ...     level=1,
            ...     reset=0,
            ...     )
            >>> duty
            Duty.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            done_action=done_action,
            duration=duration,
            level=level,
            reset=reset,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        done_action=0,
        duration=1,
        level=1,
        reset=0,
        ):
        r'''Constructs a control-rate Duty.

        ::

            >>> duty = ugentools.Duty.kr(
            ...     done_action=0,
            ...     duration=1,
            ...     level=1,
            ...     reset=0,
            ...     )
            >>> duty
            Duty.kr()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            done_action=done_action,
            duration=duration,
            level=level,
            reset=reset,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def done_action(self):
        r'''Gets `done_action` input of Duty.

        ::

            >>> duty = ugentools.Duty.ar(
            ...     done_action=0,
            ...     duration=1,
            ...     level=1,
            ...     reset=0,
            ...     )
            >>> duty.done_action
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('done_action')
        return self._inputs[index]

    @property
    def duration(self):
        r'''Gets `duration` input of Duty.

        ::

            >>> duty = ugentools.Duty.ar(
            ...     done_action=0,
            ...     duration=1,
            ...     level=1,
            ...     reset=0,
            ...     )
            >>> duty.duration
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('duration')
        return self._inputs[index]

    @property
    def level(self):
        r'''Gets `level` input of Duty.

        ::

            >>> duty = ugentools.Duty.ar(
            ...     done_action=0,
            ...     duration=1,
            ...     level=1,
            ...     reset=0,
            ...     )
            >>> duty.level
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('level')
        return self._inputs[index]

    @property
    def reset(self):
        r'''Gets `reset` input of Duty.

        ::

            >>> duty = ugentools.Duty.ar(
            ...     done_action=0,
            ...     duration=1,
            ...     level=1,
            ...     reset=0,
            ...     )
            >>> duty.reset
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('reset')
        return self._inputs[index]