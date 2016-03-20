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

                >>> ugen_graph = ugentools.WhiteNoise.ar()
                >>> result = abs(ugen_graph)
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

                >>> ugen_graph = ugentools.SinOsc.ar(
                ...     frequency=(440, 442, 443),
                ...     )
                >>> result = abs(ugen_graph)
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
        builder.add_ugens(self)
        synthdef = builder.build()
        result = synthdef.__graph__()
        return result

    def __ge__(self, expr):
        r'''Tests if ugen graph if greater than or equal to `expr`.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = ugentools.WhiteNoise.kr()
                >>> expr = ugentools.SinOsc.ar()
                >>> result = ugen_graph >= expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:440.0 -> 1_SinOsc[0:frequency]
                    const_1:0.0 -> 1_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 2_BinaryOpUGen:GREATER_THAN_OR_EQUAL[0:left]
                    1_SinOsc[0] -> 2_BinaryOpUGen:GREATER_THAN_OR_EQUAL[1:right]
                }

        ..  container:: example

            **Example 2:**

            ::

                >>> ugen_graph = ugentools.WhiteNoise.kr()
                >>> expr = ugentools.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ...     )
                >>> result = ugen_graph >= expr
                >>> result
                UGenArray({3})

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:440.0 -> 1_SinOsc[0:frequency]
                    const_1:0.0 -> 1_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 2_BinaryOpUGen:GREATER_THAN_OR_EQUAL[0:left]
                    1_SinOsc[0] -> 2_BinaryOpUGen:GREATER_THAN_OR_EQUAL[1:right]
                    const_2:442.0 -> 3_SinOsc[0:frequency]
                    const_1:0.0 -> 3_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 4_BinaryOpUGen:GREATER_THAN_OR_EQUAL[0:left]
                    3_SinOsc[0] -> 4_BinaryOpUGen:GREATER_THAN_OR_EQUAL[1:right]
                    const_3:443.0 -> 5_SinOsc[0:frequency]
                    const_1:0.0 -> 5_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 6_BinaryOpUGen:GREATER_THAN_OR_EQUAL[0:left]
                    5_SinOsc[0] -> 6_BinaryOpUGen:GREATER_THAN_OR_EQUAL[1:right]
                }

        ..  container:: example

            **Example 3:**

            ::

                >>> ugen_graph = ugentools.Dust.ar(
                ...     density=11.5,
                ...     )
                >>> expr = 4
                >>> result = ugen_graph >= expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:11.5 -> 0_Dust[0:density]
                    0_Dust[0] -> 1_BinaryOpUGen:GREATER_THAN_OR_EQUAL[0:left]
                    const_1:4.0 -> 1_BinaryOpUGen:GREATER_THAN_OR_EQUAL[1:right]
                }

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            self,
            expr,
            synthdeftools.BinaryOperator.GREATER_THAN_OR_EQUAL,
            )

    def __gt__(self, expr):
        r'''Tests if ugen graph if greater than `expr`.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = ugentools.WhiteNoise.kr()
                >>> expr = ugentools.SinOsc.ar()
                >>> result = ugen_graph > expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:440.0 -> 1_SinOsc[0:frequency]
                    const_1:0.0 -> 1_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 2_BinaryOpUGen:GREATER_THAN[0:left]
                    1_SinOsc[0] -> 2_BinaryOpUGen:GREATER_THAN[1:right]
                }

        ..  container:: example

            **Example 2:**

            ::

                >>> ugen_graph = ugentools.WhiteNoise.kr()
                >>> expr = ugentools.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ...     )
                >>> result = ugen_graph > expr
                >>> result
                UGenArray({3})

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:440.0 -> 1_SinOsc[0:frequency]
                    const_1:0.0 -> 1_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 2_BinaryOpUGen:GREATER_THAN[0:left]
                    1_SinOsc[0] -> 2_BinaryOpUGen:GREATER_THAN[1:right]
                    const_2:442.0 -> 3_SinOsc[0:frequency]
                    const_1:0.0 -> 3_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 4_BinaryOpUGen:GREATER_THAN[0:left]
                    3_SinOsc[0] -> 4_BinaryOpUGen:GREATER_THAN[1:right]
                    const_3:443.0 -> 5_SinOsc[0:frequency]
                    const_1:0.0 -> 5_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 6_BinaryOpUGen:GREATER_THAN[0:left]
                    5_SinOsc[0] -> 6_BinaryOpUGen:GREATER_THAN[1:right]
                }

        ..  container:: example

            **Example 3:**

            ::

                >>> ugen_graph = ugentools.Dust.ar(
                ...     density=11.5,
                ...     )
                >>> expr = 4
                >>> result = ugen_graph > expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:11.5 -> 0_Dust[0:density]
                    0_Dust[0] -> 1_BinaryOpUGen:GREATER_THAN[0:left]
                    const_1:4.0 -> 1_BinaryOpUGen:GREATER_THAN[1:right]
                }

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            self,
            expr,
            synthdeftools.BinaryOperator.GREATER_THAN,
            )

    def __le__(self, expr):
        r'''Tests if ugen graph if less than or equal to `expr`.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = ugentools.WhiteNoise.kr()
                >>> expr = ugentools.SinOsc.ar()
                >>> result = ugen_graph <= expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:440.0 -> 1_SinOsc[0:frequency]
                    const_1:0.0 -> 1_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 2_BinaryOpUGen:LESS_THAN_OR_EQUAL[0:left]
                    1_SinOsc[0] -> 2_BinaryOpUGen:LESS_THAN_OR_EQUAL[1:right]
                }

        ..  container:: example

            **Example 2:**

            ::

                >>> ugen_graph = ugentools.WhiteNoise.kr()
                >>> expr = ugentools.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ...     )
                >>> result = ugen_graph <= expr
                >>> result
                UGenArray({3})

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:440.0 -> 1_SinOsc[0:frequency]
                    const_1:0.0 -> 1_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 2_BinaryOpUGen:LESS_THAN_OR_EQUAL[0:left]
                    1_SinOsc[0] -> 2_BinaryOpUGen:LESS_THAN_OR_EQUAL[1:right]
                    const_2:442.0 -> 3_SinOsc[0:frequency]
                    const_1:0.0 -> 3_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 4_BinaryOpUGen:LESS_THAN_OR_EQUAL[0:left]
                    3_SinOsc[0] -> 4_BinaryOpUGen:LESS_THAN_OR_EQUAL[1:right]
                    const_3:443.0 -> 5_SinOsc[0:frequency]
                    const_1:0.0 -> 5_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 6_BinaryOpUGen:LESS_THAN_OR_EQUAL[0:left]
                    5_SinOsc[0] -> 6_BinaryOpUGen:LESS_THAN_OR_EQUAL[1:right]
                }

        ..  container:: example

            **Example 3:**

            ::

                >>> ugen_graph = ugentools.Dust.ar(
                ...     density=11.5,
                ...     )
                >>> expr = 4
                >>> result = ugen_graph <= expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:11.5 -> 0_Dust[0:density]
                    0_Dust[0] -> 1_BinaryOpUGen:LESS_THAN_OR_EQUAL[0:left]
                    const_1:4.0 -> 1_BinaryOpUGen:LESS_THAN_OR_EQUAL[1:right]
                }

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            self,
            expr,
            synthdeftools.BinaryOperator.LESS_THAN_OR_EQUAL,
            )

    def __lt__(self, expr):
        r'''Tests if ugen graph if less than `expr`.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = ugentools.WhiteNoise.kr()
                >>> expr = ugentools.SinOsc.ar()
                >>> result = ugen_graph < expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:440.0 -> 1_SinOsc[0:frequency]
                    const_1:0.0 -> 1_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 2_BinaryOpUGen:LESS_THAN[0:left]
                    1_SinOsc[0] -> 2_BinaryOpUGen:LESS_THAN[1:right]
                }

        ..  container:: example

            **Example 2:**

            ::

                >>> ugen_graph = ugentools.WhiteNoise.kr()
                >>> expr = ugentools.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ...     )
                >>> result = ugen_graph < expr
                >>> result
                UGenArray({3})

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:440.0 -> 1_SinOsc[0:frequency]
                    const_1:0.0 -> 1_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 2_BinaryOpUGen:LESS_THAN[0:left]
                    1_SinOsc[0] -> 2_BinaryOpUGen:LESS_THAN[1:right]
                    const_2:442.0 -> 3_SinOsc[0:frequency]
                    const_1:0.0 -> 3_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 4_BinaryOpUGen:LESS_THAN[0:left]
                    3_SinOsc[0] -> 4_BinaryOpUGen:LESS_THAN[1:right]
                    const_3:443.0 -> 5_SinOsc[0:frequency]
                    const_1:0.0 -> 5_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 6_BinaryOpUGen:LESS_THAN[0:left]
                    5_SinOsc[0] -> 6_BinaryOpUGen:LESS_THAN[1:right]
                }

        ..  container:: example

            **Example 3:**

            ::

                >>> ugen_graph = ugentools.Dust.ar(
                ...     density=11.5,
                ...     )
                >>> expr = 4
                >>> result = ugen_graph < expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:11.5 -> 0_Dust[0:density]
                    0_Dust[0] -> 1_BinaryOpUGen:LESS_THAN[0:left]
                    const_1:4.0 -> 1_BinaryOpUGen:LESS_THAN[1:right]
                }

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            self,
            expr,
            synthdeftools.BinaryOperator.LESS_THAN,
            )

    def __mod__(self, expr):
        r'''Gets modulo of ugen graph and `expr`.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = ugentools.WhiteNoise.kr()
                >>> expr = ugentools.SinOsc.ar()
                >>> result = ugen_graph % expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:440.0 -> 1_SinOsc[0:frequency]
                    const_1:0.0 -> 1_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 2_BinaryOpUGen:MODULO[0:left]
                    1_SinOsc[0] -> 2_BinaryOpUGen:MODULO[1:right]
                }

        ..  container:: example

            **Example 2:**

            ::

                >>> ugen_graph = ugentools.WhiteNoise.kr()
                >>> expr = ugentools.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ...     )
                >>> result = ugen_graph % expr
                >>> result
                UGenArray({3})

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:440.0 -> 1_SinOsc[0:frequency]
                    const_1:0.0 -> 1_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 2_BinaryOpUGen:MODULO[0:left]
                    1_SinOsc[0] -> 2_BinaryOpUGen:MODULO[1:right]
                    const_2:442.0 -> 3_SinOsc[0:frequency]
                    const_1:0.0 -> 3_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 4_BinaryOpUGen:MODULO[0:left]
                    3_SinOsc[0] -> 4_BinaryOpUGen:MODULO[1:right]
                    const_3:443.0 -> 5_SinOsc[0:frequency]
                    const_1:0.0 -> 5_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 6_BinaryOpUGen:MODULO[0:left]
                    5_SinOsc[0] -> 6_BinaryOpUGen:MODULO[1:right]
                }

        ..  container:: example

            **Example 3:**

            ::

                >>> ugen_graph = ugentools.Dust.ar(
                ...     density=11.5,
                ...     )
                >>> expr = 4
                >>> result = ugen_graph % expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:11.5 -> 0_Dust[0:density]
                    0_Dust[0] -> 1_BinaryOpUGen:MODULO[0:left]
                    const_1:4.0 -> 1_BinaryOpUGen:MODULO[1:right]
                }

        Returns ugen graph.
        '''
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

                >>> ugen_graph = ugentools.WhiteNoise.ar()
                >>> result = -ugen_graph
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

                >>> ugen_graph = ugentools.SinOsc.ar(
                ...     frequency=(440, 442, 443),
                ...     )
                >>> result = -ugen_graph
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

    def __pow__(self, expr):
        r'''Raises ugen graph to the power of `expr`.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = ugentools.WhiteNoise.kr()
                >>> expr = ugentools.SinOsc.ar()
                >>> result = ugen_graph ** expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:440.0 -> 1_SinOsc[0:frequency]
                    const_1:0.0 -> 1_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 2_BinaryOpUGen:POWER[0:left]
                    1_SinOsc[0] -> 2_BinaryOpUGen:POWER[1:right]
                }

        ..  container:: example

            **Example 2:**

            ::

                >>> ugen_graph = ugentools.WhiteNoise.kr()
                >>> expr = ugentools.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ...     )
                >>> result = ugen_graph ** expr
                >>> result
                UGenArray({3})

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:440.0 -> 1_SinOsc[0:frequency]
                    const_1:0.0 -> 1_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 2_BinaryOpUGen:POWER[0:left]
                    1_SinOsc[0] -> 2_BinaryOpUGen:POWER[1:right]
                    const_2:442.0 -> 3_SinOsc[0:frequency]
                    const_1:0.0 -> 3_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 4_BinaryOpUGen:POWER[0:left]
                    3_SinOsc[0] -> 4_BinaryOpUGen:POWER[1:right]
                    const_3:443.0 -> 5_SinOsc[0:frequency]
                    const_1:0.0 -> 5_SinOsc[1:phase]
                    0_WhiteNoise[0] -> 6_BinaryOpUGen:POWER[0:left]
                    5_SinOsc[0] -> 6_BinaryOpUGen:POWER[1:right]
                }

        ..  container:: example

            **Example 3:**

            ::

                >>> ugen_graph = ugentools.Dust.ar(
                ...     density=11.5,
                ...     )
                >>> expr = 4
                >>> result = ugen_graph ** expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:11.5 -> 0_Dust[0:density]
                    0_Dust[0] -> 1_BinaryOpUGen:POWER[0:left]
                    const_1:4.0 -> 1_BinaryOpUGen:POWER[1:right]
                }

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            self,
            expr,
            synthdeftools.BinaryOperator.POWER,
            )

    def __rpow__(self, expr):
        r'''Raises `expr` to the power of ugen graph.

        ..  container:: example

            **Example 1:**

            ::

                >>> expr = 1.5
                >>> ugen_graph = ugentools.SinOsc.ar()
                >>> result = expr ** ugen_graph
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:440.0 -> 0_SinOsc[0:frequency]
                    const_1:0.0 -> 0_SinOsc[1:phase]
                    const_2:1.5 -> 1_BinaryOpUGen:POWER[0:left]
                    0_SinOsc[0] -> 1_BinaryOpUGen:POWER[1:right]
                }

        ..  container:: example

            **Example 2:**

            ::

                >>> expr = [220, 330]
                >>> ugen_graph = ugentools.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ...     )
                >>> result = expr ** ugen_graph
                >>> result
                UGenArray({3})

            ::

                >>> print(str(result))
                SynthDef ... {
                    const_0:440.0 -> 0_SinOsc[0:frequency]
                    const_1:0.0 -> 0_SinOsc[1:phase]
                    const_2:220.0 -> 1_BinaryOpUGen:POWER[0:left]
                    0_SinOsc[0] -> 1_BinaryOpUGen:POWER[1:right]
                    const_3:442.0 -> 2_SinOsc[0:frequency]
                    const_1:0.0 -> 2_SinOsc[1:phase]
                    const_4:330.0 -> 3_BinaryOpUGen:POWER[0:left]
                    2_SinOsc[0] -> 3_BinaryOpUGen:POWER[1:right]
                    const_5:443.0 -> 4_SinOsc[0:frequency]
                    const_1:0.0 -> 4_SinOsc[1:phase]
                    const_2:220.0 -> 5_BinaryOpUGen:POWER[0:left]
                    4_SinOsc[0] -> 5_BinaryOpUGen:POWER[1:right]
                }

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            expr,
            self,
            synthdeftools.BinaryOperator.POWER,
            )

    def __radd__(self, expr):
        r'''Adds ugen graph to `expr`.

        ..  container:: example

            **Example 1:**

            ::

                >>> expr = 1.5
                >>> ugen_graph = ugentools.SinOsc.ar()
                >>> result = expr + ugen_graph
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

                >>> expr = [220, 330]
                >>> ugen_graph = ugentools.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ...     )
                >>> result = expr + ugen_graph
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

                >>> expr = 1.5
                >>> ugen_graph = ugentools.SinOsc.ar()
                >>> result = expr / ugen_graph
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

                >>> expr = [220, 330]
                >>> ugen_graph = ugentools.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ...     )
                >>> result = expr / ugen_graph
                >>> result
                UGenArray({3})

            ::

                >>> print(str(result))
                SynthDef ... {
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

    def __rmod__(self, expr):
        r'''Gets modulo of `expr` and ugen graph.

        ..  container:: example

            **Example 1:**

            ::

                >>> expr = 1.5
                >>> ugen_graph = ugentools.SinOsc.ar()
                >>> result = expr % ugen_graph
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

                >>> expr = [220, 330]
                >>> ugen_graph = ugentools.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ...     )
                >>> result = expr % ugen_graph
                >>> result
                UGenArray({3})

            ::

                >>> print(str(result))
                SynthDef ... {
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

                >>> expr = 1.5
                >>> ugen_graph = ugentools.SinOsc.ar()
                >>> result = expr * ugen_graph
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

                >>> expr = [220, 330]
                >>> ugen_graph = ugentools.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ...     )
                >>> result = expr * ugen_graph
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

                >>> expr = 1.5
                >>> ugen_graph = ugentools.SinOsc.ar()
                >>> result = expr - ugen_graph
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

                >>> expr = [220, 330]
                >>> ugen_graph = ugentools.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ...     )
                >>> result = expr - ugen_graph
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
        builder.add_ugens(self)
        synthdef = builder.build(optimize=False)
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

    __truediv__ = __div__
    __rtruediv__ = __rdiv__

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
        for expanded_dict in ugentools.UGen._expand_dictionary(dictionary):
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
        a_rate = synthdeftools.CalculationRate.from_input(ugen_a)
        b_rate = synthdeftools.CalculationRate.from_input(ugen_b)
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

    def _compute_ugen_map(self, map_ugen, **kwargs):
        from supriya.tools import synthdeftools
        from supriya.tools import ugentools
        ugens = []
        for source in self[:]:
            method = ugentools.UGen._get_method_for_rate(map_ugen, source)
            ugen = method(
                source=source,
                **kwargs
                )
            ugens.extend(ugen)
        if 1 < len(ugens):
            return synthdeftools.UGenArray(ugens)
        elif len(ugens) == 1:
            return ugens[0].source
        return []

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
            calculation_rate = synthdeftools.CalculationRate.from_input(
                single_source)
            ugen = ugentools.UnaryOpUGen._new_single(
                calculation_rate=calculation_rate,
                source=single_source,
                special_index=special_index,
                )
            result.append(ugen)
        if len(result) == 1:
            return result[0]
        return synthdeftools.UGenArray(result)

    def _get_output_proxy(self, i):
        from supriya import synthdeftools
        if isinstance(i, int):
            if not (0 <= i < len(self)):
                raise IndexError(i, len(self))
            return synthdeftools.OutputProxy(self, i)
        indices = i.indices(len(self))
        if not (0 <= indices[0] <= indices[1] <= len(self)):
            raise IndexError(i, indices, len(self))
        output_proxies = (
            synthdeftools.OutputProxy(self, i)
            for i in range(*indices)
            )
        return synthdeftools.UGenArray(output_proxies)

    ### PUBLIC METHODS ###

    def clip(self, minimum, maximum):
        r'''Clips ugen graph.

        ..  container:: example::

            >>> ugen_graph = ugentools.WhiteNoise.ar()
            >>> result = ugen_graph.clip(-0.25, 0.25)
            >>> print(str(result))
            SynthDef e710843b0e0fbc5e6185afc6cdf90149 {
                0_WhiteNoise[0] -> 1_Clip[0:source]
                const_0:-0.25 -> 1_Clip[1:minimum]
                const_1:0.25 -> 1_Clip[2:maximum]
            }

        ..  container:: example::

            >>> ugen_graph = ugentools.SinOsc.ar(
            ...     frequency=[440, 442, 443],
            ...     )
            >>> result = ugen_graph.clip(-0.25, 0.25)
            >>> print(str(result))
            SynthDef 000e997ea0d7e8637c9f9040547baa50 {
                const_0:440.0 -> 0_SinOsc[0:frequency]
                const_1:0.0 -> 0_SinOsc[1:phase]
                0_SinOsc[0] -> 1_Clip[0:source]
                const_2:-0.25 -> 1_Clip[1:minimum]
                const_3:0.25 -> 1_Clip[2:maximum]
                const_4:442.0 -> 2_SinOsc[0:frequency]
                const_1:0.0 -> 2_SinOsc[1:phase]
                2_SinOsc[0] -> 3_Clip[0:source]
                const_2:-0.25 -> 3_Clip[1:minimum]
                const_3:0.25 -> 3_Clip[2:maximum]
                const_5:443.0 -> 4_SinOsc[0:frequency]
                const_1:0.0 -> 4_SinOsc[1:phase]
                4_SinOsc[0] -> 5_Clip[0:source]
                const_2:-0.25 -> 5_Clip[1:minimum]
                const_3:0.25 -> 5_Clip[2:maximum]
            }

        '''
        from supriya.tools import ugentools
        return self._compute_ugen_map(
            ugentools.Clip,
            minimum=minimum,
            maximum=maximum,
            )

    def lag(
        self,
        lag_time=0.5,
        ):
        r'''Lags ugen graph.

        ..  container:: example::

            >>> ugen_graph = ugentools.WhiteNoise.ar()
            >>> result = ugen_graph.lag(0.5)
            >>> print(str(result))
            SynthDef 6c3e2cc1a3d54ecfaa49d567a84eae77 {
                0_WhiteNoise[0] -> 1_Lag[0:source]
                const_0:0.5 -> 1_Lag[1:lag_time]
            }

        ..  container:: example::

            >>> ugen_graph = ugentools.SinOsc.ar(
            ...     frequency=[440, 442, 443],
            ...     )
            >>> result = ugen_graph.lag(0.5)
            >>> print(str(result))
            SynthDef 67098a4ddab35f6e1333a80a226bf559 {
                const_0:440.0 -> 0_SinOsc[0:frequency]
                const_1:0.0 -> 0_SinOsc[1:phase]
                0_SinOsc[0] -> 1_Lag[0:source]
                const_2:0.5 -> 1_Lag[1:lag_time]
                const_3:442.0 -> 2_SinOsc[0:frequency]
                const_1:0.0 -> 2_SinOsc[1:phase]
                2_SinOsc[0] -> 3_Lag[0:source]
                const_2:0.5 -> 3_Lag[1:lag_time]
                const_4:443.0 -> 4_SinOsc[0:frequency]
                const_1:0.0 -> 4_SinOsc[1:phase]
                4_SinOsc[0] -> 5_Lag[0:source]
                const_2:0.5 -> 5_Lag[1:lag_time]
            }

        '''
        from supriya.tools import ugentools
        return self._compute_ugen_map(
            ugentools.Lag,
            lag_time=lag_time,
            )

    def scale(
        self,
        input_minimum,
        input_maximum,
        output_minimum,
        output_maximum,
        exponential=False,
        ):
        r'''Lags ugen graph.

        ..  container:: example::

            >>> ugen_graph = ugentools.WhiteNoise.ar()
            >>> result = ugen_graph.scale(-1, 1, 0.5, 0.75)
            >>> print(str(result))
            SynthDef e2295e64ed7b9c949ec22ccdc82520e3 {
                0_WhiteNoise[0] -> 1_MulAdd[0:source]
                const_0:0.125 -> 1_MulAdd[1:multiplier]
                const_1:0.625 -> 1_MulAdd[2:addend]
            }

        ..  container:: example::

            >>> ugen_graph = ugentools.SinOsc.ar(
            ...     frequency=[440, 442, 443],
            ...     )
            >>> result = ugen_graph.scale(-1, 1, 0.5, 0.75, exponential=True)
            >>> print(str(result))
            SynthDef 88dca305143542bd40a82d8a6a337306 {
                const_0:440.0 -> 0_SinOsc[0:frequency]
                const_1:0.0 -> 0_SinOsc[1:phase]
                0_SinOsc[0] -> 1_LinExp[0:source]
                const_2:-1.0 -> 1_LinExp[1:input_minimum]
                const_3:1.0 -> 1_LinExp[2:input_maximum]
                const_4:0.5 -> 1_LinExp[3:output_minimum]
                const_5:0.75 -> 1_LinExp[4:output_maximum]
                const_6:442.0 -> 2_SinOsc[0:frequency]
                const_1:0.0 -> 2_SinOsc[1:phase]
                2_SinOsc[0] -> 3_LinExp[0:source]
                const_2:-1.0 -> 3_LinExp[1:input_minimum]
                const_3:1.0 -> 3_LinExp[2:input_maximum]
                const_4:0.5 -> 3_LinExp[3:output_minimum]
                const_5:0.75 -> 3_LinExp[4:output_maximum]
                const_7:443.0 -> 4_SinOsc[0:frequency]
                const_1:0.0 -> 4_SinOsc[1:phase]
                4_SinOsc[0] -> 5_LinExp[0:source]
                const_2:-1.0 -> 5_LinExp[1:input_minimum]
                const_3:1.0 -> 5_LinExp[2:input_maximum]
                const_4:0.5 -> 5_LinExp[3:output_minimum]
                const_5:0.75 -> 5_LinExp[4:output_maximum]
            }

        '''
        from supriya.tools import ugentools
        map_ugen = ugentools.LinLin
        if exponential:
            map_ugen = ugentools.LinExp
        return self._compute_ugen_map(
            map_ugen,
            input_minimum=input_minimum,
            input_maximum=input_maximum,
            output_minimum=output_minimum,
            output_maximum=output_maximum,
            )
