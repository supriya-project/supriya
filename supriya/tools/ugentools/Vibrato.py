# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class Vibrato(PureUGen):
    """
    Vibrato is a slow frequency modulation.

    ::

        >>> vibrato = ugentools.Vibrato.ar(
        ...     delay=0,
        ...     depth=0.02,
        ...     depth_variation=0.1,
        ...     frequency=440,
        ...     initial_phase=0,
        ...     onset=0,
        ...     rate=6,
        ...     rate_variation=0.04,
        ...     )
        >>> vibrato
        Vibrato.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'frequency',
        'rate',
        'depth',
        'delay',
        'onset',
        'rate_variation',
        'depth_variation',
        'initial_phase',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        delay=0,
        depth=0.02,
        depth_variation=0.1,
        frequency=440,
        initial_phase=0,
        onset=0,
        rate=6,
        rate_variation=0.04,
        ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            delay=delay,
            depth=depth,
            depth_variation=depth_variation,
            frequency=frequency,
            initial_phase=initial_phase,
            onset=onset,
            rate=rate,
            rate_variation=rate_variation,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        delay=0,
        depth=0.02,
        depth_variation=0.1,
        frequency=440,
        initial_phase=0,
        onset=0,
        rate=6,
        rate_variation=0.04,
        ):
        """
        Constructs an audio-rate Vibrato.

        ::

            >>> vibrato = ugentools.Vibrato.ar(
            ...     delay=0,
            ...     depth=0.02,
            ...     depth_variation=0.1,
            ...     frequency=440,
            ...     initial_phase=0,
            ...     onset=0,
            ...     rate=6,
            ...     rate_variation=0.04,
            ...     )
            >>> vibrato
            Vibrato.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            delay=delay,
            depth=depth,
            depth_variation=depth_variation,
            frequency=frequency,
            initial_phase=initial_phase,
            onset=onset,
            rate=rate,
            rate_variation=rate_variation,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        delay=0,
        depth=0.02,
        depth_variation=0.1,
        frequency=440,
        initial_phase=0,
        onset=0,
        rate=6,
        rate_variation=0.04,
        ):
        """
        Constructs a control-rate Vibrato.

        ::

            >>> vibrato = ugentools.Vibrato.kr(
            ...     delay=0,
            ...     depth=0.02,
            ...     depth_variation=0.1,
            ...     frequency=440,
            ...     initial_phase=0,
            ...     onset=0,
            ...     rate=6,
            ...     rate_variation=0.04,
            ...     )
            >>> vibrato
            Vibrato.kr()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            delay=delay,
            depth=depth,
            depth_variation=depth_variation,
            frequency=frequency,
            initial_phase=initial_phase,
            onset=onset,
            rate=rate,
            rate_variation=rate_variation,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def delay(self):
        """
        Gets `delay` input of Vibrato.

        ::

            >>> vibrato = ugentools.Vibrato.ar(
            ...     delay=0,
            ...     depth=0.02,
            ...     depth_variation=0.1,
            ...     frequency=440,
            ...     initial_phase=0,
            ...     onset=0,
            ...     rate=6,
            ...     rate_variation=0.04,
            ...     )
            >>> vibrato.delay
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('delay')
        return self._inputs[index]

    @property
    def depth(self):
        """
        Gets `depth` input of Vibrato.

        ::

            >>> vibrato = ugentools.Vibrato.ar(
            ...     delay=0,
            ...     depth=0.02,
            ...     depth_variation=0.1,
            ...     frequency=440,
            ...     initial_phase=0,
            ...     onset=0,
            ...     rate=6,
            ...     rate_variation=0.04,
            ...     )
            >>> vibrato.depth
            0.02

        Returns ugen input.
        """
        index = self._ordered_input_names.index('depth')
        return self._inputs[index]

    @property
    def depth_variation(self):
        """
        Gets `depth_variation` input of Vibrato.

        ::

            >>> vibrato = ugentools.Vibrato.ar(
            ...     delay=0,
            ...     depth=0.02,
            ...     depth_variation=0.1,
            ...     frequency=440,
            ...     initial_phase=0,
            ...     onset=0,
            ...     rate=6,
            ...     rate_variation=0.04,
            ...     )
            >>> vibrato.depth_variation
            0.1

        Returns ugen input.
        """
        index = self._ordered_input_names.index('depth_variation')
        return self._inputs[index]

    @property
    def frequency(self):
        """
        Gets `frequency` input of Vibrato.

        ::

            >>> vibrato = ugentools.Vibrato.ar(
            ...     delay=0,
            ...     depth=0.02,
            ...     depth_variation=0.1,
            ...     frequency=440,
            ...     initial_phase=0,
            ...     onset=0,
            ...     rate=6,
            ...     rate_variation=0.04,
            ...     )
            >>> vibrato.frequency
            440.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def initial_phase(self):
        """
        Gets `initial_phase` input of Vibrato.

        ::

            >>> vibrato = ugentools.Vibrato.ar(
            ...     delay=0,
            ...     depth=0.02,
            ...     depth_variation=0.1,
            ...     frequency=440,
            ...     initial_phase=0,
            ...     onset=0,
            ...     rate=6,
            ...     rate_variation=0.04,
            ...     )
            >>> vibrato.initial_phase
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('initial_phase')
        return self._inputs[index]

    @property
    def onset(self):
        """
        Gets `onset` input of Vibrato.

        ::

            >>> vibrato = ugentools.Vibrato.ar(
            ...     delay=0,
            ...     depth=0.02,
            ...     depth_variation=0.1,
            ...     frequency=440,
            ...     initial_phase=0,
            ...     onset=0,
            ...     rate=6,
            ...     rate_variation=0.04,
            ...     )
            >>> vibrato.onset
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('onset')
        return self._inputs[index]

    @property
    def rate(self):
        """
        Gets `rate` input of Vibrato.

        ::

            >>> vibrato = ugentools.Vibrato.ar(
            ...     delay=0,
            ...     depth=0.02,
            ...     depth_variation=0.1,
            ...     frequency=440,
            ...     initial_phase=0,
            ...     onset=0,
            ...     rate=6,
            ...     rate_variation=0.04,
            ...     )
            >>> vibrato.rate
            6.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('rate')
        return self._inputs[index]

    @property
    def rate_variation(self):
        """
        Gets `rate_variation` input of Vibrato.

        ::

            >>> vibrato = ugentools.Vibrato.ar(
            ...     delay=0,
            ...     depth=0.02,
            ...     depth_variation=0.1,
            ...     frequency=440,
            ...     initial_phase=0,
            ...     onset=0,
            ...     rate=6,
            ...     rate_variation=0.04,
            ...     )
            >>> vibrato.rate_variation
            0.04

        Returns ugen input.
        """
        index = self._ordered_input_names.index('rate_variation')
        return self._inputs[index]
