# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class UnaryOpUGen(UGen):
    r'''A unary operator ugen, created by applying a unary operator to a ugen.

    ::

        >>> ugen = ugentools.SinOsc.ar()
        >>> unary_op_ugen = abs(ugen)
        >>> unary_op_ugen
        UnaryOpUGen.ar()

    ::

        >>> unary_op_ugen.operator
        <UnaryOperator.ABSOLUTE_VALUE: 5>

    '''

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
    def operator(self):
        r'''Gets operator of UnaryOpUgen.

        ::

            >>> source = ugentools.SinOsc.ar()
            >>> unary_op_ugen = -source
            >>> unary_op_ugen.operator
            <UnaryOperator.NEGATIVE: 0>

        Returns unary operator.
        '''
        from supriya.tools import synthdeftools
        return synthdeftools.UnaryOperator(self.special_index)

    @property
    def source(self):
        r'''Gets `source` input of UnaryOpUGen.

        ::

            >>> source = ugentools.SinOsc.ar()
            >>> unary_op_ugen = -source
            >>> unary_op_ugen.source
            OutputProxy(
                source=SinOsc(
                    rate=<CalculationRate.AUDIO: 2>,
                    frequency=440.0,
                    phase=0.0
                    ),
                output_index=0
                )

        Returns input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]