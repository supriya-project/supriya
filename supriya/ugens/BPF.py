from supriya.ugens.Filter import Filter


class BPF(Filter):
    """
    A 2nd order Butterworth bandpass filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> b_p_f = supriya.ugens.BPF.ar(source=source)
        >>> b_p_f
        BPF.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'frequency',
        'reciprocal_of_q',
        )

    ### PUBLIC METHODS ###

    def __init__(
        self,
        frequency=440,
        calculation_rate=None,
        reciprocal_of_q=1.0,
        source=None,
        ):
        Filter.__init__(
            self,
            frequency=frequency,
            calculation_rate=calculation_rate,
            reciprocal_of_q=reciprocal_of_q,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=440,
        reciprocal_of_q=1.0,
        source=None,
        ):
        """
        Constructs an audio-rate bandpass filter.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> b_p_f = supriya.ugens.BPF.ar(
            ...     frequency=440,
            ...     reciprocal_of_q=1.0,
            ...     source=source,
            ...     )
            >>> b_p_f
            BPF.ar()

        Returns unit generator graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            frequency=frequency,
            calculation_rate=calculation_rate,
            reciprocal_of_q=reciprocal_of_q,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        frequency=440,
        reciprocal_of_q=1.0,
        source=None,
        ):
        """
        Constructs a control-rate bandpass filter.

        ::

            >>> source = supriya.ugens.In.kr(bus=0)
            >>> b_p_f = supriya.ugens.BPF.kr(
            ...     frequency=440,
            ...     reciprocal_of_q=1.0,
            ...     source=source,
            ...     )
            >>> b_p_f
            BPF.kr()

        Returns unit generator graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            frequency=frequency,
            calculation_rate=calculation_rate,
            reciprocal_of_q=reciprocal_of_q,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def frequency(self):
        """
        Gets `frequency` input of BPF.

        ::

            >>> frequency = 440.0
            >>> source = supriya.ugens.In.ar(bus=0)
            >>> bpf = supriya.ugens.BPF.ar(
            ...     frequency=frequency,
            ...     source=source,
            ...     )
            >>> bpf.frequency
            440.0

        Returns input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def reciprocal_of_q(self):
        """
        Gets `reciprocal_of_q` input of BPF.

        ::

            >>> reciprocal_of_q = 1.0
            >>> source = supriya.ugens.In.ar(bus=0)
            >>> bpf = supriya.ugens.BPF.ar(
            ...     reciprocal_of_q=reciprocal_of_q,
            ...     source=source,
            ...     )
            >>> bpf.reciprocal_of_q
            1.0

        Returns input.
        """
        index = self._ordered_input_names.index('reciprocal_of_q')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of BPF.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> bpf = supriya.ugens.BPF.ar(
            ...     source=source,
            ...     )
            >>> bpf.source
            In.ar()[0]

        Returns input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
