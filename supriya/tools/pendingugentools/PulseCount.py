# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.UGen import UGen


class PulseCount(UGen):
    r"""

    ::

        >>> pulse_count = ugentools.PulseCount.ar(
        ...     reset=0,
        ...     trigger=0,
        ...     )
        >>> pulse_count
        PulseCount.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'trigger',
        'reset',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        reset=0,
        trigger=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            reset=reset,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        reset=0,
        trigger=0,
        ):
        r"""
        Constructs an audio-rate PulseCount.

        ::

            >>> pulse_count = ugentools.PulseCount.ar(
            ...     reset=0,
            ...     trigger=0,
            ...     )
            >>> pulse_count
            PulseCount.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            reset=reset,
            trigger=trigger,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        reset=0,
        trigger=0,
        ):
        r"""
        Constructs a control-rate PulseCount.

        ::

            >>> pulse_count = ugentools.PulseCount.kr(
            ...     reset=0,
            ...     trigger=0,
            ...     )
            >>> pulse_count
            PulseCount.kr()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            reset=reset,
            trigger=trigger,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def reset(self):
        r"""
        Gets `reset` input of PulseCount.

        ::

            >>> pulse_count = ugentools.PulseCount.ar(
            ...     reset=0,
            ...     trigger=0,
            ...     )
            >>> pulse_count.reset
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('reset')
        return self._inputs[index]

    @property
    def trigger(self):
        r"""
        Gets `trigger` input of PulseCount.

        ::

            >>> pulse_count = ugentools.PulseCount.ar(
            ...     reset=0,
            ...     trigger=0,
            ...     )
            >>> pulse_count.trigger
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]
