from supriya.tools.ugentools.Delay1 import Delay1


class Delay2(Delay1):
    """
    A two-sample delay line unit generator.

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> ugentools.Delay2.ar(source=source)
        Delay2.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Delay UGens'

    __slots__ = ()

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        delay_time=0.2,
        maximum_delay_time=0.2,
        source=None,
        ):
        """
        Constructs an audio-rate two-sample delay line.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> ugentools.Delay2.ar(
            ...     source=source,
            ...     )
            Delay2.ar()

        Returns unit generator graph.
        """
        return super(Delay2, cls).ar(
            source=source,
            )

    @classmethod
    def kr(
        cls,
        source=None,
        ):
        """
        Constructs a control-rate two-sample delay line.

        ::

            >>> source = ugentools.In.kr(bus=0)
            >>> ugentools.Delay2.kr(
            ...     source=source,
            ...     )
            Delay2.ar()

        Returns unit generator graph.
        """
        return super(Delay2, cls).kr(
            source=source,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        """
        Gets `source` input of Delay2.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> delay_2 = ugentools.Delay2.ar(
            ...     source=source,
            ...     )
            >>> delay_2.source
            In.ar()[0]

        Returns input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
