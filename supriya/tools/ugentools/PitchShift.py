# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class PitchShift(UGen):
    r'''Pitch shift unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> source = ugentools.SoundIn.ar()
        >>> ugentools.PitchShift.ar(
        ...     source=source,
        ...     )
        PitchShift.ar()

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'window_size',
        'pitch_ratio',
        'pitch_dispersion',
        'time_dispersion',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        pitch_dispersion=0.0,
        pitch_ratio=1.0,
        source=None,
        time_dispersion=0.0,
        window_size=0.2,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            pitch_dispersion=pitch_dispersion,
            pitch_ratio=pitch_ratio,
            source=source,
            time_dispersion=time_dispersion,
            window_size=window_size,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        pitch_dispersion=0.0,
        pitch_ratio=1.0,
        source=None,
        time_dispersion=0.0,
        window_size=0.2,
        ):
        r'''Creates an audio-rate pitch shifter.

        ::

            >>> from supriya.tools import ugentools
            >>> source = ugentools.SoundIn.ar(bus=0)
            >>> ugentools.PitchShift.ar(
            ...     pitch_dispersion=0.0,
            ...     pitch_ratio=1.0,
            ...     source=source,
            ...     time_dispersion=0.0,
            ...     window_size=0.2,
            ...     )
            PitchShift.ar()

        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            pitch_dispersion=pitch_dispersion,
            pitch_ratio=pitch_ratio,
            source=source,
            time_dispersion=time_dispersion,
            window_size=window_size,
            )
        return ugen
