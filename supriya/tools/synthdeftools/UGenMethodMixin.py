# -*- encoding: utf-8 -*-
import collections
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class UGenMethodMixin(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __abs__(self):
        return UGenMethodMixin._compute_unary_op(self, 'abs')

    def __add__(self, expr):
        return UGenMethodMixin._compute_binary_op(self, expr, 'add')

    def __div__(self, expr):
        return UGenMethodMixin._compute_binary_op(self, expr, 'fdiv')

    def __mod__(self, expr):
        return UGenMethodMixin._compute_binary_op(self, expr, 'mod')

    def __mul__(self, expr):
        return UGenMethodMixin._compute_binary_op(self, expr, 'mul')

    def __neg__(self):
        return UGenMethodMixin._compute_unary_op(self, 'neg')

    def __radd__(self, expr):
        return UGenMethodMixin._compute_binary_op(expr, self, 'add')

    def __rdiv__(self, expr):
        return UGenMethodMixin._compute_binary_op(expr, self, 'fdiv')

    def __rmul__(self, expr):
        return UGenMethodMixin._compute_binary_op(expr, self, 'mul')

    def __rsub__(self, expr):
        return UGenMethodMixin._compute_binary_op(expr, self, 'sub')

    def __sub__(self, expr):
        return UGenMethodMixin._compute_binary_op(self, expr, 'sub')

    ### PRIVATE METHODS ###

    @staticmethod
    def _compute_binary_op(left, right, operator):
        from supriya import synthdeftools
        from supriya import ugentools
        result = []
        if not isinstance(left, collections.Sequence):
            left = (left,)
        if not isinstance(right, collections.Sequence):
            right = (right,)
        dictionary = {'left': left, 'right': right}
        operator = synthdeftools.BinaryOperator.from_expr(operator)
        special_index = operator.value
        for expanded_dict in synthdeftools.UGen.expand_dictionary(dictionary):
            left = expanded_dict['left']
            right = expanded_dict['right']
            calculation_rate = UGenMethodMixin._compute_binary_rate(
                left, right)
            ugen = ugentools.BinaryOpUGen._new_single(
                calculation_rate=calculation_rate,
                left=left,
                right=right,
                special_index=special_index,
                )
            result.append(ugen)
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
    def _compute_unary_op(source, operator):
        from supriya import synthdeftools
        from supriya import ugentools
        result = []
        if not isinstance(source, collections.Sequence):
            source = (source,)
        operator = synthdeftools.UnaryOperator.from_expr(operator)
        special_index = operator.value
        for single_source in source:
            ugen = ugentools.UnaryOpUGen._new_single(
                calculation_rate=single_source.calculation_rate,
                source=single_source,
                special_index=special_index,
                )
            result.append(ugen)
        if len(result) == 1:
            return result[0]
        return synthdeftools.UGenArray(result)
