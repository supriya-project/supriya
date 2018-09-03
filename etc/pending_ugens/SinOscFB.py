import collections
from supriya.enums import CalculationRate
from supriya.ugens.PureUGen import PureUGen


class SinOscFB(PureUGen):
    """

    ::

        >>> sin_osc_fb = supriya.ugens.SinOscFB.ar(
        ...     feedback=0,
        ...     frequency=440,
        ...     )
        >>> sin_osc_fb
        SinOscFB.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        'frequency',
        'feedback',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        feedback=0,
        frequency=440,
        ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            feedback=feedback,
            frequency=frequency,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        feedback=0,
        frequency=440,
        ):
        """
        Constructs an audio-rate SinOscFB.

        ::

            >>> sin_osc_fb = supriya.ugens.SinOscFB.ar(
            ...     feedback=0,
            ...     frequency=440,
            ...     )
            >>> sin_osc_fb
            SinOscFB.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            feedback=feedback,
            frequency=frequency,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        feedback=0,
        frequency=440,
        ):
        """
        Constructs a control-rate SinOscFB.

        ::

            >>> sin_osc_fb = supriya.ugens.SinOscFB.kr(
            ...     feedback=0,
            ...     frequency=440,
            ...     )
            >>> sin_osc_fb
            SinOscFB.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            feedback=feedback,
            frequency=frequency,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def feedback(self):
        """
        Gets `feedback` input of SinOscFB.

        ::

            >>> sin_osc_fb = supriya.ugens.SinOscFB.ar(
            ...     feedback=0,
            ...     frequency=440,
            ...     )
            >>> sin_osc_fb.feedback
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('feedback')
        return self._inputs[index]

    @property
    def frequency(self):
        """
        Gets `frequency` input of SinOscFB.

        ::

            >>> sin_osc_fb = supriya.ugens.SinOscFB.ar(
            ...     feedback=0,
            ...     frequency=440,
            ...     )
            >>> sin_osc_fb.frequency
            440.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]
