# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_BinShift(PV_ChainUGen):
    r"""
    Shifts and stretches bin positions.

    ::

        >>> pv_chain = ugentools.FFT(
        ...     source=ugentools.WhiteNoise.ar(),
        ...     )
        >>> pv_bin_shift = ugentools.PV_BinShift(
        ...     pv_chain=pv_chain,
        ...     interpolate=0,
        ...     shift=0,
        ...     stretch=1,
        ...     )
        >>> pv_bin_shift
        PV_BinShift.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        'stretch',
        'shift',
        'interpolate',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pv_chain=None,
        interpolate=0,
        shift=0,
        stretch=1,
        ):
        PV_ChainUGen.__init__(
            self,
            pv_chain=pv_chain,
            interpolate=interpolate,
            shift=shift,
            stretch=stretch,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        pv_chain=None,
        interpolate=0,
        shift=0,
        stretch=1,
        ):
        r"""
        Constructs a PV_BinShift.

        ::

            >>> pv_chain = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_bin_shift = ugentools.PV_BinShift.new(
            ...     pv_chain=pv_chain,
            ...     interpolate=0,
            ...     shift=0,
            ...     stretch=1,
            ...     )
            >>> pv_bin_shift
            PV_BinShift.kr()

        Returns ugen graph.
        """
        ugen = cls._new_expanded(
            pv_chain=pv_chain,
            interpolate=interpolate,
            shift=shift,
            stretch=stretch,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        r"""
        Gets `pv_chain` input of PV_BinShift.

        ::

            >>> pv_chain = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_bin_shift = ugentools.PV_BinShift(
            ...     pv_chain=pv_chain,
            ...     interpolate=0,
            ...     shift=0,
            ...     stretch=1,
            ...     )
            >>> pv_bin_shift.pv_chain
            OutputProxy(
                source=FFT(
                    buffer_id=OutputProxy(
                        source=LocalBuf(
                            frame_count=2048.0,
                            channel_count=1.0,
                            calculation_rate=CalculationRate.SCALAR
                            ),
                        output_index=0
                        ),
                    source=OutputProxy(
                        source=WhiteNoise(
                            calculation_rate=CalculationRate.AUDIO
                            ),
                        output_index=0
                        ),
                    active=1.0,
                    hop=0.5,
                    window_size=0.0,
                    window_type=0.0
                    ),
                output_index=0
                )

        Returns ugen input.
        """
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]

    @property
    def interpolate(self):
        r"""
        Gets `interpolate` input of PV_BinShift.

        ::

            >>> pv_chain = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_bin_shift = ugentools.PV_BinShift(
            ...     pv_chain=pv_chain,
            ...     interpolate=0,
            ...     shift=0,
            ...     stretch=1,
            ...     )
            >>> pv_bin_shift.interpolate
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('interpolate')
        return self._inputs[index]

    @property
    def shift(self):
        r"""
        Gets `shift` input of PV_BinShift.

        ::

            >>> pv_chain = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_bin_shift = ugentools.PV_BinShift(
            ...     pv_chain=pv_chain,
            ...     interpolate=0,
            ...     shift=0,
            ...     stretch=1,
            ...     )
            >>> pv_bin_shift.shift
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('shift')
        return self._inputs[index]

    @property
    def stretch(self):
        r"""
        Gets `stretch` input of PV_BinShift.

        ::

            >>> pv_chain = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_bin_shift = ugentools.PV_BinShift(
            ...     pv_chain=pv_chain,
            ...     interpolate=0,
            ...     shift=0,
            ...     stretch=1,
            ...     )
            >>> pv_bin_shift.stretch
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('stretch')
        return self._inputs[index]
