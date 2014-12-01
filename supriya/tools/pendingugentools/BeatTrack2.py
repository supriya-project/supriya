# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class BeatTrack2(MultiOutUGen):
    r'''

    ::

        >>> beat_track_2 = ugentools.BeatTrack2.ar(
        ...     busindex=busindex,
        ...     lock=0,
        ...     numfeatures=numfeatures,
        ...     phaseaccuracy=0.02,
        ...     weightingscheme=weightingscheme,
        ...     windowsize=2,
        ...     )
        >>> beat_track_2
        BeatTrack2.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'busindex',
        'numfeatures',
        'windowsize',
        'phaseaccuracy',
        'lock',
        'weightingscheme',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        busindex=None,
        lock=0,
        numfeatures=None,
        phaseaccuracy=0.02,
        weightingscheme=None,
        windowsize=2,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            busindex=busindex,
            lock=lock,
            numfeatures=numfeatures,
            phaseaccuracy=phaseaccuracy,
            weightingscheme=weightingscheme,
            windowsize=windowsize,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        busindex=busindex,
        lock=0,
        numfeatures=numfeatures,
        phaseaccuracy=0.02,
        weightingscheme=weightingscheme,
        windowsize=2,
        ):
        r'''Constructs a control-rate BeatTrack2.

        ::

            >>> beat_track_2 = ugentools.BeatTrack2.kr(
            ...     busindex=busindex,
            ...     lock=0,
            ...     numfeatures=numfeatures,
            ...     phaseaccuracy=0.02,
            ...     weightingscheme=weightingscheme,
            ...     windowsize=2,
            ...     )
            >>> beat_track_2
            BeatTrack2.kr()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            busindex=busindex,
            lock=lock,
            numfeatures=numfeatures,
            phaseaccuracy=phaseaccuracy,
            weightingscheme=weightingscheme,
            windowsize=windowsize,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def busindex(self):
        r'''Gets `busindex` input of BeatTrack2.

        ::

            >>> beat_track_2 = ugentools.BeatTrack2.ar(
            ...     busindex=busindex,
            ...     lock=0,
            ...     numfeatures=numfeatures,
            ...     phaseaccuracy=0.02,
            ...     weightingscheme=weightingscheme,
            ...     windowsize=2,
            ...     )
            >>> beat_track_2.busindex

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('busindex')
        return self._inputs[index]

    @property
    def lock(self):
        r'''Gets `lock` input of BeatTrack2.

        ::

            >>> beat_track_2 = ugentools.BeatTrack2.ar(
            ...     busindex=busindex,
            ...     lock=0,
            ...     numfeatures=numfeatures,
            ...     phaseaccuracy=0.02,
            ...     weightingscheme=weightingscheme,
            ...     windowsize=2,
            ...     )
            >>> beat_track_2.lock
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('lock')
        return self._inputs[index]

    @property
    def numfeatures(self):
        r'''Gets `numfeatures` input of BeatTrack2.

        ::

            >>> beat_track_2 = ugentools.BeatTrack2.ar(
            ...     busindex=busindex,
            ...     lock=0,
            ...     numfeatures=numfeatures,
            ...     phaseaccuracy=0.02,
            ...     weightingscheme=weightingscheme,
            ...     windowsize=2,
            ...     )
            >>> beat_track_2.numfeatures

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('numfeatures')
        return self._inputs[index]

    @property
    def phaseaccuracy(self):
        r'''Gets `phaseaccuracy` input of BeatTrack2.

        ::

            >>> beat_track_2 = ugentools.BeatTrack2.ar(
            ...     busindex=busindex,
            ...     lock=0,
            ...     numfeatures=numfeatures,
            ...     phaseaccuracy=0.02,
            ...     weightingscheme=weightingscheme,
            ...     windowsize=2,
            ...     )
            >>> beat_track_2.phaseaccuracy
            0.02

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('phaseaccuracy')
        return self._inputs[index]

    @property
    def weightingscheme(self):
        r'''Gets `weightingscheme` input of BeatTrack2.

        ::

            >>> beat_track_2 = ugentools.BeatTrack2.ar(
            ...     busindex=busindex,
            ...     lock=0,
            ...     numfeatures=numfeatures,
            ...     phaseaccuracy=0.02,
            ...     weightingscheme=weightingscheme,
            ...     windowsize=2,
            ...     )
            >>> beat_track_2.weightingscheme

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('weightingscheme')
        return self._inputs[index]

    @property
    def windowsize(self):
        r'''Gets `windowsize` input of BeatTrack2.

        ::

            >>> beat_track_2 = ugentools.BeatTrack2.ar(
            ...     busindex=busindex,
            ...     lock=0,
            ...     numfeatures=numfeatures,
            ...     phaseaccuracy=0.02,
            ...     weightingscheme=weightingscheme,
            ...     windowsize=2,
            ...     )
            >>> beat_track_2.windowsize
            2.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('windowsize')
        return self._inputs[index]