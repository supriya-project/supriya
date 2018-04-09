from supriya.tools.ugentools.DUGen import DUGen


class Dswitch(DUGen):
    """
    A demand-rate generator for embedding different inputs.

    ::

        >>> index = ugentools.Dseq(sequence=[0, 1, 2, 1, 0])
        >>> sequence = (1., 2., 3.)
        >>> dswitch = ugentools.Dswitch(
        ...     index=index,
        ...     sequence=sequence,
        ...     )
        >>> dswitch
        Dswitch()

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'index',
        'sequence',
        )

    _unexpanded_input_names = (
        'sequence',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        index=None,
        sequence=None,
        ):
        DUGen.__init__(
            self,
            index=index,
            sequence=sequence,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        index=None,
        sequence=None,
        ):
        """
        Constructs a Dswitch.

        ::

            >>> index = ugentools.Dseq(sequence=[0, 1, 2, 1, 0])
            >>> sequence = (1., 2., 3.)
            >>> dswitch = ugentools.Dswitch.new(
            ...     index=index,
            ...     sequence=sequence,
            ...     )
            >>> dswitch
            Dswitch()

        Returns ugen graph.
        """
        ugen = cls._new_expanded(
            index=index,
            sequence=sequence,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def index(self):
        """
        Gets `index` input of Dswitch.

        ::

            >>> index = ugentools.Dseq(sequence=[0, 1, 2, 1, 0])
            >>> sequence = (1., 2., 3.)
            >>> dswitch = ugentools.Dswitch(
            ...     index=index,
            ...     sequence=sequence,
            ...     )
            >>> dswitch.index
            Dseq()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('index')
        return self._inputs[index]

    @property
    def sequence(self):
        """
        Gets `sequence` input of Dswitch.

        ::

            >>> index = ugentools.Dseq(sequence=[0, 1, 2, 1, 0])
            >>> sequence = (1., 2., 3.)
            >>> dswitch = ugentools.Dswitch(
            ...     index=index,
            ...     sequence=sequence,
            ...     )
            >>> dswitch.sequence
            (1.0, 2.0, 3.0)

        Returns ugen input.
        """
        index = self._ordered_input_names.index('index') + 1
        return tuple(self._inputs[index:])
