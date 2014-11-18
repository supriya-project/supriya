# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class LFGauss(UGen):
    r'''A non-band-limited gaussian function oscillator.

    ::

        >>> ugentools.LFGauss.ar()
        LFGauss.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Oscillator UGens'

    __slots__ = ()

    _ordered_input_names = (
        'duration',
        'width',
        'initial_phase',
        'loop',
        'done_action',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        done_action=0,
        duration=1,
        initial_phase=0,
        loop=1,
        width=0.1,
        ):
        from supriya.tools import synthdeftools
        done_action = synthdeftools.DoneAction.from_expr(done_action)
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            done_action=done_action,
            duration=duration,
            initial_phase=initial_phase,
            loop=loop,
            width=width,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        done_action=0,
        duration=1,
        initial_phase=0,
        loop=1,
        width=0.1,
        ):
        r'''Constructs an audio-rate non-band-limited gaussian function
        oscillator.

        ::

            >>> ugentools.LFGauss.ar(
            ...     done_action=DoneAction.NOTHING,
            ...     duration=[1.0, 1.1],
            ...     initial_phase=0.0,
            ...     loop=True,
            ...     width=0.1,
            ...     )
            UGenArray({2})

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            done_action=done_action,
            duration=duration,
            initial_phase=initial_phase,
            loop=loop,
            width=width,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        done_action=0,
        duration=1,
        initial_phase=0,
        loop=1,
        width=0.1,
        ):
        r'''Constructs a control-rate non-band-limited gaussian function
        oscillator.

        ::

            >>> ugentools.LFGauss.kr(
            ...     done_action=DoneAction.NOTHING,
            ...     duration=[1.0, 1.1],
            ...     initial_phase=0.0,
            ...     loop=True,
            ...     width=0.1,
            ...     )
            UGenArray({2})

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            done_action=done_action,
            duration=duration,
            initial_phase=initial_phase,
            loop=loop,
            width=width,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self):
        r'''Gets `duration` input of LFSaw.

        ::

            >>> l_f_gauss = ugentools.LFGauss.ar(
            ...     done_action=DoneAction.NOTHING,
            ...     duration=1.0,
            ...     initial_phase=0.0,
            ...     loop=True,
            ...     width=0.1,
            ...     )
            >>> l_f_gauss.duration
            1.0

        Returns input.
        '''
        index = self._ordered_input_names.index('duration')
        return self._inputs[index]

    @property
    def done_action(self):
        r'''Gets `done_action` input of LFSaw.

        ::

            >>> l_f_gauss = ugentools.LFGauss.ar(
            ...     done_action=DoneAction.NOTHING,
            ...     duration=1.0,
            ...     initial_phase=0.0,
            ...     loop=True,
            ...     width=0.1,
            ...     )
            >>> l_f_gauss.done_action
            0.0

        Returns input.
        '''
        index = self._ordered_input_names.index('done_action')
        return self._inputs[index]

    @property
    def initial_phase(self):
        r'''Gets `initial_phase` input of LFSaw.

        ::

            >>> l_f_gauss = ugentools.LFGauss.ar(
            ...     done_action=DoneAction.NOTHING,
            ...     duration=1.0,
            ...     initial_phase=0.0,
            ...     loop=True,
            ...     width=0.1,
            ...     )
            >>> l_f_gauss.initial_phase
            0.0

        Returns input.
        '''
        index = self._ordered_input_names.index('initial_phase')
        return self._inputs[index]

    @property
    def loop(self):
        r'''Gets `loop` input of LFSaw.

        ::

            >>> l_f_gauss = ugentools.LFGauss.ar(
            ...     done_action=DoneAction.NOTHING,
            ...     duration=1.0,
            ...     initial_phase=0.0,
            ...     loop=True,
            ...     width=0.1,
            ...     )
            >>> l_f_gauss.loop
            1.0

        Returns input.
        '''
        index = self._ordered_input_names.index('loop')
        return self._inputs[index]

    @property
    def width(self):
        r'''Gets `width` input of LFSaw.

        ::

            >>> l_f_gauss = ugentools.LFGauss.ar(
            ...     done_action=DoneAction.NOTHING,
            ...     duration=1.0,
            ...     initial_phase=0.0,
            ...     loop=True,
            ...     width=0.1,
            ...     )
            >>> l_f_gauss.width
            0.1

        Returns input.
        '''
        index = self._ordered_input_names.index('width')
        return self._inputs[index]