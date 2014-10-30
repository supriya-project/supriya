# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class XLine(UGen):
    r'''An exponential line generating unit generator.

    ::

        >>> from supriya.tools import ugentools
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

            >>> from supriya.tools import synthdeftools
            >>> from supriya.tools import ugentools
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

            >>> from supriya.tools import synthdeftools
            >>> from supriya.tools import ugentools
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