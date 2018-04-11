from supriya.ugens.UGen import UGen


class Duty(UGen):
    """
    A value is demanded of each UGen in the list and output according to a stream of duration values.

    ::

        >>> duty = supriya.ugens.Duty.kr(
        ...     done_action=0,
        ...     duration=supriya.ugens.Drand(
        ...         sequence=[0.01, 0.2, 0.4],
        ...         repeats=2,
        ...     ),
        ...     reset=0,
        ...     level=supriya.ugens.Dseq(
        ...         sequence=[204, 400, 201, 502, 300, 200],
        ...         repeats=2,
        ...         ),
        ...     )
        >>> duty
        Duty.kr()

    """

    # ### CLASS VARIABLES ###

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
        """
        Constructs an audio-rate Duty.

        ::

            >>> duty = supriya.ugens.Duty.ar(
            ...     done_action=0,
            ...     duration=supriya.ugens.Drand(
            ...         sequence=[0.01, 0.2, 0.4],
            ...         repeats=2,
            ...     ),
            ...     reset=0,
            ...     level=supriya.ugens.Dseq(
            ...         sequence=[204, 400, 201, 502, 300, 200],
            ...         repeats=2,
            ...         ),
            ...     )
            >>> duty
            Duty.ar()

        Returns ugen graph.
        """
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
        """
        Constructs a control-rate Duty.

        ::

            >>> duty = supriya.ugens.Duty.kr(
            ...     done_action=0,
            ...     duration=supriya.ugens.Drand(
            ...         sequence=[0.01, 0.2, 0.4],
            ...         repeats=2,
            ...     ),
            ...     reset=0,
            ...     level=supriya.ugens.Dseq(
            ...         sequence=[204, 400, 201, 502, 300, 200],
            ...         repeats=2,
            ...         ),
            ...     )
            >>> duty
            Duty.kr()

        Returns ugen graph.
        """
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

    # ### PUBLIC PROPERTIES ###

    @property
    def done_action(self):
        """
        Gets `done_action` input of Duty.

        ::

            >>> duty = supriya.ugens.Duty.ar(
            ...     done_action=0,
            ...     duration=supriya.ugens.Drand(
            ...         sequence=[0.01, 0.2, 0.4],
            ...         repeats=2,
            ...     ),
            ...     reset=0,
            ...     level=supriya.ugens.Dseq(
            ...         sequence=[204, 400, 201, 502, 300, 200],
            ...         repeats=2,
            ...         ),
            ...     )
            >>> duty.done_action
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('done_action')
        return self._inputs[index]

    @property
    def duration(self):
        """
        Gets `duration` input of Duty.

        ::

            >>> duty = supriya.ugens.Duty.ar(
            ...     done_action=0,
            ...     duration=supriya.ugens.Drand(
            ...         sequence=[0.01, 0.2, 0.4],
            ...         repeats=2,
            ...     ),
            ...     reset=0,
            ...     level=supriya.ugens.Dseq(
            ...         sequence=[204, 400, 201, 502, 300, 200],
            ...         repeats=2,
            ...         ),
            ...     )
            >>> duty.duration
            Drand()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('duration')
        return self._inputs[index]

    @property
    def level(self):
        """
        Gets `level` input of Duty.

        ::

            >>> duty = supriya.ugens.Duty.ar(
            ...     done_action=0,
            ...     duration=supriya.ugens.Drand(
            ...         sequence=[0.01, 0.2, 0.4],
            ...         repeats=2,
            ...     ),
            ...     reset=0,
            ...     level=supriya.ugens.Dseq(
            ...         sequence=[204, 400, 201, 502, 300, 200],
            ...         repeats=2,
            ...         ),
            ...     )
            >>> duty.level
            Dseq()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('level')
        return self._inputs[index]

    @property
    def reset(self):
        """
        Gets `reset` input of Duty.

        ::

            >>> duty = supriya.ugens.Duty.ar(
            ...     done_action=0,
            ...     duration=supriya.ugens.Drand(
            ...         sequence=[0.01, 0.2, 0.4],
            ...         repeats=2,
            ...     ),
            ...     reset=0,
            ...     level=supriya.ugens.Dseq(
            ...         sequence=[204, 400, 201, 502, 300, 200],
            ...         repeats=2,
            ...         ),
            ...     )
            >>> duty.reset
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('reset')
        return self._inputs[index]
