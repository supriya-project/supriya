# -*- encoding: utf-8 -*-
from abjad.tools import sequencetools
from supriya.tools.ugentools.PseudoUGen import PseudoUGen


class Mix(PseudoUGen):
    """
    A down-to-mono signal mixer.

    ::

        >>> with synthdeftools.SynthDefBuilder() as builder:
        ...     oscillators = [ugentools.DC.ar(1) for _ in range(5)]
        ...     mix = ugentools.Mix.new(oscillators)
        ...
        >>> synthdef = builder.build(name='mix1')
        >>> print(synthdef)
        SynthDef mix1 {
            const_0:1.0 -> 0_DC[0:source]
            const_0:1.0 -> 1_DC[0:source]
            const_0:1.0 -> 2_DC[0:source]
            const_0:1.0 -> 3_DC[0:source]
            0_DC[0] -> 4_Sum4[0:input_one]
            1_DC[0] -> 4_Sum4[1:input_two]
            2_DC[0] -> 4_Sum4[2:input_three]
            3_DC[0] -> 4_Sum4[3:input_four]
            const_0:1.0 -> 5_DC[0:source]
            4_Sum4[0] -> 6_BinaryOpUGen:ADDITION[0:left]
            5_DC[0] -> 6_BinaryOpUGen:ADDITION[1:right]
        }

    ::

        >>> with synthdeftools.SynthDefBuilder() as builder:
        ...     oscillators = [ugentools.DC.ar(1) for _ in range(15)]
        ...     mix = ugentools.Mix.new(oscillators)
        ...
        >>> synthdef = builder.build('mix2')
        >>> print(synthdef)
        SynthDef mix2 {
            const_0:1.0 -> 0_DC[0:source]
            const_0:1.0 -> 1_DC[0:source]
            const_0:1.0 -> 2_DC[0:source]
            const_0:1.0 -> 3_DC[0:source]
            0_DC[0] -> 4_Sum4[0:input_one]
            1_DC[0] -> 4_Sum4[1:input_two]
            2_DC[0] -> 4_Sum4[2:input_three]
            3_DC[0] -> 4_Sum4[3:input_four]
            const_0:1.0 -> 5_DC[0:source]
            const_0:1.0 -> 6_DC[0:source]
            const_0:1.0 -> 7_DC[0:source]
            const_0:1.0 -> 8_DC[0:source]
            5_DC[0] -> 9_Sum4[0:input_one]
            6_DC[0] -> 9_Sum4[1:input_two]
            7_DC[0] -> 9_Sum4[2:input_three]
            8_DC[0] -> 9_Sum4[3:input_four]
            const_0:1.0 -> 10_DC[0:source]
            const_0:1.0 -> 11_DC[0:source]
            const_0:1.0 -> 12_DC[0:source]
            const_0:1.0 -> 13_DC[0:source]
            10_DC[0] -> 14_Sum4[0:input_one]
            11_DC[0] -> 14_Sum4[1:input_two]
            12_DC[0] -> 14_Sum4[2:input_three]
            13_DC[0] -> 14_Sum4[3:input_four]
            const_0:1.0 -> 15_DC[0:source]
            const_0:1.0 -> 16_DC[0:source]
            const_0:1.0 -> 17_DC[0:source]
            15_DC[0] -> 18_Sum3[0:input_one]
            16_DC[0] -> 18_Sum3[1:input_two]
            17_DC[0] -> 18_Sum3[2:input_three]
            4_Sum4[0] -> 19_Sum4[0:input_one]
            9_Sum4[0] -> 19_Sum4[1:input_two]
            14_Sum4[0] -> 19_Sum4[2:input_three]
            18_Sum3[0] -> 19_Sum4[3:input_four]
        }

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utility UGens'

    __slots__ = ()

    ### PUBLIC METHODS ###

    @staticmethod
    def new(sources):
        from supriya.tools import synthdeftools
        from supriya.tools import ugentools
        flattened_sources = []
        for source in sources:
            if isinstance(source, synthdeftools.UGenArray):
                flattened_sources.extend(source)
            else:
                flattened_sources.append(source)
        sources = synthdeftools.UGenArray(flattened_sources)
        summed_sources = []
        parts = sequencetools.partition_sequence_by_counts(
            sources,
            [4],
            cyclic=True,
            overhang=True,
            )
        for part in parts:
            if len(part) == 4:
                summed_sources.append(ugentools.Sum4(*part))
            elif len(part) == 3:
                summed_sources.append(ugentools.Sum3(*part))
            elif len(part) == 2:
                summed_sources.append(part[0] + part[1])
            else:
                summed_sources.append(part[0])
        if len(summed_sources) == 1:
            return summed_sources[0]
        return Mix.new(summed_sources) 
