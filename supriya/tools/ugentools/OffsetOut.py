# -*- encoding: utf-8 -*-
import collections
from supriya.tools.ugentools.UGen import UGen


class OffsetOut(UGen):
    r"""
    A bus output unit generator with sample-accurate timing.

    ::

        >>> source = ugentools.SinOsc.ar()
        >>> ugentools.OffsetOut.ar(
        ...     bus=0,
        ...     source=source,
        ...     )
        OffsetOut.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Input/Output UGens'

    __slots__ = ()

    _ordered_input_names = (
        'bus',
        'source',
        )

    _unexpanded_input_names = (
        'source',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        bus=0,
        source=None,
        ):
        if not isinstance(source, collections.Sequence):
            source = [source]
        UGen.__init__(
            self,
            bus=bus,
            calculation_rate=calculation_rate,
            source=source,
            )

    ### PRIVATE METHODS ###

    def _get_outputs(self):
        return []

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        bus=0,
        source=None,
        ):
        r"""
        Constructs a sample-accurately-timed audio-rate bus output.

        ::

            >>> source = ugentools.SinOsc.ar(frequency=[440, 442])
            >>> offset_out = ugentools.OffsetOut.ar(
            ...     bus=0,
            ...     source=source,
            ...     )
            >>> offset_out
            OffsetOut.ar()

        Returns ugen graph.
        """
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        prototype = (
            servertools.Bus,
            servertools.BusGroup,
            servertools.BusProxy,
            )
        if isinstance(bus, prototype):
            bus = int(bus)
        return cls._new_expanded(
            bus=bus,
            calculation_rate=calculation_rate,
            source=source,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def bus(self):
        r"""
        Gets `bus` input of OffsetOut.

        ::

            >>> bus = 0
            >>> source = ugentools.WhiteNoise.ar()
            >>> offset_out = ugentools.OffsetOut.ar(
            ...     bus=bus,
            ...     source=source,
            ...     )
            >>> offset_out.bus
            0.0

        Returns input.
        """
        index = self._ordered_input_names.index('bus')
        return self._inputs[index]

    @property
    def is_output_ugen(self):
        return True

    @property
    def source(self):
        r"""
        Gets `source` input of OffsetOut.

        ::

            >>> bus = 0
            >>> source = ugentools.WhiteNoise.ar()
            >>> out = ugentools.OffsetOut.ar(
            ...     bus=bus,
            ...     source=source,
            ...     )
            >>> out.source
            (OutputProxy(
                source=WhiteNoise(
                    calculation_rate=CalculationRate.AUDIO
                    ),
                output_index=0
                ),)

        Returns input.
        """
        index = self._ordered_input_names.index('source')
        return tuple(self._inputs[index:])
