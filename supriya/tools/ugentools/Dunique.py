# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DUGen import DUGen


class Dunique(DUGen):
    """
    Returns the same unique series of values for several demand streams.

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> dunique = ugentools.Dunique(
        ...     max_buffer_size=1024,
        ...     protected=True,
        ...     source=source,
        ...     )
        >>> dunique
        Dunique()

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'max_buffer_size',
        'protected',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        max_buffer_size=1024,
        protected=True,
        source=None,
        ):
        DUGen.__init__(
            self,
            max_buffer_size=max_buffer_size,
            protected=protected,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        max_buffer_size=1024,
        protected=True,
        source=None,
        ):
        """
        Constructs a Dunique.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> dunique = ugentools.Dunique.new(
            ...     max_buffer_size=1024,
            ...     protected=True,
            ...     source=source,
            ...     )
            >>> dunique
            Dunique()

        Returns ugen graph.
        """
        ugen = cls._new_expanded(
            max_buffer_size=max_buffer_size,
            protected=protected,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def max_buffer_size(self):
        """
        Gets `max_buffer_size` input of Dunique.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> dunique = ugentools.Dunique(
            ...     max_buffer_size=1024,
            ...     protected=True,
            ...     source=source,
            ...     )
            >>> dunique.max_buffer_size
            1024.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('max_buffer_size')
        return self._inputs[index]

    @property
    def protected(self):
        """
        Gets `protected` input of Dunique.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> dunique = ugentools.Dunique(
            ...     max_buffer_size=1024,
            ...     protected=True,
            ...     source=source,
            ...     )
            >>> dunique.protected
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('protected')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of Dunique.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> dunique = ugentools.Dunique(
            ...     max_buffer_size=1024,
            ...     protected=True,
            ...     source=source,
            ...     )
            >>> dunique.source
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
