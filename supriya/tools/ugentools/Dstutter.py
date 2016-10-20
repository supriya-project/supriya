# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DUGen import DUGen


class Dstutter(DUGen):
    """
    A demand-rate input replicator.

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> dstutter = ugentools.Dstutter(
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

            >>> source = ugentools.In.ar(bus=0)
            >>> dstutter = ugentools.Dstutter.new(
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

            >>> source = ugentools.In.ar(bus=0)
            >>> dstutter = ugentools.Dstutter(
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

            >>> source = ugentools.In.ar(bus=0)
            >>> dstutter = ugentools.Dstutter(
            ...     n=2,
            ...     source=source,
            ...     )
            >>> dstutter.source
            OutputProxy(
                source=In(
                    bus=0.0,
                    calculation_rate=CalculationRate.AUDIO,
                    channel_count=1
                    ),
                output_index=0
                )

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
