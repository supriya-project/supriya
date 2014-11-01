# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class BinaryOpUGen(UGen):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Basic Operator UGens'

    __slots__ = ()

    _ordered_input_names = (
        'left',
        'right',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        left=None,
        right=None,
        rate=None,
        special_index=None,
        ):
        UGen.__init__(
            self,
            rate=rate,
            left=left,
            right=right,
            special_index=special_index,
            )

    ### PRIVATE METHODS ###

    @classmethod
    def _new_single(
        cls,
        rate=None,
        special_index=None,
        **kwargs
        ):
        from supriya.tools import synthdeftools
        a = kwargs['left']
        b = kwargs['right']
        if special_index == synthdeftools.BinaryOperator.MULTIPLICATION:
            if a == 0:
                return 0
            if b == 0:
                return 0
            if a == 1:
                return b
            if a == 1:
                return -b
            if b == 1:
                return a
            if b == -1:
                return -a
        if special_index == synthdeftools.BinaryOperator.ADDITION:
            if a == 0:
                return b
            if b == 0:
                return a
        if special_index == synthdeftools.BinaryOperator.SUBTRACTION:
            if a == 0:
                return -b
            if b == 0:
                return a
        if special_index == synthdeftools.BinaryOperator.FLOAT_DIVISION:
            if b == 1:
                return a
            if b == -1:
                return -a
        ugen = cls(
            rate=rate,
            special_index=special_index,
            left=a,
            right=b,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def left(self):
        r'''Gets `left` input of BinaryOpUGen.

        ::

            >>> left = ugentools.SinOsc.ar()
            >>> right = ugentools.WhiteNoise.kr()
            >>> binary_op_ugen = left * right
            >>> binary_op_ugen.left
            OutputProxy(
                source=SinOsc(
                    rate=<Rate.AUDIO: 2>,
                    frequency=440.0,
                    phase=0.0
                    ),
                output_index=0
                )

        Returns input.
        '''
        index = self._ordered_input_names.index('left')
        return self._inputs[index]

    @property
    def operator(self):
        r'''Gets operator of BinaryOpUgen.

        ::

            >>> left = ugentools.SinOsc.ar()
            >>> right = ugentools.WhiteNoise.kr()
            >>> binary_op_ugen = left / right
            >>> binary_op_ugen.operator
            <BinaryOperator.FLOAT_DIVISION: 4>

        Returns binary operator.
        '''
        from supriya.tools import synthdeftools
        return synthdeftools.BinaryOperator(self.special_index)

    @property
    def right(self):
        r'''Gets `right` input of BinaryOpUGen.

        ::

            >>> left = ugentools.SinOsc.ar()
            >>> right = ugentools.WhiteNoise.kr()
            >>> binary_op_ugen = left * right
            >>> binary_op_ugen.right
            OutputProxy(
                source=WhiteNoise(
                    rate=<Rate.CONTROL: 1>
                    ),
                output_index=0
                )

        Returns input.
        '''
        index = self._ordered_input_names.index('right')
        return self._inputs[index]