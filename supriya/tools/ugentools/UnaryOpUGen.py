from supriya.tools.ugentools.PureUGen import PureUGen


class UnaryOpUGen(PureUGen):
    """
    A unary operator ugen, created by applying a unary operator to a ugen.

    ::

        >>> ugen = ugentools.SinOsc.ar()
        >>> unary_op_ugen = abs(ugen)
        >>> unary_op_ugen
        UnaryOpUGen.ar()

    ::

        >>> unary_op_ugen.operator
        UnaryOperator.ABSOLUTE_VALUE

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Basic Operator UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        source=None,
        special_index=None,
        ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            source=source,
            special_index=special_index,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def operator(self):
        """
        Gets operator of UnaryOpUgen.

        ::

            >>> source = ugentools.SinOsc.ar()
            >>> unary_op_ugen = -source
            >>> unary_op_ugen.operator
            UnaryOperator.NEGATIVE

        Returns unary operator.
        """
        from supriya.tools import synthdeftools
        return synthdeftools.UnaryOperator(self.special_index)

    @property
    def source(self):
        """
        Gets `source` input of UnaryOpUGen.

        ::

            >>> source = ugentools.SinOsc.ar()
            >>> unary_op_ugen = -source
            >>> unary_op_ugen.source
            SinOsc.ar()[0]

        Returns input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
