from supriya import CalculationRate
from supriya.ugens.MultiOutUGen import MultiOutUGen


class BeatTrack(MultiOutUGen):
    """
    Autocorrelation beat tracker.

    ::

        >>> source = supriya.ugens.SoundIn.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT(source=source)
        >>> beat_track = supriya.ugens.BeatTrack.kr(
        ...     pv_chain=pv_chain,
        ...     lock=0,
        ...     )
        >>> beat_track
        UGenArray({4})

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Machine Listening UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        'lock',
        )

    _valid_calculation_rates = (
        CalculationRate.CONTROL,
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pv_chain=None,
        lock=0,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=CalculationRate.CONTROL,
            channel_count=4,
            lock=lock,
            pv_chain=pv_chain,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        pv_chain=None,
        lock=0,
        ):
        """
        Constructs a control-rate BeatTrack.

        ::

            >>> source = supriya.ugens.SoundIn.ar(bus=0)
            >>> pv_chain = supriya.ugens.FFT(source=source)
            >>> beat_track = supriya.ugens.BeatTrack.kr(
            ...     pv_chain=pv_chain,
            ...     lock=0,
            ...     )
            >>> beat_track
            UGenArray({4})

        Returns ugen graph.
        """
        ugen = cls._new_expanded(
            pv_chain=pv_chain,
            lock=lock,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        """
        Gets `pv_chain` input of BeatTrack.

        ::

            >>> source = supriya.ugens.SoundIn.ar(bus=0)
            >>> pv_chain = supriya.ugens.FFT(source=source)
            >>> beat_track = supriya.ugens.BeatTrack.kr(
            ...     pv_chain=pv_chain,
            ...     lock=0,
            ...     )
            >>> beat_track[0].source.pv_chain
            FFT.kr()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]

    @property
    def lock(self):
        """
        Gets `lock` input of BeatTrack.

        ::

            >>> source = supriya.ugens.SoundIn.ar(bus=0)
            >>> pv_chain = supriya.ugens.FFT(source=source)
            >>> beat_track = supriya.ugens.BeatTrack.kr(
            ...     pv_chain=pv_chain,
            ...     lock=0,
            ...     )
            >>> beat_track[0].source.lock
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('lock')
        return self._inputs[index]
