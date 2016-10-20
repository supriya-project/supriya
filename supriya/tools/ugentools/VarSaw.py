# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class VarSaw(PureUGen):
    """
    A sawtooth-triangle oscillator with variable duty.

    ::

        >>> ugentools.VarSaw.ar()
        VarSaw.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Oscillator UGens'

    __slots__ = ()

    _ordered_input_names = (
        'frequency',
        'initial_phase',
        'width',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        frequency=440.,
        initial_phase=0.,
        calculation_rate=None,
        width=0.5,
        ):
        PureUGen.__init__(
            self,
            frequency=frequency,
            initial_phase=initial_phase,
            calculation_rate=calculation_rate,
            width=width,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=440,
        initial_phase=0.,
        width=0.5,
        ):
        """
        Constructs an audio-rate sawtooth-triangle oscillator with variable
        duty.

        ::

            >>> ugentools.VarSaw.ar(
            ...     frequency=443,
            ...     initial_phase=0.5,
            ...     width=0.25,
            ...     )
            VarSaw.ar()

        Returns unit generator graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            frequency=frequency,
            initial_phase=initial_phase,
            calculation_rate=calculation_rate,
            width=width,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        frequency=440,
        initial_phase=0.,
        width=0.5,
        ):
        """
        Constructs a control-rate sawtooth-triangle oscillator with variable
        duty.

        ::

            >>> ugentools.VarSaw.kr(
            ...     frequency=443,
            ...     initial_phase=0.5,
            ...     width=0.25,
            ...     )
            VarSaw.kr()

        Returns unit generator graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            frequency=frequency,
            initial_phase=initial_phase,
            calculation_rate=calculation_rate,
            width=width,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def frequency(self):
        """
        Gets `frequency` input of VarSaw.

        ::

            >>> frequency = 442
            >>> var_saw = ugentools.VarSaw.ar(
            ...     frequency=frequency,
            ...     )
            >>> var_saw.frequency
            442.0

        Returns input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def initial_phase(self):
        """
        Gets `initial_phase` input of VarSaw.

        ::

            >>> initial_phase = 0.25
            >>> var_saw = ugentools.VarSaw.ar(
            ...     initial_phase=initial_phase,
            ...     )
            >>> var_saw.initial_phase
            0.25

        Returns input.
        """
        index = self._ordered_input_names.index('initial_phase')
        return self._inputs[index]

    @property
    def width(self):
        """
        Gets `width` input of VarSaw.

        ::

            >>> width = 0.9
            >>> var_saw = ugentools.VarSaw.ar(
            ...     width=width,
            ...     )
            >>> var_saw.width
            0.9

        Returns input.
        """
        index = self._ordered_input_names.index('width')
        return self._inputs[index]
