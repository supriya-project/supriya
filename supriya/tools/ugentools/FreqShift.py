# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.UGen import UGen


class FreqShift(UGen):
    """

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> freq_shift = ugentools.FreqShift.ar(
        ...     frequency=0,
        ...     phase=0,
        ...     source=source,
        ...     )
        >>> freq_shift
        FreqShift.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'frequency',
        'phase',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        frequency=0,
        phase=0,
        source=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            frequency=frequency,
            phase=phase,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=0,
        phase=0,
        source=None,
        ):
        """
        Constructs an audio-rate FreqShift.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> freq_shift = ugentools.FreqShift.ar(
            ...     frequency=0,
            ...     phase=0,
            ...     source=source,
            ...     )
            >>> freq_shift
            FreqShift.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            phase=phase,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def frequency(self):
        """
        Gets `frequency` input of FreqShift.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> freq_shift = ugentools.FreqShift.ar(
            ...     frequency=0,
            ...     phase=0,
            ...     source=source,
            ...     )
            >>> freq_shift.frequency
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def phase(self):
        """
        Gets `phase` input of FreqShift.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> freq_shift = ugentools.FreqShift.ar(
            ...     frequency=0,
            ...     phase=0,
            ...     source=source,
            ...     )
            >>> freq_shift.phase
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('phase')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of FreqShift.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> freq_shift = ugentools.FreqShift.ar(
            ...     frequency=0,
            ...     phase=0,
            ...     source=source,
            ...     )
            >>> freq_shift.source
            OutputProxy(
                source=In(
                    bus=0.0,
                    calculation_rate=CalculationRate.AUDIO,
                    channel_count=1
                    ),
                output_index=0
                )

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
