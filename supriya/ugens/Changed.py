from supriya.ugens.PseudoUGen import PseudoUGen


class Changed(PseudoUGen):
    """
    Triggers when a value changes.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> changed = supriya.ugens.Changed.ar(
        ...     source=source,
        ...     threshold=0,
        ...     )
        >>> supriya.graph(changed)  # doctest: +SKIP

    ::

        >>> print(changed)
        synthdef:
            name: 39e1f9d61589c4acaaf297cc961d65e4
            ugens:
            -   In.ar:
                    bus: 0.0
            -   HPZ1.ar:
                    source: In.ar[0]
            -   UnaryOpUGen(ABSOLUTE_VALUE).ar:
                    source: HPZ1.ar[0]
            -   BinaryOpUGen(GREATER_THAN).ar:
                    left: UnaryOpUGen(ABSOLUTE_VALUE).ar[0]
                    right: 0.0

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Filter UGens"

    ### PUBLIC METHODS ###

    @classmethod
    def ar(cls, source=None, threshold=0):
        """
        Constructs an audio-rate Changed.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> changed = supriya.ugens.Changed.ar(
            ...     source=source,
            ...     threshold=0,
            ...     )
            >>> supriya.graph(changed)  # doctest: +SKIP

        ::

            >>> print(changed)
            synthdef:
                name: 39e1f9d61589c4acaaf297cc961d65e4
                ugens:
                -   In.ar:
                        bus: 0.0
                -   HPZ1.ar:
                        source: In.ar[0]
                -   UnaryOpUGen(ABSOLUTE_VALUE).ar:
                        source: HPZ1.ar[0]
                -   BinaryOpUGen(GREATER_THAN).ar:
                        left: UnaryOpUGen(ABSOLUTE_VALUE).ar[0]
                        right: 0.0

        Returns ugen graph.
        """
        import supriya.ugens

        ugen = abs(supriya.ugens.HPZ1.ar(source=source)) > threshold
        return ugen

    @classmethod
    def kr(cls, source=None, threshold=0):
        """
        Constructs a control-rate Changed.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> changed = supriya.ugens.Changed.kr(
            ...     source=source,
            ...     threshold=0,
            ...     )
            >>> supriya.graph(changed)  # doctest: +SKIP

        ::

            >>> print(changed)
            synthdef:
                name: e2436271176995c6a0a5cac6d1553f8b
                ugens:
                -   In.ar:
                        bus: 0.0
                -   HPZ1.kr:
                        source: In.ar[0]
                -   UnaryOpUGen(ABSOLUTE_VALUE).kr:
                        source: HPZ1.kr[0]
                -   BinaryOpUGen(GREATER_THAN).kr:
                        left: UnaryOpUGen(ABSOLUTE_VALUE).kr[0]
                        right: 0.0

        Returns ugen graph.
        """
        import supriya.ugens

        ugen = abs(supriya.ugens.HPZ1.kr(source=source)) > threshold
        return ugen
