# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class BeatTrack2(MultiOutUGen):

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
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
        busindex=None,
        lock=0,
        numfeatures=None,
        phaseaccuracy=0.02,
        weightingscheme=None,
        windowsize=2,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
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
