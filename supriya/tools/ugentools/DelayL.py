# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DelayN import DelayN


class DelayL(DelayN):
    r"""
    A linear-interpolating delay line unit generator.

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> ugentools.DelayL.ar(source=source)
        DelayL.ar()

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
        r"""
        Constructs an audio-rate linear-interpolating delay line.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> ugentools.DelayL.ar(
            ...     delay_time=0.5,
            ...     maximum_delay_time=1.0,
            ...     source=source,
            ...     )
            DelayL.ar()

        Returns unit generator graph.
        """
        return super(DelayL, cls).ar(
            delay_time=delay_time,
            maximum_delay_time=maximum_delay_time,
            source=source,
            )

    @classmethod
    def kr(
        cls,
        delay_time=0.2,
        maximum_delay_time=0.2,
        source=None,
        ):
        r"""
        Constructs a control-rate linear-interpolating delay line.

        ::

            >>> source = ugentools.In.kr(bus=0)
            >>> ugentools.DelayL.kr(
            ...     delay_time=0.5,
            ...     maximum_delay_time=1.0,
            ...     source=source,
            ...     )
            DelayL.ar()

        Returns unit generator graph.
        """
        return super(DelayL, cls).kr(
            delay_time=delay_time,
            maximum_delay_time=maximum_delay_time,
            source=source,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def delay_time(self):
        r"""
        Gets `delay_time` input of DelayL.

        ::

            >>> delay_time = 1.5
            >>> source = ugentools.In.ar(bus=0)
            >>> delay_l = ugentools.DelayL.ar(
            ...     delay_time=delay_time,
            ...     source=source,
            ...     )
            >>> delay_l.delay_time
            1.5

        Returns input.
        """
        index = self._ordered_input_names.index('delay_time')
        return self._inputs[index]

    @property
    def maximum_delay_time(self):
        r"""
        Gets `maximum_delay_time` input of DelayL.

        ::

            >>> maximum_delay_time = 2.0
            >>> source = ugentools.In.ar(bus=0)
            >>> delay_l = ugentools.DelayL.ar(
            ...     maximum_delay_time=maximum_delay_time,
            ...     source=source,
            ...     )
            >>> delay_l.maximum_delay_time
            2.0

        Returns input.
        """
        index = self._ordered_input_names.index('maximum_delay_time')
        return self._inputs[index]

    @property
    def source(self):
        r"""
        Gets `source` input of DelayL.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> delay_l = ugentools.DelayL.ar(
            ...     source=source,
            ...     )
            >>> delay_l.source
            OutputProxy(
                source=In(
                    bus=0.0,
                    calculation_rate=CalculationRate.AUDIO,
                    channel_count=1
                    ),
                output_index=0
                )

        Returns input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
