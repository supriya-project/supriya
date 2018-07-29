from supriya.synthdefs.SignalRange import SignalRange
from supriya.ugens.UGen import UGen


class Dust(UGen):
    """
    A unipolar random impulse generator.

    ::

        >>> dust = supriya.ugens.Dust.ar(
        ...    density=23,
        ...    )
        >>> dust
        Dust.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Noise UGens'

    __slots__ = ()

    _ordered_input_names = (
        'density',
        )

    _signal_range = SignalRange.UNIPOLAR

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        density=0.,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            density=density,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        density=0,
        ):
        """
        Constructs an audio-rate unipolar random impulse generator.

        ::

            >>> supriya.ugens.Dust.ar(
            ...     density=[1, 2],
            ...     )
            UGenArray({2})

        Returns unit generator graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            density=density,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        density=0,
        ):
        """
        Constructs a control-rate unipolar random impulse generator.

        ::

            >>> supriya.ugens.Dust.kr(
            ...     density=[1, 2],
            ...     )
            UGenArray({2})

        Returns unit generator graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            density=density,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def density(self):
        """
        Gets `density` input of Dust.

        ::

            >>> density = 0.25
            >>> dust = supriya.ugens.Dust.ar(
            ...     density=density,
            ...     )
            >>> dust.density
            0.25

        Returns input.
        """
        index = self._ordered_input_names.index('density')
        return self._inputs[index]
