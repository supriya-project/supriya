# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DUGen import DUGen


class Dreset(DUGen):
    r"""
    Resets demand-rate UGens.

    ::

        >>> source = ugentools.Dseries(start=0, step=2)
        >>> dreset = ugentools.Dreset(
        ...     reset=0,
        ...     source=source,
        ...     )
        >>> dreset
        Dreset()

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'reset',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        reset=0,
        source=None,
        ):
        DUGen.__init__(
            self,
            reset=reset,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        reset=0,
        source=None,
        ):
        r"""
        Constructs a Dreset.

        ::

            >>> source = ugentools.Dseries(start=0, step=2)
            >>> dreset = ugentools.Dreset.new(
            ...     reset=0,
            ...     source=source,
            ...     )
            >>> dreset
            Dreset()

        Returns ugen graph.
        """
        ugen = cls._new_expanded(
            reset=reset,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def reset(self):
        r"""
        Gets `reset` input of Dreset.

        ::

            >>> source = ugentools.Dseries(start=0, step=2)
            >>> dreset = ugentools.Dreset(
            ...     reset=0,
            ...     source=source,
            ...     )
            >>> dreset.reset
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('reset')
        return self._inputs[index]

    @property
    def source(self):
        r"""
        Gets `source` input of Dreset.

        ::

            >>> source = ugentools.Dseries(start=0, step=2)
            >>> dreset = ugentools.Dreset(
            ...     reset=0,
            ...     source=source,
            ...     )
            >>> dreset.source
            OutputProxy(
                source=Dseries(
                    length=inf,
                    start=0.0,
                    step=2.0
                    ),
                output_index=0
                )

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
