# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class XLine(UGen):
    r'''An exponential line generating unit generator.

    ::

        >>> ugentools.XLine.ar()
        XLine.ar()

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
        rate=None,
        done_action=0.,
        duration=1.,
        start=0.,
        stop=1.,
        ):
        UGen.__init__(
            self,
            rate=rate,
            done_action=done_action,
            duration=duration,
            start=start,
            stop=stop,
            )

    ### PRIVATE METHODS ###

    @classmethod
    def _new_expanded(
        cls,
        rate=None,
        done_action=None,
        duration=None,
        stop=None,
        start=None,
        ):
        from supriya.tools import synthdeftools
        done_action = synthdeftools.DoneAction.from_expr(done_action)
        return super(XLine, cls)._new_expanded(
            rate=rate,
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
        r'''Creates an audio-rate exponential line generator.

        ::

            >>> ugentools.XLine.ar(
            ...     done_action=synthdeftools.DoneAction.FREE_SYNTH,
            ...     duration=5.5,
            ...     stop=12.1,
            ...     start=0.1,
            ...     )
            XLine.ar()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.AUDIO
        return cls._new_expanded(
            rate=rate,
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
        r'''Creates a control-rate exponential line generator.

        ::

            >>> ugentools.XLine.kr(
            ...     done_action=synthdeftools.DoneAction.FREE_SYNTH,
            ...     duration=5.5,
            ...     stop=12.1,
            ...     start=0.1,
            ...     )
            XLine.kr()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.CONTROL
        return cls._new_expanded(
            rate=rate,
            done_action=done_action,
            duration=duration,
            stop=stop,
            start=start,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def done_action(self):
        r'''Gets `done_action` input of XLine.

        ::

            >>> done_action = 0
            >>> xline = ugentools.XLine.ar(
            ...     done_action=done_action,
            ...     )
            >>> xline.done_action
            0.0

        Returns input.
        '''
        index = self._ordered_input_names.index('done_action')
        return self._inputs[index]

    @property
    def duration(self):
        r'''Gets `duration` input of XLine.

        ::

            >>> duration = 1.5
            >>> xline = ugentools.XLine.ar(
            ...     duration=duration,
            ...     )
            >>> xline.duration
            1.5

        Returns input.
        '''
        index = self._ordered_input_names.index('duration')
        return self._inputs[index]

    @property
    def start(self):
        r'''Gets `start` input of XLine.

        ::

            >>> start = 0
            >>> xline = ugentools.XLine.ar(
            ...     start=start,
            ...     )
            >>> xline.start
            0.0

        Returns input.
        '''
        index = self._ordered_input_names.index('start')
        return self._inputs[index]

    @property
    def stop(self):
        r'''Gets `stop` input of XLine.

        ::

            >>> stop = 1
            >>> xline = ugentools.XLine.ar(
            ...     stop=stop,
            ...     )
            >>> xline.stop
            1.0

        Returns input.
        '''
        index = self._ordered_input_names.index('stop')
        return self._inputs[index]