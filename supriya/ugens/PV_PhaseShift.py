from supriya.ugens.PV_ChainUGen import PV_ChainUGen


class PV_PhaseShift(PV_ChainUGen):
    """
    Shifts phase.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> shift = supriya.ugens.LFNoise2.kr(1).scale(-1, 1, -180, 180)
        >>> pv_phase_shift = supriya.ugens.PV_PhaseShift(
        ...     pv_chain=pv_chain,
        ...     integrate=0,
        ...     shift=shift,
        ...     )
        >>> pv_phase_shift
        PV_PhaseShift.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        'shift',
        'integrate',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pv_chain=None,
        integrate=0,
        shift=None,
        ):
        PV_ChainUGen.__init__(
            self,
            pv_chain=pv_chain,
            integrate=integrate,
            shift=shift,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        pv_chain=None,
        integrate=0,
        shift=None,
        ):
        """
        Constructs a PV_PhaseShift.

        ::

            >>> pv_chain = supriya.ugens.FFT(
            ...     source=supriya.ugens.WhiteNoise.ar(),
            ...     )
            >>> shift = supriya.ugens.LFNoise2.kr(1).scale(-1, 1, -180, 180)
            >>> pv_phase_shift = supriya.ugens.PV_PhaseShift.new(
            ...     pv_chain=pv_chain,
            ...     integrate=0,
            ...     shift=shift,
            ...     )
            >>> pv_phase_shift
            PV_PhaseShift.kr()

        Returns ugen graph.
        """
        ugen = cls._new_expanded(
            pv_chain=pv_chain,
            integrate=integrate,
            shift=shift,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        """
        Gets `pv_chain` input of PV_PhaseShift.

        ::

            >>> pv_chain = supriya.ugens.FFT(
            ...     source=supriya.ugens.WhiteNoise.ar(),
            ...     )
            >>> shift = supriya.ugens.LFNoise2.kr(1).scale(-1, 1, -180, 180)
            >>> pv_phase_shift = supriya.ugens.PV_PhaseShift(
            ...     pv_chain=pv_chain,
            ...     integrate=0,
            ...     shift=shift,
            ...     )
            >>> pv_phase_shift.pv_chain
            FFT.kr()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]

    @property
    def integrate(self):
        """
        Gets `integrate` input of PV_PhaseShift.

        ::

            >>> pv_chain = supriya.ugens.FFT(
            ...     source=supriya.ugens.WhiteNoise.ar(),
            ...     )
            >>> shift = supriya.ugens.LFNoise2.kr(1).scale(-1, 1, -180, 180)
            >>> pv_phase_shift = supriya.ugens.PV_PhaseShift(
            ...     pv_chain=pv_chain,
            ...     integrate=0,
            ...     shift=shift,
            ...     )
            >>> pv_phase_shift.integrate
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('integrate')
        return self._inputs[index]

    @property
    def shift(self):
        """
        Gets `shift` input of PV_PhaseShift.

        ::

            >>> pv_chain = supriya.ugens.FFT(
            ...     source=supriya.ugens.WhiteNoise.ar(),
            ...     )
            >>> shift = supriya.ugens.LFNoise2.kr(1).scale(-1, 1, -180, 180)
            >>> pv_phase_shift = supriya.ugens.PV_PhaseShift(
            ...     pv_chain=pv_chain,
            ...     integrate=0,
            ...     shift=shift,
            ...     )
            >>> pv_phase_shift.shift
            BinaryOpUGen.kr()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('shift')
        return self._inputs[index]
