from supriya.tools.synthdeftools.CalculationRate import CalculationRate
from supriya.tools.ugentools.UGen import UGen


class KeyTrack(UGen):
    """
    A key tracker.

    ::

        >>> source = ugentools.SoundIn.ar(bus=0)
        >>> pv_chain = ugentools.FFT(source=source)
        >>> key_track = ugentools.KeyTrack.kr(
        ...     pv_chain=pv_chain,
        ...     chroma_leak=0.5,
        ...     key_decay=2,
        ...     )
        >>> key_track
        KeyTrack.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Machine Listening UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        'key_decay',
        'chroma_leak',
        )

    _valid_calculation_rates = (
        CalculationRate.CONTROL,
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pv_chain=None,
        chroma_leak=0.5,
        key_decay=2,
        ):
        UGen.__init__(
            self,
            calculation_rate=CalculationRate.CONTROL,
            pv_chain=pv_chain,
            chroma_leak=chroma_leak,
            key_decay=key_decay,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        pv_chain=None,
        chroma_leak=0.5,
        key_decay=2,
        ):
        """
        Constructs a control-rate KeyTrack.

        ::

            >>> source = ugentools.SoundIn.ar(bus=0)
            >>> pv_chain = ugentools.FFT(source=source)
            >>> key_track = ugentools.KeyTrack.kr(
            ...     pv_chain=pv_chain,
            ...     chroma_leak=0.5,
            ...     key_decay=2,
            ...     )
            >>> key_track
            KeyTrack.kr()

        Returns ugen graph.
        """
        ugen = cls._new_expanded(
            pv_chain=pv_chain,
            chroma_leak=chroma_leak,
            key_decay=key_decay,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        """
        Gets `pv_chain` input of KeyTrack.

        ::

            >>> source = ugentools.SoundIn.ar(bus=0)
            >>> pv_chain = ugentools.FFT(source=source)
            >>> key_track = ugentools.KeyTrack.kr(
            ...     pv_chain=pv_chain,
            ...     chroma_leak=0.5,
            ...     key_decay=2,
            ...     )
            >>> key_track.pv_chain
            FFT.kr()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]

    @property
    def chroma_leak(self):
        """
        Gets `chroma_leak` input of KeyTrack.

        ::

            >>> source = ugentools.SoundIn.ar(bus=0)
            >>> pv_chain = ugentools.FFT(source=source)
            >>> key_track = ugentools.KeyTrack.kr(
            ...     pv_chain=pv_chain,
            ...     chroma_leak=0.5,
            ...     key_decay=2,
            ...     )
            >>> key_track.chroma_leak
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('chroma_leak')
        return self._inputs[index]

    @property
    def key_decay(self):
        """
        Gets `key_decay` input of KeyTrack.

        ::

            >>> source = ugentools.SoundIn.ar(bus=0)
            >>> pv_chain = ugentools.FFT(source=source)
            >>> key_track = ugentools.KeyTrack.kr(
            ...     pv_chain=pv_chain,
            ...     chroma_leak=0.5,
            ...     key_decay=2,
            ...     )
            >>> key_track.key_decay
            2.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('key_decay')
        return self._inputs[index]
