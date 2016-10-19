# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.UGen import UGen


class Phasor(UGen):
    r"""
    A resettable linear ramp between two levels.

    ::

        >>> trigger = ugentools.Impulse.kr(0.5)
        >>> phasor = ugentools.Phasor.ar(
        ...     rate=1,
        ...     reset_pos=0,
        ...     start=0,
        ...     stop=1,
        ...     trigger=trigger,
        ...     )
        >>> phasor
        Phasor.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Trigger Utility UGens'

    __slots__ = ()

    _ordered_input_names = (
        'trigger',
        'rate',
        'start',
        'stop',
        'reset_pos',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        rate=1,
        reset_pos=0,
        start=0,
        stop=1,
        trigger=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            rate=rate,
            reset_pos=reset_pos,
            start=start,
            stop=stop,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        rate=1,
        reset_pos=0,
        start=0,
        stop=1,
        trigger=0,
        ):
        r"""
        Constructs an audio-rate Phasor.

        ::

            >>> trigger = ugentools.Impulse.kr([0.5, 0.6])
            >>> phasor = ugentools.Phasor.ar(
            ...     rate=1,
            ...     reset_pos=0,
            ...     start=0,
            ...     stop=1,
            ...     trigger=trigger,
            ...     )
            >>> phasor
            UGenArray({2})

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            rate=rate,
            reset_pos=reset_pos,
            start=start,
            stop=stop,
            trigger=trigger,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        rate=1,
        reset_pos=0,
        start=0,
        stop=1,
        trigger=0,
        ):
        r"""
        Constructs a control-rate Phasor.

        ::

            >>> trigger = ugentools.Impulse.kr([0.5, 0.6])
            >>> phasor = ugentools.Phasor.kr(
            ...     rate=1,
            ...     reset_pos=0,
            ...     start=0,
            ...     stop=1,
            ...     trigger=trigger,
            ...     )
            >>> phasor
            UGenArray({2})

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            rate=rate,
            reset_pos=reset_pos,
            start=start,
            stop=stop,
            trigger=trigger,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def rate(self):
        r"""
        Gets `rate` input of Phasor.

        ::

            >>> trigger = ugentools.Impulse.kr(0.5)
            >>> phasor = ugentools.Phasor.ar(
            ...     rate=1,
            ...     reset_pos=0,
            ...     start=0,
            ...     stop=1,
            ...     trigger=trigger,
            ...     )
            >>> phasor.rate
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('rate')
        return self._inputs[index]

    @property
    def reset_pos(self):
        r"""
        Gets `reset_pos` input of Phasor.

        ::

            >>> trigger = ugentools.Impulse.kr(0.5)
            >>> phasor = ugentools.Phasor.ar(
            ...     rate=1,
            ...     reset_pos=0,
            ...     start=0,
            ...     stop=1,
            ...     trigger=trigger,
            ...     )
            >>> phasor.reset_pos
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('reset_pos')
        return self._inputs[index]

    @property
    def start(self):
        r"""
        Gets `start` input of Phasor.

        ::

            >>> trigger = ugentools.Impulse.kr(0.5)
            >>> phasor = ugentools.Phasor.ar(
            ...     rate=1,
            ...     reset_pos=0,
            ...     start=0,
            ...     stop=1,
            ...     trigger=trigger,
            ...     )
            >>> phasor.start
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('start')
        return self._inputs[index]

    @property
    def stop(self):
        r"""
        Gets `stop` input of Phasor.

        ::

            >>> trigger = ugentools.Impulse.kr(0.5)
            >>> phasor = ugentools.Phasor.ar(
            ...     rate=1,
            ...     reset_pos=0,
            ...     start=0,
            ...     stop=1,
            ...     trigger=trigger,
            ...     )
            >>> phasor.stop
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('stop')
        return self._inputs[index]

    @property
    def trigger(self):
        r"""
        Gets `trigger` input of Phasor.

        ::

            >>> trigger = ugentools.Impulse.kr(0.5)
            >>> phasor = ugentools.Phasor.ar(
            ...     rate=1,
            ...     reset_pos=0,
            ...     start=0,
            ...     stop=1,
            ...     trigger=trigger,
            ...     )
            >>> phasor.trigger
            OutputProxy(
                source=Impulse(
                    calculation_rate=CalculationRate.CONTROL,
                    frequency=0.5,
                    phase=0.0
                    ),
                output_index=0
                )

        Returns ugen input.
        """
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]
