from supriya.ugens.Filter import Filter


class BRF(Filter):
    """
    A 2nd order Butterworth band-reject filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> b_r_f =supriya.ugens.BRF.ar(source=source)
        >>> b_r_f
        BRF.ar()

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
        Constructs an audio-rate band-reject filter.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> b_r_f = supriya.ugens.BRF.ar(
            ...     frequency=440,
            ...     reciprocal_of_q=1.0,
            ...     source=source,
            ...     )
            >>> b_r_f
            BRF.ar()

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
        Constructs a control-rate band-reject filter.

        ::

            >>> source = supriya.ugens.In.kr(bus=0)
            >>> b_r_f = supriya.ugens.BRF.kr(
            ...     frequency=440,
            ...     reciprocal_of_q=1.0,
            ...     source=source,
            ...     )
            >>> b_r_f
            BRF.kr()

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
        Gets `frequency` input of BRF.

        ::

            >>> frequency = 440.0
            >>> source = supriya.ugens.In.ar(bus=0)
            >>> brf = supriya.ugens.BRF.ar(
            ...     frequency=frequency,
            ...     source=source,
            ...     )
            >>> brf.frequency
            440.0

        Returns input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def reciprocal_of_q(self):
        """
        Gets `reciprocal_of_q` input of BRF.

        ::

            >>> reciprocal_of_q = 1.0
            >>> source = supriya.ugens.In.ar(bus=0)
            >>> brf = supriya.ugens.BRF.ar(
            ...     reciprocal_of_q=reciprocal_of_q,
            ...     source=source,
            ...     )
            >>> brf.reciprocal_of_q
            1.0

        Returns input.
        """
        index = self._ordered_input_names.index('reciprocal_of_q')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of BRF.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> brf = supriya.ugens.BRF.ar(
            ...     source=source,
            ...     )
            >>> brf.source
            In.ar()[0]

        Returns input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
