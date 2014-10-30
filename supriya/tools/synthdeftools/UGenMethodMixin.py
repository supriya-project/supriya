# -*- encoding: utf-8 -*-
import collections
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class UGenMethodMixin(SupriyaObject):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'SynthDef Internals'

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __abs__(self):
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_unary_op(
            self,
            synthdeftools.UnaryOperator.ABSOLUTE_VALUE,
            )

    def __add__(self, expr):
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            self,
            expr,
            synthdeftools.BinaryOperator.ADDITION,
            )

    def __div__(self, expr):
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            self,
            expr,
            synthdeftools.BinaryOperator.FLOAT_DIVISION,
            )

    def __mod__(self, expr):
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            self,
            expr,
            synthdeftools.BinaryOperator.MODULO,
            )

    def __mul__(self, expr):
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            self,
            expr,
            synthdeftools.BinaryOperator.MULTIPLICATION,
            )

    def __neg__(self):
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_unary_op(
            self,
            synthdeftools.UnaryOperator.NEGATIVE,
            )

    def __radd__(self, expr):
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            expr,
            self,
            synthdeftools.BinaryOperator.ADDITION,
            )

    def __rdiv__(self, expr):
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            expr,
            self,
            synthdeftools.BinaryOperator.FLOAT_DIVISION,
            )

    def __rmul__(self, expr):
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            expr,
            self,
            synthdeftools.BinaryOperator.MULTIPLICATION,
            )

    def __rsub__(self, expr):
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            expr,
            self,
            synthdeftools.BinaryOperator.SUBRACTION,
            )

    def __str__(self):
        from supriya.tools import synthdeftools
        builder = synthdeftools.SynthDefBuilder()
        builder.add_ugen(self)
        synthdef = builder.build()
        result = str(synthdef)
        return result

    def __sub__(self, expr):
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            self,
            expr,
            synthdeftools.BinaryOperator.SUBRACTION,
            )

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
            rate = UGenMethodMixin._compute_binary_rate(
                left, right)
            ugen = ugentools.BinaryOpUGen._new_single(
                rate=rate,
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

        a_rate = synthdeftools.Rate.from_input(ugen_a)
        #a_rate = synthdeftools.Rate.SCALAR
        #if isinstance(ugen_a, (synthdeftools.OutputProxy, synthdeftools.UGen)):
        #    a_rate = ugen_a.rate
        #elif isinstance(ugen_a, synthdeftools.Parameter):
        #    a_rate = synthdeftools.Rate.from_input(ugen_a)

        b_rate = synthdeftools.Rate.from_input(ugen_b)
        #b_rate = synthdeftools.Rate.SCALAR
        #if isinstance(ugen_b, (synthdeftools.OutputProxy, synthdeftools.UGen)):
        #    b_rate = ugen_b.rate
        #elif isinstance(ugen_b, synthdeftools.Parameter):
        #    b_rate = synthdeftools.Rate.from_input(ugen_b)

        if a_rate == synthdeftools.Rate.DEMAND \
            or a_rate == synthdeftools.Rate.DEMAND:
            return synthdeftools.Rate.DEMAND
        elif a_rate == synthdeftools.Rate.AUDIO \
            or b_rate == synthdeftools.Rate.AUDIO:
            return synthdeftools.Rate.AUDIO
        elif a_rate == synthdeftools.Rate.CONTROL \
            or b_rate == synthdeftools.Rate.CONTROL:
            return synthdeftools.Rate.CONTROL
        return synthdeftools.Rate.SCALAR

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
                rate=single_source.rate,
                source=single_source,
                special_index=special_index,
                )
            result.append(ugen)
        if len(result) == 1:
            return result[0]
        return synthdeftools.UGenArray(result)

    ### PUBLIC METHODS ###

    def lag(self, time_one=0.1, time_two=None):
        from supriya.tools import synthdeftools
        from supriya.tools import ugentools
        rate = synthdeftools.Rate.from_ugen_method_mixin(self)
        if time_two is None:
            result = ugentools.Lag._new_expanded(
                rate=rate,
                source=self,
                lag_time=time_one,
                )
        else:
            result = ugentools.LagUD._new_expanded(
                rate=rate,
                source=self,
                lag_time_up=time_one,
                lag_time_down=time_two,
                )
        return result