from supriya.ugens.CombN import CombN


class CombC(CombN):
    """
    A cubic-interpolating comb delay line unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.CombC.ar(source=source)
        CombC.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Delay UGens'

    __slots__ = ()

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        decay_time=1.0,
        delay_time=0.2,
        maximum_delay_time=0.2,
        source=None,
        ):
        """
        Constructs an audio-rate cubic-interpolating comb delay line.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> supriya.ugens.CombC.ar(
            ...     decay_time=1.0,
            ...     delay_time=0.2,
            ...     maximum_delay_time=0.2,
            ...     source=source,
            ...     )
            CombC.ar()

        Returns unit generator graph.
        """
        return super(CombC, cls).ar(
            delay_time=delay_time,
            maximum_delay_time=maximum_delay_time,
            source=source,
            )

    @classmethod
    def kr(
        cls,
        decay_time=1.0,
        delay_time=0.2,
        maximum_delay_time=0.2,
        source=None,
        ):
        """
        Constructs a control-rate cubic-interpolating comb delay line.

        ::

            >>> source = supriya.ugens.In.kr(bus=0)
            >>> supriya.ugens.CombC.kr(
            ...     decay_time=1.0,
            ...     delay_time=0.2,
            ...     maximum_delay_time=0.2,
            ...     source=source,
            ...     )
            CombC.ar()

        Returns unit generator graph.
        """
        return super(CombC, cls).kr(
            delay_time=delay_time,
            maximum_delay_time=maximum_delay_time,
            source=source,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def decay_time(self):
        """
        Gets `decay_time` input of CombC.

        ::

            >>> decay_time = 1.0
            >>> source = supriya.ugens.In.ar(bus=0)
            >>> comb_c = supriya.ugens.CombC.ar(
            ...     decay_time=decay_time,
            ...     source=source,
            ...     )
            >>> comb_c.decay_time
            1.0

        Returns input.
        """
        index = self._ordered_input_names.index('decay_time')
        return self._inputs[index]

    @property
    def delay_time(self):
        """
        Gets `delay_time` input of CombC.

        ::

            >>> delay_time = 1.5
            >>> source = supriya.ugens.In.ar(bus=0)
            >>> comb_c = supriya.ugens.CombC.ar(
            ...     delay_time=delay_time,
            ...     source=source,
            ...     )
            >>> comb_c.delay_time
            1.5

        Returns input.
        """
        index = self._ordered_input_names.index('delay_time')
        return self._inputs[index]

    @property
    def maximum_delay_time(self):
        """
        Gets `maximum_delay_time` input of CombC.

        ::

            >>> maximum_delay_time = 2.0
            >>> source = supriya.ugens.In.ar(bus=0)
            >>> comb_c = supriya.ugens.CombC.ar(
            ...     maximum_delay_time=maximum_delay_time,
            ...     source=source,
            ...     )
            >>> comb_c.maximum_delay_time
            2.0

        Returns input.
        """
        index = self._ordered_input_names.index('maximum_delay_time')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of CombC.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> comb_c = supriya.ugens.CombC.ar(
            ...     source=source,
            ...     )
            >>> comb_c.source
            In.ar()[0]

        Returns input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
