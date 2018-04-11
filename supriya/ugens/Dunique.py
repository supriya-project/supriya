from supriya.ugens.DUGen import DUGen


class Dunique(DUGen):
    """
    Returns the same unique series of values for several demand streams.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> dunique = supriya.ugens.Dunique(
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

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> dunique = supriya.ugens.Dunique.new(
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

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> dunique = supriya.ugens.Dunique(
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

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> dunique = supriya.ugens.Dunique(
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

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> dunique = supriya.ugens.Dunique(
            ...     max_buffer_size=1024,
            ...     protected=True,
            ...     source=source,
            ...     )
            >>> dunique.source
            In.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
