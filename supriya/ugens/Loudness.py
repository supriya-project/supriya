from supriya.tools.synthdeftools.CalculationRate import CalculationRate
from supriya.ugens.UGen import UGen


class Loudness(UGen):
    """
    Extraction of instantaneous loudness in `sones`.

    ::

        >>> source = supriya.ugens.SoundIn.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT(source=source)
        >>> loudness = supriya.ugens.Loudness.kr(
        ...     pv_chain=pv_chain,
        ...     smask=0.25,
        ...     tmask=1,
        ...     )
        >>> loudness
        Loudness.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Machine Listening UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        'smask',
        'tmask',
        )

    _valid_calculation_rates = (
        CalculationRate.CONTROL,
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pv_chain=None,
        smask=0.25,
        tmask=1,
        ):
        UGen.__init__(
            self,
            calculation_rate=CalculationRate.CONTROL,
            pv_chain=pv_chain,
            smask=smask,
            tmask=tmask,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        pv_chain=None,
        smask=0.25,
        tmask=1,
        ):
        """
        Constructs a control-rate Loudness.

        ::

            >>> source = supriya.ugens.SoundIn.ar(bus=0)
            >>> pv_chain = supriya.ugens.FFT(source=source)
            >>> loudness = supriya.ugens.Loudness.kr(
            ...     pv_chain=pv_chain,
            ...     smask=0.25,
            ...     tmask=1,
            ...     )
            >>> loudness
            Loudness.kr()

        Returns ugen graph.
        """
        ugen = cls._new_expanded(
            pv_chain=pv_chain,
            smask=smask,
            tmask=tmask,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        """
        Gets `pv_chain` input of Loudness.

        ::

            >>> source = supriya.ugens.SoundIn.ar(bus=0)
            >>> pv_chain = supriya.ugens.FFT(source=source)
            >>> loudness = supriya.ugens.Loudness.kr(
            ...     pv_chain=pv_chain,
            ...     smask=0.25,
            ...     tmask=1,
            ...     )
            >>> loudness.pv_chain
            FFT.kr()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]

    @property
    def smask(self):
        """
        Gets `smask` input of Loudness.

        ::

            >>> source = supriya.ugens.SoundIn.ar(bus=0)
            >>> pv_chain = supriya.ugens.FFT(source=source)
            >>> loudness = supriya.ugens.Loudness.kr(
            ...     pv_chain=pv_chain,
            ...     smask=0.25,
            ...     tmask=1,
            ...     )
            >>> loudness.smask
            0.25

        Returns ugen input.
        """
        index = self._ordered_input_names.index('smask')
        return self._inputs[index]

    @property
    def tmask(self):
        """
        Gets `tmask` input of Loudness.

        ::

            >>> source = supriya.ugens.SoundIn.ar(bus=0)
            >>> pv_chain = supriya.ugens.FFT(source=source)
            >>> loudness = supriya.ugens.Loudness.kr(
            ...     pv_chain=pv_chain,
            ...     smask=0.25,
            ...     tmask=1,
            ...     )
            >>> loudness.tmask
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('tmask')
        return self._inputs[index]
