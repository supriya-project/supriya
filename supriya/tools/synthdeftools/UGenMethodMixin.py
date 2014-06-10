# -*- encoding: utf-8 -*-
import collections
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class UGenMethodMixin(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        return UGenMethodMixin._compute_binary_op(self, expr, 'ADD')

    def __div__(self, expr):
        return UGenMethodMixin._compute_binary_op(self, expr, 'FDIV')

    def __mod__(self, expr):
        return UGenMethodMixin._compute_binary_op(self, expr, 'MOD')

    def __mul__(self, expr):
        return UGenMethodMixin._compute_binary_op(self, expr, 'MUL')

    def __neg__(self):
        return UGenMethodMixin._compute_unary_op(self, 'NEG')

    def __radd__(self, expr):
        return UGenMethodMixin._compute_binary_op(expr, self, 'ADD')

    def __rdiv__(self, expr):
        return UGenMethodMixin._compute_binary_op(expr, self, 'FDIV')

    def __rmul__(self, expr):
        return UGenMethodMixin._compute_binary_op(expr, self, 'MUL')

    def __rsub__(self, expr):
        return UGenMethodMixin._compute_binary_op(expr, self, 'SUB')

    def __sub__(self, expr):
        return UGenMethodMixin._compute_binary_op(self, expr, 'SUB')

    ### PRIVATE METHODS ###

    @staticmethod
    def _compute_binary_op(left, right, op_name):
        from supriya import synthdeftools
        result = []
        if not isinstance(left, collections.Sequence):
            left = [left]
        if not isinstance(right, collections.Sequence):
            right = [right]
        arguments = {'left': left, 'right': right}
        operator = synthdeftools.BinaryOperator[op_name]
        special_index = operator.value
        for expanded_arguments in UGenMethodMixin.expand_arguments(arguments):
            left = expanded_arguments['left']
            right = expanded_arguments['right']
            calculation_rate = UGenMethodMixin._compute_binary_rate(
                left, right)
            binary_op_ugen = synthdeftools.BinaryOpUGen(
                calculation_rate=calculation_rate,
                left=left,
                right=right,
                special_index=special_index,
                )
            result.append(binary_op_ugen)
        if len(result) == 1:
            return result[0]
        return synthdeftools.UGenArray(result)

    @staticmethod
    def _compute_binary_rate(ugen_a, ugen_b):
        from supriya import synthdeftools
        a_rate = synthdeftools.CalculationRate.SCALAR
        if isinstance(ugen_a, (synthdeftools.OutputProxy, synthdeftools.UGen)):
            a_rate = ugen_a.calculation_rate
        b_rate = synthdeftools.CalculationRate.SCALAR
        if isinstance(ugen_b, (synthdeftools.OutputProxy, synthdeftools.UGen)):
            b_rate = ugen_b.calculation_rate
        if a_rate == synthdeftools.CalculationRate.DEMAND \
            or a_rate == synthdeftools.CalculationRate.DEMAND:
            return synthdeftools.CalculationRate.DEMAND
        elif a_rate == synthdeftools.CalculationRate.AUDIO \
            or b_rate == synthdeftools.CalculationRate.AUDIO:
            return synthdeftools.CalculationRate.AUDIO
        elif a_rate == synthdeftools.CalculationRate.CONTROL \
            or b_rate == synthdeftools.CalculationRate.CONTROL:
            return synthdeftools.CalculationRate.CONTROL
        return synthdeftools.CalculationRate.SCALAR

    @staticmethod
    def _compute_unary_op(source, op_name):
        from supriya import synthdeftools
        result = []
        if not isinstance(source, collections.Sequence):
            source = [source]
        operator = synthdeftools.UnaryOperator[op_name]
        special_index = operator.value
        for single_source in source:
            unary_op_ugen = synthdeftools.UnaryOpUGen(
                calculation_rate=single_source.calculation_rate,
                source=single_source,
                special_index=special_index,
                )
            result.append(unary_op_ugen)
        if len(result) == 1:
            return result[0]
        return synthdeftools.UGenArray(result)

    ### PUBLIC METHODS ###

    @staticmethod
    def expand_arguments(arguments, unexpanded_argument_names=None):
        r'''Expands arguments into multichannel dictionaries.

        ::

            >>> import supriya
            >>> arguments = {'foo': 0, 'bar': (1, 2), 'baz': (3, 4, 5)}
            >>> result = supriya.synthdeftools.UGen.expand_arguments(arguments)
            >>> for x in result:
            ...     sorted(x.items())
            ...
            [('bar', 1), ('baz', 3), ('foo', 0)]
            [('bar', 2), ('baz', 4), ('foo', 0)]
            [('bar', 1), ('baz', 5), ('foo', 0)]

        ::

            >>> arguments = {'bus': (8, 9), 'source': (1, 2, 3)}
            >>> result = supriya.synthdeftools.UGen.expand_arguments(
            ...     arguments,
            ...     unexpanded_argument_names=('source',),
            ...     )
            >>> for x in result:
            ...     sorted(x.items())
            ...
            [('bus', 8), ('source', (1, 2, 3))]
            [('bus', 9), ('source', (1, 2, 3))]

        '''
        cached_unexpanded_arguments = {}
        if unexpanded_argument_names is not None:
            for argument_name in unexpanded_argument_names:
                if argument_name not in arguments:
                    continue
                cached_unexpanded_arguments[argument_name] = \
                    arguments[argument_name]
                del(arguments[argument_name])
        maximum_length = 1
        result = []
        for name, value in arguments.items():
            if isinstance(value, collections.Sequence):
                maximum_length = max(maximum_length, len(value))
        for i in range(maximum_length):
            result.append({})
            for name, value in arguments.items():
                if isinstance(value, collections.Sequence):
                    value = value[i % len(value)]
                    result[i][name] = value
                else:
                    result[i][name] = value
        for expanded_arguments in result:
            expanded_arguments.update(cached_unexpanded_arguments)
        return result
