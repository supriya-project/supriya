# -*- encoding: utf-8 -*-
import collections
from abjad.tools import sequencetools
from supriya.tools.synthdeftools.CalculationRate import CalculationRate
from supriya.tools.synthdeftools.UGen import UGen


class Klank(UGen):
    r'''A bank of resonators.

    ::

        >>> frequencies = [200, 671, 1153, 1723]
        >>> amplitudes = None
        >>> decay_times = [1, 1, 1, 1]
        >>> specifications = [frequencies, amplitudes, decay_times]
        >>> source = ugentools.BrownNoise.ar() * 0.001
        >>> klank = ugentools.Klank.ar(
        ...     decay_scale=1,
        ...     frequency_offset=0,
        ...     frequency_scale=1,
        ...     source=source,
        ...     specifications=specifications,
        ...     )
        >>> klank
        Klank.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'frequency_scale',
        'frequency_offset',
        'decay_scale',
        'specifications',
        )

    _unexpanded_input_names = (
        'specifications',
        )

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        decay_scale=1,
        frequency_offset=0,
        frequency_scale=1,
        source=None,
        specifications=None,
        ):
        frequencies, amplitudes, decay_times = specifications
        assert len(frequencies)
        if not amplitudes:
            amplitudes = [1.0] * len(frequencies)
        elif not isinstance(amplitudes, collections.Sequence):
            amplitudes = [amplitudes] * len(frequencies)
        if not decay_times:
            decay_times = [1.0] * len(frequencies)
        elif not isinstance(decay_times, collections.Sequence):
            decay_times = [decay_times] * len(frequencies)
        specifications = sequencetools.zip_sequences(
            [frequencies, amplitudes, decay_times])
        specifications = sequencetools.flatten_sequence(specifications)
        specifications = tuple(specifications)
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            decay_scale=decay_scale,
            frequency_offset=frequency_offset,
            frequency_scale=frequency_scale,
            source=source,
            specifications=specifications,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        decay_scale=1,
        frequency_offset=0,
        frequency_scale=1,
        source=None,
        specifications=None,
        ):
        r'''Constructs an audio-rate Klank.

        ::

            >>> klank = ugentools.Klank.ar(
            ...     decay_scale=1,
            ...     frequency_offset=0,
            ...     frequency_scale=1,
            ...     source=source,
            ...     specifications=specifications,
            ...     )
            >>> klank
            Klank.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            decay_scale=decay_scale,
            frequency_offset=frequency_offset,
            frequency_scale=frequency_scale,
            source=source,
            specifications=specifications,
            )
        return ugen

    # def new1(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def decay_scale(self):
        r'''Gets `decay_scale` source of Klank.

        ::

            >>> frequencies = [200, 671, 1153, 1723]
            >>> amplitudes = None
            >>> decay_times = [1, 1, 1, 1]
            >>> specifications = [frequencies, amplitudes, decay_times]
            >>> source = ugentools.BrownNoise.ar() * 0.001
            >>> klank = ugentools.Klank.ar(
            ...     decay_scale=1,
            ...     frequency_offset=0,
            ...     frequency_scale=1,
            ...     source=source,
            ...     specifications=specifications,
            ...     )
            >>> klank.decay_scale
            1.0

        Returns ugen source.
        '''
        index = self._ordered_input_names.index('decay_scale')
        return self._inputs[index]

    @property
    def frequency_offset(self):
        r'''Gets `frequency_offset` source of Klank.

        ::

            >>> frequencies = [200, 671, 1153, 1723]
            >>> amplitudes = None
            >>> decay_times = [1, 1, 1, 1]
            >>> specifications = [frequencies, amplitudes, decay_times]
            >>> source = ugentools.BrownNoise.ar() * 0.001
            >>> klank = ugentools.Klank.ar(
            ...     decay_scale=1,
            ...     frequency_offset=0,
            ...     frequency_scale=1,
            ...     source=source,
            ...     specifications=specifications,
            ...     )
            >>> klank.frequency_offset
            0.0

        Returns ugen source.
        '''
        index = self._ordered_input_names.index('frequency_offset')
        return self._inputs[index]

    @property
    def frequency_scale(self):
        r'''Gets `frequency_scale` source of Klank.

        ::

            >>> frequencies = [200, 671, 1153, 1723]
            >>> amplitudes = None
            >>> decay_times = [1, 1, 1, 1]
            >>> specifications = [frequencies, amplitudes, decay_times]
            >>> source = ugentools.BrownNoise.ar() * 0.001
            >>> klank = ugentools.Klank.ar(
            ...     decay_scale=1,
            ...     frequency_offset=0,
            ...     frequency_scale=1,
            ...     source=source,
            ...     specifications=specifications,
            ...     )
            >>> klank.frequency_scale
            1.0

        Returns ugen source.
        '''
        index = self._ordered_input_names.index('frequency_scale')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` source of Klank.

        ::

            >>> frequencies = [200, 671, 1153, 1723]
            >>> amplitudes = None
            >>> decay_times = [1, 1, 1, 1]
            >>> specifications = [frequencies, amplitudes, decay_times]
            >>> source = ugentools.BrownNoise.ar() * 0.001
            >>> klank = ugentools.Klank.ar(
            ...     decay_scale=1,
            ...     frequency_offset=0,
            ...     frequency_scale=1,
            ...     source=source,
            ...     specifications=specifications,
            ...     )
            >>> klank.source
            OutputProxy(
                source=BinaryOpUGen(
                    left=OutputProxy(
                        source=BrownNoise(
                            calculation_rate=<CalculationRate.AUDIO: 2>
                            ),
                        output_index=0
                        ),
                    right=0.001,
                    calculation_rate=<CalculationRate.AUDIO: 2>,
                    special_index=2
                    ),
                output_index=0
                )

        Returns ugen source.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def specifications(self):
        r'''Gets `specifications` source of Klank.

        ::

            >>> frequencies = [200, 671, 1153, 1723]
            >>> amplitudes = None
            >>> decay_times = [1, 1, 1, 1]
            >>> specifications = [frequencies, amplitudes, decay_times]
            >>> source = ugentools.BrownNoise.ar() * 0.001
            >>> klank = ugentools.Klank.ar(
            ...     decay_scale=1,
            ...     frequency_offset=0,
            ...     frequency_scale=1,
            ...     source=source,
            ...     specifications=specifications,
            ...     )
            >>> klank.specifications
            (200.0, 1.0, 1.0, 671.0, 1.0, 1.0, 1153.0, 1.0, 1.0, 1723.0, 1.0, 1.0)

        Returns ugen source.
        '''
        index = self._ordered_input_names.index('specifications')
        return tuple(self._inputs[index:])