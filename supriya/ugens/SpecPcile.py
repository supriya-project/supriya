from supriya.tools.synthdeftools.CalculationRate import CalculationRate
from supriya.ugens.UGen import UGen


class SpecPcile(UGen):
    """
    Find a percentile of FFT magnitude spectrum.

    ::

        >>> source = supriya.ugens.SoundIn.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT(source=source)
        >>> spec_pcile = supriya.ugens.SpecPcile.kr(
        ...     pv_chain=pv_chain,
        ...     fraction=0.5,
        ...     interpolate=0,
        ...     )
        >>> spec_pcile
        SpecPcile.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Machine Listening UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        'fraction',
        'interpolate',
        )

    _valid_calculation_rates = (
        CalculationRate.CONTROL,
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pv_chain=None,
        fraction=0.5,
        interpolate=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=CalculationRate.CONTROL,
            pv_chain=pv_chain,
            fraction=fraction,
            interpolate=interpolate,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        pv_chain=None,
        fraction=0.5,
        interpolate=0,
        ):
        """
        Constructs a control-rate SpecPcile.

        ::

            >>> source = supriya.ugens.SoundIn.ar(bus=0)
            >>> pv_chain = supriya.ugens.FFT(source=source)
            >>> spec_pcile = supriya.ugens.SpecPcile.kr(
            ...     pv_chain=pv_chain,
            ...     fraction=0.5,
            ...     interpolate=0,
            ...     )
            >>> spec_pcile
            SpecPcile.kr()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        ugen = cls._new_expanded(
            pv_chain=pv_chain,
            fraction=fraction,
            interpolate=interpolate,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        """
        Gets `pv_chain` input of SpecPcile.

        ::

            >>> source = supriya.ugens.SoundIn.ar(bus=0)
            >>> pv_chain = supriya.ugens.FFT(source=source)
            >>> spec_pcile = supriya.ugens.SpecPcile.kr(
            ...     pv_chain=pv_chain,
            ...     fraction=0.5,
            ...     interpolate=0,
            ...     )
            >>> spec_pcile.pv_chain
            FFT.kr()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]

    @property
    def fraction(self):
        """
        Gets `fraction` input of SpecPcile.

        ::

            >>> source = supriya.ugens.SoundIn.ar(bus=0)
            >>> pv_chain = supriya.ugens.FFT(source=source)
            >>> spec_pcile = supriya.ugens.SpecPcile.kr(
            ...     pv_chain=pv_chain,
            ...     fraction=0.5,
            ...     interpolate=0,
            ...     )
            >>> spec_pcile.fraction
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('fraction')
        return self._inputs[index]

    @property
    def interpolate(self):
        """
        Gets `interpolate` input of SpecPcile.

        ::

            >>> source = supriya.ugens.SoundIn.ar(bus=0)
            >>> pv_chain = supriya.ugens.FFT(source=source)
            >>> spec_pcile = supriya.ugens.SpecPcile.kr(
            ...     pv_chain=pv_chain,
            ...     fraction=0.5,
            ...     interpolate=0,
            ...     )
            >>> spec_pcile.interpolate
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('interpolate')
        return self._inputs[index]
