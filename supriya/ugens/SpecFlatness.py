from supriya.tools.synthdeftools.CalculationRate import CalculationRate
from supriya.ugens.UGen import UGen


class SpecFlatness(UGen):
    """
    A spectral flatness measure.

    ::

        >>> source = supriya.ugens.SoundIn.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT(source=source)
        >>> spec_flatness = supriya.ugens.SpecFlatness.kr(
        ...     pv_chain=pv_chain,
        ...     )
        >>> spec_flatness
        SpecFlatness.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Machine Listening UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        )

    _valid_calculation_rates = (
        CalculationRate.CONTROL,
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pv_chain=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=CalculationRate.CONTROL,
            pv_chain=pv_chain,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        pv_chain=None,
        ):
        """
        Constructs a control-rate SpecFlatness.

        ::

            >>> source = supriya.ugens.SoundIn.ar(bus=0)
            >>> pv_chain = supriya.ugens.FFT(source=source)
            >>> spec_flatness = supriya.ugens.SpecFlatness.kr(
            ...     pv_chain=pv_chain,
            ...     )
            >>> spec_flatness
            SpecFlatness.kr()

        Returns ugen graph.
        """
        ugen = cls._new_expanded(
            pv_chain=pv_chain,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        """
        Gets `pv_chain` input of SpecFlatness.

        ::

            >>> source = supriya.ugens.SoundIn.ar(bus=0)
            >>> pv_chain = supriya.ugens.FFT(source=source)
            >>> spec_flatness = supriya.ugens.SpecFlatness.kr(
            ...     pv_chain=pv_chain,
            ...     )
            >>> spec_flatness.pv_chain
            FFT.kr()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]
