# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class UnaryOpUGen(UGen):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Basic Operator UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        rate=None,
        source=None,
        special_index=None,
        ):
        UGen.__init__(
            self,
            rate=rate,
            source=source,
            special_index=special_index,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        r'''Gets `source` input of UnaryOpUGen.

        ::

            >>> source = None
            >>> unary_op_ugen = ugentools.UnaryOpUGen.ar(
            ...     source=source,
            ...     )
            >>> unary_op_ugen.source

        Returns input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]