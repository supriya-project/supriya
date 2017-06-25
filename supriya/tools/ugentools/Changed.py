from supriya.tools.ugentools.PseudoUGen import PseudoUGen


class Changed(PseudoUGen):
    """
    Triggers when a value changes.

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> changed = ugentools.Changed.ar(
        ...     source=source,
        ...     threshold=0,
        ...     )
        >>> print(str(changed))
        SynthDef 39e1f9d61589c4acaaf297cc961d65e4 {
            const_0:0.0 -> 0_In[0:bus]
            0_In[0] -> 1_HPZ1[0:source]
            1_HPZ1[0] -> 2_UnaryOpUGen:ABSOLUTE_VALUE[0:source]
            2_UnaryOpUGen:ABSOLUTE_VALUE[0] -> 3_BinaryOpUGen:GREATER_THAN[0:left]
            const_0:0.0 -> 3_BinaryOpUGen:GREATER_THAN[1:right]
        }

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

    __slots__ = ()

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        source=None,
        threshold=0,
        ):
        """
        Constructs an audio-rate Changed.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> changed = ugentools.Changed.ar(
            ...     source=source,
            ...     threshold=0,
            ...     )
            >>> print(str(changed))
            SynthDef 39e1f9d61589c4acaaf297cc961d65e4 {
                const_0:0.0 -> 0_In[0:bus]
                0_In[0] -> 1_HPZ1[0:source]
                1_HPZ1[0] -> 2_UnaryOpUGen:ABSOLUTE_VALUE[0:source]
                2_UnaryOpUGen:ABSOLUTE_VALUE[0] -> 3_BinaryOpUGen:GREATER_THAN[0:left]
                const_0:0.0 -> 3_BinaryOpUGen:GREATER_THAN[1:right]
            }

        Returns ugen graph.
        """
        from supriya.tools import ugentools
        ugen = abs(ugentools.HPZ1.ar(source=source)) > threshold
        return ugen

    # def coeffs(): ...

    @classmethod
    def kr(
        cls,
        source=None,
        threshold=0,
        ):
        """
        Constructs a control-rate Changed.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> changed = ugentools.Changed.kr(
            ...     source=source,
            ...     threshold=0,
            ...     )
            >>> print(str(changed))
            SynthDef e2436271176995c6a0a5cac6d1553f8b {
                const_0:0.0 -> 0_In[0:bus]
                0_In[0] -> 1_HPZ1[0:source]
                1_HPZ1[0] -> 2_UnaryOpUGen:ABSOLUTE_VALUE[0:source]
                2_UnaryOpUGen:ABSOLUTE_VALUE[0] -> 3_BinaryOpUGen:GREATER_THAN[0:left]
                const_0:0.0 -> 3_BinaryOpUGen:GREATER_THAN[1:right]
            }

        Returns ugen graph.
        """
        from supriya.tools import ugentools
        ugen = abs(ugentools.HPZ1.kr(source=source)) > threshold
        return ugen
