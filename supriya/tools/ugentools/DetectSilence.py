from supriya.tools.ugentools.Filter import Filter


class DetectSilence(Filter):
    """
    Evaluates `done_action` when input falls below `threshold`.

    ::

        >>> source = ugentools.WhiteNoise.ar()
        >>> source *= ugentools.Line.kr(start=1, stop=0)
        >>> detect_silence = ugentools.DetectSilence.kr(
        ...     done_action=DoneAction.FREE_SYNTH,
        ...     source=source,
        ...     threshold=0.0001,
        ...     time=1.0,
        ...     )
        >>> detect_silence
        DetectSilence.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Envelope Utility UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'threshold',
        'time',
        'done_action',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        done_action=0,
        source=0,
        threshold=0.0001,
        time=0.1,
        ):
        Filter.__init__(
            self,
            calculation_rate=calculation_rate,
            threshold=threshold,
            done_action=done_action,
            source=source,
            time=time,
            )

    ### PRIVATE METHODS ###

    def _optimize_graph(self, sort_bundles):
        pass

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        threshold=0.0001,
        done_action=0,
        source=0,
        time=0.1,
        ):
        """
        Constructs an audio-rate DetectSilence.

        ::

            >>> source = ugentools.WhiteNoise.ar()
            >>> source *= ugentools.Line.kr(start=1, stop=0)
            >>> detect_silence = ugentools.DetectSilence.ar(
            ...     done_action=DoneAction.FREE_SYNTH,
            ...     source=source,
            ...     threshold=0.0001,
            ...     time=1.0,
            ...     )
            >>> detect_silence
            DetectSilence.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            threshold=threshold,
            done_action=done_action,
            source=source,
            time=time,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        threshold=0.0001,
        done_action=0,
        source=0,
        time=0.1,
        ):
        """
        Constructs a control-rate DetectSilence.

        ::

            >>> source = ugentools.WhiteNoise.ar()
            >>> source *= ugentools.Line.kr(start=1, stop=0)
            >>> detect_silence = ugentools.DetectSilence.kr(
            ...     done_action=DoneAction.FREE_SYNTH,
            ...     source=source,
            ...     threshold=0.0001,
            ...     time=1.0,
            ...     )
            >>> detect_silence
            DetectSilence.kr()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            threshold=threshold,
            done_action=done_action,
            source=source,
            time=time,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def done_action(self):
        """
        Gets `done_action` input of DetectSilence.

        ::

            >>> source = ugentools.WhiteNoise.ar()
            >>> source *= ugentools.Line.kr(start=1, stop=0)
            >>> detect_silence = ugentools.DetectSilence.kr(
            ...     done_action=DoneAction.FREE_SYNTH,
            ...     source=source,
            ...     threshold=0.0001,
            ...     time=1.0,
            ...     )
            >>> detect_silence.done_action
            2.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('done_action')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of DetectSilence.

        ::

            >>> source = ugentools.WhiteNoise.ar()
            >>> source *= ugentools.Line.kr(start=1, stop=0)
            >>> detect_silence = ugentools.DetectSilence.kr(
            ...     done_action=DoneAction.FREE_SYNTH,
            ...     source=source,
            ...     threshold=0.0001,
            ...     time=1.0,
            ...     )
            >>> detect_silence.source
            OutputProxy(
                source=BinaryOpUGen(
                    left=OutputProxy(
                        source=WhiteNoise(
                            calculation_rate=CalculationRate.AUDIO
                            ),
                        output_index=0
                        ),
                    right=OutputProxy(
                        source=Line(
                            calculation_rate=CalculationRate.CONTROL,
                            done_action=0.0,
                            duration=1.0,
                            start=1.0,
                            stop=0.0
                            ),
                        output_index=0
                        ),
                    calculation_rate=CalculationRate.AUDIO,
                    special_index=2
                    ),
                output_index=0
                )

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def threshold(self):
        """
        Gets `threshold` input of DetectSilence.

        ::

            >>> source = ugentools.WhiteNoise.ar()
            >>> source *= ugentools.Line.kr(start=1, stop=0)
            >>> detect_silence = ugentools.DetectSilence.kr(
            ...     done_action=DoneAction.FREE_SYNTH,
            ...     source=source,
            ...     threshold=0.0001,
            ...     time=1.0,
            ...     )
            >>> detect_silence.threshold
            0.0001

        Returns ugen input.
        """
        index = self._ordered_input_names.index('threshold')
        return self._inputs[index]

    @property
    def time(self):
        """
        Gets `time` input of DetectSilence.

        ::

            >>> source = ugentools.WhiteNoise.ar()
            >>> source *= ugentools.Line.kr(start=1, stop=0)
            >>> detect_silence = ugentools.DetectSilence.kr(
            ...     done_action=DoneAction.FREE_SYNTH,
            ...     source=source,
            ...     threshold=0.0001,
            ...     time=1.0,
            ...     )
            >>> detect_silence.time
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('time')
        return self._inputs[index]
