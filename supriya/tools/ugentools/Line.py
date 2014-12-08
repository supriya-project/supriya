# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Line(UGen):
    r'''A line generating unit generator.

    ::

        >>> ugentools.Line.ar()
        Line.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Line Utility UGens'

    __slots__ = ()

    _ordered_input_names = (
        'start',
        'stop',
        'duration',
        'done_action',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        done_action=0.,
        duration=1.,
        start=0.,
        stop=1.,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            done_action=done_action,
            duration=duration,
            start=start,
            stop=stop,
            )

    ### PRIVATE METHODS ###

    @classmethod
    def _new_expanded(
        cls,
        calculation_rate=None,
        done_action=None,
        duration=None,
        stop=None,
        start=None,
        ):
        from supriya.tools import synthdeftools
        done_action = synthdeftools.DoneAction.from_expr(done_action)
        return super(Line, cls)._new_expanded(
            calculation_rate=calculation_rate,
            done_action=done_action,
            duration=duration,
            stop=stop,
            start=start,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        done_action=0,
        duration=1,
        stop=1,
        start=0,
        ):
        r'''Constructs an audio-rate line generator.

        ::

            >>> ugentools.Line.ar(
            ...     done_action=synthdeftools.DoneAction.FREE_SYNTH,
            ...     duration=5.5,
            ...     stop=12.1,
            ...     start=0.1,
            ...     )
            Line.ar()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        return cls._new_expanded(
            calculation_rate=calculation_rate,
            done_action=done_action,
            duration=duration,
            stop=stop,
            start=start,
            )

    @classmethod
    def kr(
        cls,
        done_action=0,
        duration=1,
        stop=1,
        start=0,
        ):
        r'''Constructs an audio-rate line generator.

        ::

            >>> ugentools.Line.kr(
            ...     done_action=synthdeftools.DoneAction.FREE_SYNTH,
            ...     duration=5.5,
            ...     stop=12.1,
            ...     start=0.1,
            ...     )
            Line.kr()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        return cls._new_expanded(
            calculation_rate=calculation_rate,
            done_action=done_action,
            duration=duration,
            stop=stop,
            start=start,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def done_action(self):
        r'''Gets `done_action` input of Line.

        ::

            >>> done_action = 0
            >>> line = ugentools.Line.ar(
            ...     done_action=done_action,
            ...     )
            >>> line.done_action
            0.0

        Returns input.
        '''
        index = self._ordered_input_names.index('done_action')
        return self._inputs[index]

    @property
    def duration(self):
        r'''Gets `duration` input of Line.

        ::

            >>> duration = 5.5
            >>> line = ugentools.Line.ar(
            ...     duration=duration,
            ...     )
            >>> line.duration
            5.5

        Returns input.
        '''
        index = self._ordered_input_names.index('duration')
        return self._inputs[index]

    @property
    def has_done_flag(self):
        r'''Is true if UGen has a done flag.

        Returns boolean.
        '''
        return True

    @property
    def start(self):
        r'''Gets `start` input of Line.

        ::

            >>> start = 0.1
            >>> line = ugentools.Line.ar(
            ...     start=start,
            ...     )
            >>> line.start
            0.1

        Returns input.
        '''
        index = self._ordered_input_names.index('start')
        return self._inputs[index]

    @property
    def stop(self):
        r'''Gets `stop` input of Line.

        ::

            >>> stop = 12.1
            >>> line = ugentools.Line.ar(
            ...     stop=stop,
            ...     )
            >>> line.stop
            12.1

        Returns input.
        '''
        index = self._ordered_input_names.index('stop')
        return self._inputs[index]