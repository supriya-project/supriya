# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class Pitch(MultiOutUGen):
    r'''

    ::

        >>> pitch = ugentools.Pitch.(
        ...     amp_threshold=0.01,
        ...     clar=0,
        ...     down_sample=1,
        ...     exec_frequency=100,
        ...     init_frequency=440,
        ...     max_bins_per_octave=16,
        ...     max_frequency=4000,
        ...     median=1,
        ...     min_frequency=60,
        ...     peak_threshold=0.5,
        ...     source=None,
        ...     )
        >>> pitch

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'init_frequency',
        'min_frequency',
        'max_frequency',
        'exec_frequency',
        'max_bins_per_octave',
        'median',
        'amp_threshold',
        'peak_threshold',
        'down_sample',
        'clar',
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
        source=None,
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
        source=None,
        ):
        r'''Constructs a control-rate Pitch.

        ::

            >>> pitch = ugentools.Pitch.kr(
            ...     amp_threshold=0.01,
            ...     clar=0,
            ...     down_sample=1,
            ...     exec_frequency=100,
            ...     init_frequency=440,
            ...     max_bins_per_octave=16,
            ...     max_frequency=4000,
            ...     median=1,
            ...     min_frequency=60,
            ...     peak_threshold=0.5,
            ...     source=None,
            ...     )
            >>> pitch

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
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

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        r'''Gets `source` input of Pitch.

        ::

            >>> pitch = ugentools.Pitch.ar(
            ...     amp_threshold=0.01,
            ...     clar=0,
            ...     down_sample=1,
            ...     exec_frequency=100,
            ...     init_frequency=440,
            ...     max_bins_per_octave=16,
            ...     max_frequency=4000,
            ...     median=1,
            ...     min_frequency=60,
            ...     peak_threshold=0.5,
            ...     source=None,
            ...     )
            >>> pitch.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def init_frequency(self):
        r'''Gets `init_frequency` input of Pitch.

        ::

            >>> pitch = ugentools.Pitch.ar(
            ...     amp_threshold=0.01,
            ...     clar=0,
            ...     down_sample=1,
            ...     exec_frequency=100,
            ...     init_frequency=440,
            ...     max_bins_per_octave=16,
            ...     max_frequency=4000,
            ...     median=1,
            ...     min_frequency=60,
            ...     peak_threshold=0.5,
            ...     source=None,
            ...     )
            >>> pitch.init_frequency

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('init_frequency')
        return self._inputs[index]

    @property
    def min_frequency(self):
        r'''Gets `min_frequency` input of Pitch.

        ::

            >>> pitch = ugentools.Pitch.ar(
            ...     amp_threshold=0.01,
            ...     clar=0,
            ...     down_sample=1,
            ...     exec_frequency=100,
            ...     init_frequency=440,
            ...     max_bins_per_octave=16,
            ...     max_frequency=4000,
            ...     median=1,
            ...     min_frequency=60,
            ...     peak_threshold=0.5,
            ...     source=None,
            ...     )
            >>> pitch.min_frequency

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('min_frequency')
        return self._inputs[index]

    @property
    def max_frequency(self):
        r'''Gets `max_frequency` input of Pitch.

        ::

            >>> pitch = ugentools.Pitch.ar(
            ...     amp_threshold=0.01,
            ...     clar=0,
            ...     down_sample=1,
            ...     exec_frequency=100,
            ...     init_frequency=440,
            ...     max_bins_per_octave=16,
            ...     max_frequency=4000,
            ...     median=1,
            ...     min_frequency=60,
            ...     peak_threshold=0.5,
            ...     source=None,
            ...     )
            >>> pitch.max_frequency

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('max_frequency')
        return self._inputs[index]

    @property
    def exec_frequency(self):
        r'''Gets `exec_frequency` input of Pitch.

        ::

            >>> pitch = ugentools.Pitch.ar(
            ...     amp_threshold=0.01,
            ...     clar=0,
            ...     down_sample=1,
            ...     exec_frequency=100,
            ...     init_frequency=440,
            ...     max_bins_per_octave=16,
            ...     max_frequency=4000,
            ...     median=1,
            ...     min_frequency=60,
            ...     peak_threshold=0.5,
            ...     source=None,
            ...     )
            >>> pitch.exec_frequency

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('exec_frequency')
        return self._inputs[index]

    @property
    def max_bins_per_octave(self):
        r'''Gets `max_bins_per_octave` input of Pitch.

        ::

            >>> pitch = ugentools.Pitch.ar(
            ...     amp_threshold=0.01,
            ...     clar=0,
            ...     down_sample=1,
            ...     exec_frequency=100,
            ...     init_frequency=440,
            ...     max_bins_per_octave=16,
            ...     max_frequency=4000,
            ...     median=1,
            ...     min_frequency=60,
            ...     peak_threshold=0.5,
            ...     source=None,
            ...     )
            >>> pitch.max_bins_per_octave

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('max_bins_per_octave')
        return self._inputs[index]

    @property
    def median(self):
        r'''Gets `median` input of Pitch.

        ::

            >>> pitch = ugentools.Pitch.ar(
            ...     amp_threshold=0.01,
            ...     clar=0,
            ...     down_sample=1,
            ...     exec_frequency=100,
            ...     init_frequency=440,
            ...     max_bins_per_octave=16,
            ...     max_frequency=4000,
            ...     median=1,
            ...     min_frequency=60,
            ...     peak_threshold=0.5,
            ...     source=None,
            ...     )
            >>> pitch.median

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('median')
        return self._inputs[index]

    @property
    def amp_threshold(self):
        r'''Gets `amp_threshold` input of Pitch.

        ::

            >>> pitch = ugentools.Pitch.ar(
            ...     amp_threshold=0.01,
            ...     clar=0,
            ...     down_sample=1,
            ...     exec_frequency=100,
            ...     init_frequency=440,
            ...     max_bins_per_octave=16,
            ...     max_frequency=4000,
            ...     median=1,
            ...     min_frequency=60,
            ...     peak_threshold=0.5,
            ...     source=None,
            ...     )
            >>> pitch.amp_threshold

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('amp_threshold')
        return self._inputs[index]

    @property
    def peak_threshold(self):
        r'''Gets `peak_threshold` input of Pitch.

        ::

            >>> pitch = ugentools.Pitch.ar(
            ...     amp_threshold=0.01,
            ...     clar=0,
            ...     down_sample=1,
            ...     exec_frequency=100,
            ...     init_frequency=440,
            ...     max_bins_per_octave=16,
            ...     max_frequency=4000,
            ...     median=1,
            ...     min_frequency=60,
            ...     peak_threshold=0.5,
            ...     source=None,
            ...     )
            >>> pitch.peak_threshold

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('peak_threshold')
        return self._inputs[index]

    @property
    def down_sample(self):
        r'''Gets `down_sample` input of Pitch.

        ::

            >>> pitch = ugentools.Pitch.ar(
            ...     amp_threshold=0.01,
            ...     clar=0,
            ...     down_sample=1,
            ...     exec_frequency=100,
            ...     init_frequency=440,
            ...     max_bins_per_octave=16,
            ...     max_frequency=4000,
            ...     median=1,
            ...     min_frequency=60,
            ...     peak_threshold=0.5,
            ...     source=None,
            ...     )
            >>> pitch.down_sample

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('down_sample')
        return self._inputs[index]

    @property
    def clar(self):
        r'''Gets `clar` input of Pitch.

        ::

            >>> pitch = ugentools.Pitch.ar(
            ...     amp_threshold=0.01,
            ...     clar=0,
            ...     down_sample=1,
            ...     exec_frequency=100,
            ...     init_frequency=440,
            ...     max_bins_per_octave=16,
            ...     max_frequency=4000,
            ...     median=1,
            ...     min_frequency=60,
            ...     peak_threshold=0.5,
            ...     source=None,
            ...     )
            >>> pitch.clar

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('clar')
        return self._inputs[index]