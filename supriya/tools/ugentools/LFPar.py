# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class LFPar(PureUGen):
    """
    A parabolic oscillator unit generator.

    ::

        >>> ugentools.LFPar.ar()
        LFPar.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Oscillator UGens'

    __slots__ = ()

    _ordered_input_names = (
        'frequency',
        'initial_phase',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        frequency=440.,
        initial_phase=0.,
        ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            frequency=frequency,
            initial_phase=initial_phase,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=440,
        initial_phase=0,
        ):
        """
        Constructs an audio-rate parabolic oscillator.

        ::

            >>> ugentools.LFPar.ar(
            ...     frequency=443,
            ...     initial_phase=0.25,
            ...     )
            LFPar.ar()

        Returns unit generator graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            initial_phase=initial_phase,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        frequency=440,
        initial_phase=0,
        ):
        """
        Constructs a control-rate parabolic oscillator.

        ::

            >>> ugentools.LFPar.kr(
            ...     frequency=443,
            ...     initial_phase=0.25,
            ...     )
            LFPar.kr()

        Returns unit generator graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            initial_phase=initial_phase,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def frequency(self):
        """
        Gets `frequency` input of LFPar.

        ::

            >>> frequency = 442
            >>> lfpar = ugentools.LFPar.ar(
            ...     frequency=frequency,
            ...     )
            >>> lfpar.frequency
            442.0

        Returns input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def initial_phase(self):
        """
        Gets `initial_phase` input of LFPar.

        ::

            >>> initial_phase = 0.5
            >>> lfpar = ugentools.LFPar.ar(
            ...     initial_phase=initial_phase,
            ...     )
            >>> lfpar.initial_phase
            0.5

        Returns input.
        """
        index = self._ordered_input_names.index('initial_phase')
        return self._inputs[index]
