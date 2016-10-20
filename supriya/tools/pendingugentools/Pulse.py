# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.UGen import UGen


class Pulse(UGen):
    """

    ::

        >>> pulse = ugentools.Pulse.ar(
        ...     frequency=440,
        ...     width=0.5,
        ...     )
        >>> pulse
        Pulse.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'frequency',
        'width',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        frequency=440,
        width=0.5,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            frequency=frequency,
            width=width,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=440,
        width=0.5,
        ):
        """
        Constructs an audio-rate Pulse.

        ::

            >>> pulse = ugentools.Pulse.ar(
            ...     frequency=440,
            ...     width=0.5,
            ...     )
            >>> pulse
            Pulse.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            width=width,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        frequency=440,
        width=0.5,
        ):
        """
        Constructs a control-rate Pulse.

        ::

            >>> pulse = ugentools.Pulse.kr(
            ...     frequency=440,
            ...     width=0.5,
            ...     )
            >>> pulse
            Pulse.kr()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            width=width,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def frequency(self):
        """
        Gets `frequency` input of Pulse.

        ::

            >>> pulse = ugentools.Pulse.ar(
            ...     frequency=440,
            ...     width=0.5,
            ...     )
            >>> pulse.frequency
            440.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def width(self):
        """
        Gets `width` input of Pulse.

        ::

            >>> pulse = ugentools.Pulse.ar(
            ...     frequency=440,
            ...     width=0.5,
            ...     )
            >>> pulse.width
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('width')
        return self._inputs[index]
