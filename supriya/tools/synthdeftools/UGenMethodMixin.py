# -*- encoding: utf-8 -*-
import collections
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class UGenMethodMixin(SupriyaObject):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'SynthDef Internals'

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __abs__(self):
        r'''Gets absolute value of ugen graph.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen = ugentools.WhiteNoise.ar()
                >>> result = abs(ugen)
                >>> result
                UnaryOpUGen.ar()

            ::

                >>> print(str(result))
                SynthDef ... {
                    0_WhiteNoise[0] -> 1_UnaryOpUGen:ABSOLUTE_VALUE[0:source]
                }

        ..  container:: example

            **Example 2:**

            ::

                >>> ugen_array = ugentools.SinOsc.ar(
                ...     frequency=(440, 442, 443),
                ...     )
                >>> result = abs(ugen_array)
                >>> result
                UGenArray({3})

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:440.0 -> 0_SinOsc[0:frequency]
                    const_1:0.0 -> 0_SinOsc[1:phase]
                    0_SinOsc[0] -> 1_UnaryOpUGen:ABSOLUTE_VALUE[0:source]
                    const_2:442.0 -> 2_SinOsc[0:frequency]
                    const_1:0.0 -> 2_SinOsc[1:phase]
                    2_SinOsc[0] -> 3_UnaryOpUGen:ABSOLUTE_VALUE[0:source]
                    const_3:443.0 -> 4_SinOsc[0:frequency]
                    const_1:0.0 -> 4_SinOsc[1:phase]
                    4_SinOsc[0] -> 5_UnaryOpUGen:ABSOLUTE_VALUE[0:source]
                }

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_unary_op(
            self,
            synthdeftools.UnaryOperator.ABSOLUTE_VALUE,
            )

    def __add__(self, expr):
        r'''Adds `expr` to ugen graph.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = ugentools.WhiteNoise.kr()
                >>> expr = ugentools.SinOsc.ar()
                >>> result = ugen_graph + expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:440.0 -> 1_SinOsc[0:frequency]
                    const_1:0.0 -> 1_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 2_BinaryOpUGen:ADDITION[0:left]
                    1_SinOsc[0] -> 2_BinaryOpUGen:ADDITION[1:right]
                }

        ..  container:: example

            **Example 2:**

            ::

                >>> ugen_graph = ugentools.WhiteNoise.kr()
                >>> expr = ugentools.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ...     )
                >>> result = ugen_graph + expr
                >>> result
                UGenArray({3})

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:440.0 -> 1_SinOsc[0:frequency]
                    const_1:0.0 -> 1_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 2_BinaryOpUGen:ADDITION[0:left]
                    1_SinOsc[0] -> 2_BinaryOpUGen:ADDITION[1:right]
                    const_2:442.0 -> 3_SinOsc[0:frequency]
                    const_1:0.0 -> 3_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 4_BinaryOpUGen:ADDITION[0:left]
                    3_SinOsc[0] -> 4_BinaryOpUGen:ADDITION[1:right]
                    const_3:443.0 -> 5_SinOsc[0:frequency]
                    const_1:0.0 -> 5_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 6_BinaryOpUGen:ADDITION[0:left]
                    5_SinOsc[0] -> 6_BinaryOpUGen:ADDITION[1:right]
                }

        ..  container:: example

            **Example 3:**

            ::

                >>> ugen_graph = ugentools.Dust.ar(
                ...     density=11.5,
                ...     )
                >>> expr = 4
                >>> result = ugen_graph + expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:11.5 -> 0_Dust[0:density]
                    0_Dust[0] -> 1_BinaryOpUGen:ADDITION[0:left]
                    const_1:4.0 -> 1_BinaryOpUGen:ADDITION[1:right]
                }

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            self,
            expr,
            synthdeftools.BinaryOperator.ADDITION,
            )

    def __div__(self, expr):
        r'''Divides ugen graph by `expr`.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = ugentools.WhiteNoise.kr()
                >>> expr = ugentools.SinOsc.ar()
                >>> result = ugen_graph / expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:440.0 -> 1_SinOsc[0:frequency]
                    const_1:0.0 -> 1_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 2_BinaryOpUGen:FLOAT_DIVISION[0:left]
                    1_SinOsc[0] -> 2_BinaryOpUGen:FLOAT_DIVISION[1:right]
                }

        ..  container:: example

            **Example 2:**

            ::

                >>> ugen_graph = ugentools.WhiteNoise.kr()
                >>> expr = ugentools.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ...     )
                >>> result = ugen_graph / expr
                >>> result
                UGenArray({3})

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:440.0 -> 1_SinOsc[0:frequency]
                    const_1:0.0 -> 1_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 2_BinaryOpUGen:FLOAT_DIVISION[0:left]
                    1_SinOsc[0] -> 2_BinaryOpUGen:FLOAT_DIVISION[1:right]
                    const_2:442.0 -> 3_SinOsc[0:frequency]
                    const_1:0.0 -> 3_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 4_BinaryOpUGen:FLOAT_DIVISION[0:left]
                    3_SinOsc[0] -> 4_BinaryOpUGen:FLOAT_DIVISION[1:right]
                    const_3:443.0 -> 5_SinOsc[0:frequency]
                    const_1:0.0 -> 5_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 6_BinaryOpUGen:FLOAT_DIVISION[0:left]
                    5_SinOsc[0] -> 6_BinaryOpUGen:FLOAT_DIVISION[1:right]
                }

        ..  container:: example

            **Example 3:**

            ::

                >>> ugen_graph = ugentools.Dust.ar(
                ...     density=11.5,
                ...     )
                >>> expr = 4
                >>> result = ugen_graph / expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:11.5 -> 0_Dust[0:density]
                    0_Dust[0] -> 1_BinaryOpUGen:FLOAT_DIVISION[0:left]
                    const_1:4.0 -> 1_BinaryOpUGen:FLOAT_DIVISION[1:right]
                }

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            self,
            expr,
            synthdeftools.BinaryOperator.FLOAT_DIVISION,
            )

    def __graph__(self):
        r'''Gets Graphviz representation of ugen graph.

        Returns GraphvizGraph instance.
        '''
        from supriya.tools import synthdeftools
        builder = synthdeftools.SynthDefBuilder()
        builder.add_ugen(self)
        synthdef = builder.build()
        result = synthdef.__graph__()
        return result

    def __mod__(self, expr):
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            self,
            expr,
            synthdeftools.BinaryOperator.MODULO,
            )

    def __mul__(self, expr):
        r'''Multiplies ugen graph by `expr`.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = ugentools.WhiteNoise.kr()
                >>> expr = ugentools.SinOsc.ar()
                >>> result = ugen_graph * expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:440.0 -> 1_SinOsc[0:frequency]
                    const_1:0.0 -> 1_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 2_BinaryOpUGen:MULTIPLICATION[0:left]
                    1_SinOsc[0] -> 2_BinaryOpUGen:MULTIPLICATION[1:right]
                }

        ..  container:: example

            **Example 2:**

            ::

                >>> ugen_graph = ugentools.WhiteNoise.kr()
                >>> expr = ugentools.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ...     )
                >>> result = ugen_graph * expr
                >>> result
                UGenArray({3})

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:440.0 -> 1_SinOsc[0:frequency]
                    const_1:0.0 -> 1_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 2_BinaryOpUGen:MULTIPLICATION[0:left]
                    1_SinOsc[0] -> 2_BinaryOpUGen:MULTIPLICATION[1:right]
                    const_2:442.0 -> 3_SinOsc[0:frequency]
                    const_1:0.0 -> 3_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 4_BinaryOpUGen:MULTIPLICATION[0:left]
                    3_SinOsc[0] -> 4_BinaryOpUGen:MULTIPLICATION[1:right]
                    const_3:443.0 -> 5_SinOsc[0:frequency]
                    const_1:0.0 -> 5_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 6_BinaryOpUGen:MULTIPLICATION[0:left]
                    5_SinOsc[0] -> 6_BinaryOpUGen:MULTIPLICATION[1:right]
                }

        ..  container:: example

            **Example 3:**

            ::

                >>> ugen_graph = ugentools.Dust.ar(
                ...     density=11.5,
                ...     )
                >>> expr = 4
                >>> result = ugen_graph * expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:11.5 -> 0_Dust[0:density]
                    0_Dust[0] -> 1_BinaryOpUGen:MULTIPLICATION[0:left]
                    const_1:4.0 -> 1_BinaryOpUGen:MULTIPLICATION[1:right]
                }

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            self,
            expr,
            synthdeftools.BinaryOperator.MULTIPLICATION,
            )

    def __neg__(self):
        r'''Negates ugen graph.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen = ugentools.WhiteNoise.ar()
                >>> result = -ugen
                >>> result
                UnaryOpUGen.ar()

            ::

                >>> print(str(result))
                SynthDef ... {
                    0_WhiteNoise[0] -> 1_UnaryOpUGen:NEGATIVE[0:source]
                }

        ..  container:: example

            **Example 2:**

            ::

                >>> ugen_array = ugentools.SinOsc.ar(
                ...     frequency=(440, 442, 443),
                ...     )
                >>> result = -ugen_array
                >>> result
                UGenArray({3})

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:440.0 -> 0_SinOsc[0:frequency]
                    const_1:0.0 -> 0_SinOsc[1:phase]
                    0_SinOsc[0] -> 1_UnaryOpUGen:NEGATIVE[0:source]
                    const_2:442.0 -> 2_SinOsc[0:frequency]
                    const_1:0.0 -> 2_SinOsc[1:phase]
                    2_SinOsc[0] -> 3_UnaryOpUGen:NEGATIVE[0:source]
                    const_3:443.0 -> 4_SinOsc[0:frequency]
                    const_1:0.0 -> 4_SinOsc[1:phase]
                    4_SinOsc[0] -> 5_UnaryOpUGen:NEGATIVE[0:source]
                }

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_unary_op(
            self,
            synthdeftools.UnaryOperator.NEGATIVE,
            )

    def __radd__(self, expr):
        r'''Adds ugen graph to `expr`.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = 1.5
                >>> expr = ugentools.SinOsc.ar()
                >>> result = ugen_graph + expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:440.0 -> 0_SinOsc[0:frequency]
                    const_1:0.0 -> 0_SinOsc[1:phase]
                    const_2:1.5 -> 1_BinaryOpUGen:ADDITION[0:left]
                    0_SinOsc[0] -> 1_BinaryOpUGen:ADDITION[1:right]
                }

        ..  container:: example

            **Example 2:**

            ::

                >>> ugen_graph = [220, 330]
                >>> expr = ugentools.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ...     )
                >>> result = ugen_graph + expr
                >>> result
                UGenArray({3})

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:440.0 -> 0_SinOsc[0:frequency]
                    const_1:0.0 -> 0_SinOsc[1:phase]
                    const_2:220.0 -> 1_BinaryOpUGen:ADDITION[0:left]
                    0_SinOsc[0] -> 1_BinaryOpUGen:ADDITION[1:right]
                    const_3:442.0 -> 2_SinOsc[0:frequency]
                    const_1:0.0 -> 2_SinOsc[1:phase]
                    const_4:330.0 -> 3_BinaryOpUGen:ADDITION[0:left]
                    2_SinOsc[0] -> 3_BinaryOpUGen:ADDITION[1:right]
                    const_5:443.0 -> 4_SinOsc[0:frequency]
                    const_1:0.0 -> 4_SinOsc[1:phase]
                    const_2:220.0 -> 5_BinaryOpUGen:ADDITION[0:left]
                    4_SinOsc[0] -> 5_BinaryOpUGen:ADDITION[1:right]
                }

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            expr,
            self,
            synthdeftools.BinaryOperator.ADDITION,
            )

    def __rdiv__(self, expr):
        r'''Divides `expr` by ugen graph.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = 1.5
                >>> expr = ugentools.SinOsc.ar()
                >>> result = ugen_graph / expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:440.0 -> 0_SinOsc[0:frequency]
                    const_1:0.0 -> 0_SinOsc[1:phase]
                    const_2:1.5 -> 1_BinaryOpUGen:FLOAT_DIVISION[0:left]
                    0_SinOsc[0] -> 1_BinaryOpUGen:FLOAT_DIVISION[1:right]
                }

        ..  container:: example

            **Example 2:**

            ::

                >>> ugen_graph = [220, 330]
                >>> expr = ugentools.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ...     )
                >>> result = ugen_graph / expr
                >>> result
                UGenArray({3})

            ::

                >>> print(str(result))
                SynthDef d71b3081490f800d5136c87f5fef46d1 {
                    const_0:440.0 -> 0_SinOsc[0:frequency]
                    const_1:0.0 -> 0_SinOsc[1:phase]
                    const_2:220.0 -> 1_BinaryOpUGen:FLOAT_DIVISION[0:left]
                    0_SinOsc[0] -> 1_BinaryOpUGen:FLOAT_DIVISION[1:right]
                    const_3:442.0 -> 2_SinOsc[0:frequency]
                    const_1:0.0 -> 2_SinOsc[1:phase]
                    const_4:330.0 -> 3_BinaryOpUGen:FLOAT_DIVISION[0:left]
                    2_SinOsc[0] -> 3_BinaryOpUGen:FLOAT_DIVISION[1:right]
                    const_5:443.0 -> 4_SinOsc[0:frequency]
                    const_1:0.0 -> 4_SinOsc[1:phase]
                    const_2:220.0 -> 5_BinaryOpUGen:FLOAT_DIVISION[0:left]
                    4_SinOsc[0] -> 5_BinaryOpUGen:FLOAT_DIVISION[1:right]
                }

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            expr,
            self,
            synthdeftools.BinaryOperator.FLOAT_DIVISION,
            )

    def __rmul__(self, expr):
        r'''Multiplies `expr` by ugen graph.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = 1.5
                >>> expr = ugentools.SinOsc.ar()
                >>> result = ugen_graph * expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:440.0 -> 0_SinOsc[0:frequency]
                    const_1:0.0 -> 0_SinOsc[1:phase]
                    const_2:1.5 -> 1_BinaryOpUGen:MULTIPLICATION[0:left]
                    0_SinOsc[0] -> 1_BinaryOpUGen:MULTIPLICATION[1:right]
                }

        ..  container:: example

            **Example 2:**

            ::

                >>> ugen_graph = [220, 330]
                >>> expr = ugentools.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ...     )
                >>> result = ugen_graph * expr
                >>> result
                UGenArray({3})

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:440.0 -> 0_SinOsc[0:frequency]
                    const_1:0.0 -> 0_SinOsc[1:phase]
                    const_2:220.0 -> 1_BinaryOpUGen:MULTIPLICATION[0:left]
                    0_SinOsc[0] -> 1_BinaryOpUGen:MULTIPLICATION[1:right]
                    const_3:442.0 -> 2_SinOsc[0:frequency]
                    const_1:0.0 -> 2_SinOsc[1:phase]
                    const_4:330.0 -> 3_BinaryOpUGen:MULTIPLICATION[0:left]
                    2_SinOsc[0] -> 3_BinaryOpUGen:MULTIPLICATION[1:right]
                    const_5:443.0 -> 4_SinOsc[0:frequency]
                    const_1:0.0 -> 4_SinOsc[1:phase]
                    const_2:220.0 -> 5_BinaryOpUGen:MULTIPLICATION[0:left]
                    4_SinOsc[0] -> 5_BinaryOpUGen:MULTIPLICATION[1:right]
                }

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            expr,
            self,
            synthdeftools.BinaryOperator.MULTIPLICATION,
            )

    def __rsub__(self, expr):
        r'''Subtracts ugen graph from `expr`.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = 1.5
                >>> expr = ugentools.SinOsc.ar()
                >>> result = ugen_graph - expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:440.0 -> 0_SinOsc[0:frequency]
                    const_1:0.0 -> 0_SinOsc[1:phase]
                    const_2:1.5 -> 1_BinaryOpUGen:SUBTRACTION[0:left]
                    0_SinOsc[0] -> 1_BinaryOpUGen:SUBTRACTION[1:right]
                }

        ..  container:: example

            **Example 2:**

            ::

                >>> ugen_graph = [220, 330]
                >>> expr = ugentools.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ...     )
                >>> result = ugen_graph - expr
                >>> result
                UGenArray({3})

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:440.0 -> 0_SinOsc[0:frequency]
                    const_1:0.0 -> 0_SinOsc[1:phase]
                    const_2:220.0 -> 1_BinaryOpUGen:SUBTRACTION[0:left]
                    0_SinOsc[0] -> 1_BinaryOpUGen:SUBTRACTION[1:right]
                    const_3:442.0 -> 2_SinOsc[0:frequency]
                    const_1:0.0 -> 2_SinOsc[1:phase]
                    const_4:330.0 -> 3_BinaryOpUGen:SUBTRACTION[0:left]
                    2_SinOsc[0] -> 3_BinaryOpUGen:SUBTRACTION[1:right]
                    const_5:443.0 -> 4_SinOsc[0:frequency]
                    const_1:0.0 -> 4_SinOsc[1:phase]
                    const_2:220.0 -> 5_BinaryOpUGen:SUBTRACTION[0:left]
                    4_SinOsc[0] -> 5_BinaryOpUGen:SUBTRACTION[1:right]
                }

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            expr,
            self,
            synthdeftools.BinaryOperator.SUBTRACTION,
            )

    def __str__(self):
        r'''Gets string representation of ugen graph.

        ::

            >>> ugen = ugentools.SinOsc.ar()
            >>> print(str(ugen))
            SynthDef ... {
                const_0:440.0 -> 0_SinOsc[0:frequency]
                const_1:0.0 -> 0_SinOsc[1:phase]
            }

        Returns string.
        '''
        from supriya.tools import synthdeftools
        builder = synthdeftools.SynthDefBuilder()
        builder.add_ugen(self)
        synthdef = builder.build()
        result = str(synthdef)
        return result

    def __sub__(self, expr):
        r'''Subtracts `expr` from ugen graph.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = ugentools.WhiteNoise.kr()
                >>> expr = ugentools.SinOsc.ar()
                >>> result = ugen_graph - expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:440.0 -> 1_SinOsc[0:frequency]
                    const_1:0.0 -> 1_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 2_BinaryOpUGen:SUBTRACTION[0:left]
                    1_SinOsc[0] -> 2_BinaryOpUGen:SUBTRACTION[1:right]
                }

        ..  container:: example

            **Example 2:**

            ::

                >>> ugen_graph = ugentools.WhiteNoise.kr()
                >>> expr = ugentools.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ...     )
                >>> result = ugen_graph - expr
                >>> result
                UGenArray({3})

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:440.0 -> 1_SinOsc[0:frequency]
                    const_1:0.0 -> 1_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 2_BinaryOpUGen:SUBTRACTION[0:left]
                    1_SinOsc[0] -> 2_BinaryOpUGen:SUBTRACTION[1:right]
                    const_2:442.0 -> 3_SinOsc[0:frequency]
                    const_1:0.0 -> 3_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 4_BinaryOpUGen:SUBTRACTION[0:left]
                    3_SinOsc[0] -> 4_BinaryOpUGen:SUBTRACTION[1:right]
                    const_3:443.0 -> 5_SinOsc[0:frequency]
                    const_1:0.0 -> 5_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 6_BinaryOpUGen:SUBTRACTION[0:left]
                    5_SinOsc[0] -> 6_BinaryOpUGen:SUBTRACTION[1:right]
                }

        ..  container:: example

            **Example 3:**

            ::

                >>> ugen_graph = ugentools.Dust.ar(
                ...     density=11.5,
                ...     )
                >>> expr = 4
                >>> result = ugen_graph - expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:11.5 -> 0_Dust[0:density]
                    0_Dust[0] -> 1_BinaryOpUGen:SUBTRACTION[0:left]
                    const_1:4.0 -> 1_BinaryOpUGen:SUBTRACTION[1:right]
                }

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            self,
            expr,
            synthdeftools.BinaryOperator.SUBTRACTION,
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
        for expanded_dict in synthdeftools.UGen._expand_dictionary(dictionary):
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
        b_rate = synthdeftools.Rate.from_input(ugen_b)
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