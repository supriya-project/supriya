from supriya.tools.synthdeftools.CalculationRate import CalculationRate
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class MFCC(MultiOutUGen):
    """
    Mel frequency cepstral coefficients.

    ::

        >>> source = ugentools.SoundIn.ar(bus=0)
        >>> pv_chain = ugentools.FFT(source=source)
        >>> mfcc = ugentools.MFCC.kr(
        ...     pv_chain=pv_chain,
        ...     channel_count=13,
        ...     )
        >>> mfcc
        UGenArray({13})

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
        channel_count=13,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=CalculationRate.CONTROL,
            pv_chain=pv_chain,
            channel_count=channel_count,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        pv_chain=None,
        channel_count=13,
        ):
        """
        Constructs a control-rate MFCC.

        ::

            >>> source = ugentools.SoundIn.ar(bus=0)
            >>> pv_chain = ugentools.FFT(source=source)
            >>> mfcc = ugentools.MFCC.kr(
            ...     pv_chain=pv_chain,
            ...     channel_count=13,
            ...     )
            >>> mfcc
            UGenArray({13})

        Returns ugen graph.
        """
        ugen = cls._new_expanded(
            pv_chain=pv_chain,
            channel_count=channel_count,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        """
        Gets `pv_chain` input of MFCC.

        ::

            >>> source = ugentools.SoundIn.ar(bus=0)
            >>> pv_chain = ugentools.FFT(source=source)
            >>> mfcc = ugentools.MFCC.kr(
            ...     pv_chain=pv_chain,
            ...     channel_count=13,
            ...     )
            >>> mfcc[0].source.pv_chain
            FFT.kr()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]
