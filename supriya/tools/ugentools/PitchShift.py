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

    __documentation_section__ = 'Pitchshift UGens'

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
        rate=None,
        pitch_dispersion=0.0,
        pitch_ratio=1.0,
        source=None,
        time_dispersion=0.0,
        window_size=0.2,
        ):
        UGen.__init__(
            self,
            rate=rate,
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
        rate = synthdeftools.Rate.AUDIO
        ugen = cls._new_expanded(
            rate=rate,
            pitch_dispersion=pitch_dispersion,
            pitch_ratio=pitch_ratio,
            source=source,
            time_dispersion=time_dispersion,
            window_size=window_size,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pitch_dispersion(self):
        r'''Gets `pitch_dispersion` input of PitchShift.

        ::

            >>> pitch_dispersion = None
            >>> pitch_shift = ugentools.PitchShift.ar(
            ...     pitch_dispersion=pitch_dispersion,
            ...     )
            >>> pitch_shift.pitch_dispersion

        Returns input.
        '''
        index = self._ordered_input_names.index('pitch_dispersion')
        return self._inputs[index]

    @property
    def pitch_ratio(self):
        r'''Gets `pitch_ratio` input of PitchShift.

        ::

            >>> pitch_ratio = None
            >>> pitch_shift = ugentools.PitchShift.ar(
            ...     pitch_ratio=pitch_ratio,
            ...     )
            >>> pitch_shift.pitch_ratio

        Returns input.
        '''
        index = self._ordered_input_names.index('pitch_ratio')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of PitchShift.

        ::

            >>> source = None
            >>> pitch_shift = ugentools.PitchShift.ar(
            ...     source=source,
            ...     )
            >>> pitch_shift.source

        Returns input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def time_dispersion(self):
        r'''Gets `time_dispersion` input of PitchShift.

        ::

            >>> time_dispersion = None
            >>> pitch_shift = ugentools.PitchShift.ar(
            ...     time_dispersion=time_dispersion,
            ...     )
            >>> pitch_shift.time_dispersion

        Returns input.
        '''
        index = self._ordered_input_names.index('time_dispersion')
        return self._inputs[index]

    @property
    def window_size(self):
        r'''Gets `window_size` input of PitchShift.

        ::

            >>> window_size = None
            >>> pitch_shift = ugentools.PitchShift.ar(
            ...     window_size=window_size,
            ...     )
            >>> pitch_shift.window_size

        Returns input.
        '''
        index = self._ordered_input_names.index('window_size')
        return self._inputs[index]