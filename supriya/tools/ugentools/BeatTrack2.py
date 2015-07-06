# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.CalculationRate import CalculationRate
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class BeatTrack2(MultiOutUGen):
    r'''A template-matching beat-tracker.

    ::

        >>> beat_track_2 = ugentools.BeatTrack2.kr(
        ...     bus_index=0,
        ...     lock=False,
        ...     feature_count=4,
        ...     phase_accuracy=0.02,
        ...     weighting_scheme=-2.1,
        ...     window_size=2,
        ...     )
        >>> beat_track_2
        UGenArray({6})

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Machine Listening UGens'

    __slots__ = ()

    _ordered_input_names = (
        'bus_index',
        'feature_count',
        'window_size',
        'phase_accuracy',
        'lock',
        'weighting_scheme',
        )

    _valid_calculation_rates = (
        CalculationRate.CONTROL,
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        bus_index=None,
        lock=0,
        feature_count=None,
        phase_accuracy=0.02,
        weighting_scheme=-2.1,
        window_size=2,
        ):
        MultiOutUGen.__init__(
            self,
            bus_index=bus_index,
            calculation_rate=calculation_rate,
            channel_count=6,
            feature_count=feature_count,
            lock=lock,
            phase_accuracy=phase_accuracy,
            weighting_scheme=weighting_scheme,
            window_size=window_size,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        bus_index=None,
        lock=False,
        feature_count=None,
        phase_accuracy=0.02,
        weighting_scheme=-2.1,
        window_size=2,
        ):
        r'''Constructs a control-rate BeatTrack2.

        ::

            >>> beat_track_2 = ugentools.BeatTrack2.kr(
            ...     bus_index=0,
            ...     lock=False,
            ...     feature_count=4,
            ...     phase_accuracy=0.02,
            ...     weighting_scheme=-2.1,
            ...     window_size=2,
            ...     )
            >>> beat_track_2
            UGenArray({6})

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bus_index=bus_index,
            lock=lock,
            feature_count=feature_count,
            phase_accuracy=phase_accuracy,
            weighting_scheme=weighting_scheme,
            window_size=window_size,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def bus_index(self):
        r'''Gets `bus_index` input of BeatTrack2.

        ::

            >>> beat_track_2 = ugentools.BeatTrack2.kr(
            ...     bus_index=0,
            ...     lock=False,
            ...     feature_count=4,
            ...     phase_accuracy=0.02,
            ...     weighting_scheme=-2.1,
            ...     window_size=2,
            ...     )
            >>> beat_track_2[0].source.bus_index
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('bus_index')
        return self._inputs[index]

    @property
    def lock(self):
        r'''Gets `lock` input of BeatTrack2.

        ::

            >>> beat_track_2 = ugentools.BeatTrack2.kr(
            ...     bus_index=0,
            ...     lock=False,
            ...     feature_count=4,
            ...     phase_accuracy=0.02,
            ...     weighting_scheme=-2.1,
            ...     window_size=2,
            ...     )
            >>> beat_track_2[0].source.lock
            False

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('lock')
        return bool(self._inputs[index])

    @property
    def feature_count(self):
        r'''Gets `feature_count` input of BeatTrack2.

        ::

            >>> beat_track_2 = ugentools.BeatTrack2.kr(
            ...     bus_index=0,
            ...     lock=False,
            ...     feature_count=4,
            ...     phase_accuracy=0.02,
            ...     weighting_scheme=-2.1,
            ...     window_size=2,
            ...     )
            >>> beat_track_2[0].source.feature_count
            4.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('feature_count')
        return self._inputs[index]

    @property
    def phase_accuracy(self):
        r'''Gets `phase_accuracy` input of BeatTrack2.

        ::

            >>> beat_track_2 = ugentools.BeatTrack2.kr(
            ...     bus_index=0,
            ...     lock=False,
            ...     feature_count=4,
            ...     phase_accuracy=0.02,
            ...     weighting_scheme=-2.1,
            ...     window_size=2,
            ...     )
            >>> beat_track_2[0].source.phase_accuracy
            0.02

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('phase_accuracy')
        return self._inputs[index]

    @property
    def weighting_scheme(self):
        r'''Gets `weighting_scheme` input of BeatTrack2.

        ::

            >>> beat_track_2 = ugentools.BeatTrack2.kr(
            ...     bus_index=0,
            ...     lock=False,
            ...     feature_count=4,
            ...     phase_accuracy=0.02,
            ...     weighting_scheme=-2.1,
            ...     window_size=2,
            ...     )
            >>> beat_track_2[0].source.weighting_scheme
            -2.1

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('weighting_scheme')
        return self._inputs[index]

    @property
    def window_size(self):
        r'''Gets `window_size` input of BeatTrack2.

        ::

            >>> beat_track_2 = ugentools.BeatTrack2.kr(
            ...     bus_index=0,
            ...     lock=False,
            ...     feature_count=4,
            ...     phase_accuracy=0.02,
            ...     weighting_scheme=-2.1,
            ...     window_size=2,
            ...     )
            >>> beat_track_2[0].source.window_size
            2.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('window_size')
        return self._inputs[index]