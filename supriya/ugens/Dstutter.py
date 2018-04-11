from supriya.ugens.DUGen import DUGen


class Dstutter(DUGen):
    """
    A demand-rate input replicator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> dstutter = supriya.ugens.Dstutter(
        ...     n=2,
        ...     source=source,
        ...     )
        >>> dstutter
        Dstutter()

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'n',
        'source',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        n=None,
        source=None,
        ):
        DUGen.__init__(
            self,
            n=n,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        n=None,
        source=None,
        ):
        """
        Constructs a Dstutter.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> dstutter = supriya.ugens.Dstutter.new(
            ...     n=2,
            ...     source=source,
            ...     )
            >>> dstutter
            Dstutter()

        Returns ugen graph.
        """
        ugen = cls._new_expanded(
            n=n,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def n(self):
        """
        Gets `n` input of Dstutter.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> dstutter = supriya.ugens.Dstutter(
            ...     n=2,
            ...     source=source,
            ...     )
            >>> dstutter.n
            2.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('n')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of Dstutter.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> dstutter = supriya.ugens.Dstutter(
            ...     n=2,
            ...     source=source,
            ...     )
            >>> dstutter.source
            In.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
