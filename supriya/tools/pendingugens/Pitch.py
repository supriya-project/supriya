# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class Pitch(MultiOutUGen):

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
        amp_threshold=0.01,
        clar=0,
        down_sample=1,
        exec_frequency=100,
        init_frequency=440,
        max_bins_per_octave=16,
        max_frequency=4000,
        median=1,
        min_frequency=60,
        peak_threshold=0.5,
        source=0,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            amp_threshold=amp_threshold,
            clar=clar,
            down_sample=down_sample,
            exec_frequency=exec_frequency,
            init_frequency=init_frequency,
            max_bins_per_octave=max_bins_per_octave,
            max_frequency=max_frequency,
            median=median,
            min_frequency=min_frequency,
            peak_threshold=peak_threshold,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        amp_threshold=0.01,
        clar=0,
        down_sample=1,
        exec_frequency=100,
        init_frequency=440,
        max_bins_per_octave=16,
        max_frequency=4000,
        median=1,
        min_frequency=60,
        peak_threshold=0.5,
        source=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            amp_threshold=amp_threshold,
            clar=clar,
            down_sample=down_sample,
            exec_frequency=exec_frequency,
            init_frequency=init_frequency,
            max_bins_per_octave=max_bins_per_octave,
            max_frequency=max_frequency,
            median=median,
            min_frequency=min_frequency,
            peak_threshold=peak_threshold,
            source=source,
            )
        return ugen
