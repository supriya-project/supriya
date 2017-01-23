# -*- encoding: utf-8 -*-
import collections
import copy
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class UGenMethodMixin(SupriyaObject):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'SynthDef Internals'

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __abs__(self):
        """
        Gets absolute value of ugen graph.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = ugentools.WhiteNoise.ar()
                >>> result = abs(ugen_graph)
                >>> result
                UnaryOpUGen.ar()

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
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

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
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
        """
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_unary_op(
            self,
            synthdeftools.UnaryOperator.ABSOLUTE_VALUE,
            )

    def __add__(self, expr):
        """
        Adds `expr` to ugen graph.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = ugentools.WhiteNoise.kr()
                >>> expr = ugentools.SinOsc.ar()
                >>> result = ugen_graph + expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
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

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
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

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
                SynthDef ... {
                    const_0:11.5 -> 0_Dust[0:density]
                    0_Dust[0] -> 1_BinaryOpUGen:ADDITION[0:left]
                    const_1:4.0 -> 1_BinaryOpUGen:ADDITION[1:right]
                }

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            self,
            expr,
            synthdeftools.BinaryOperator.ADDITION,
            )

    def __div__(self, expr):
        """
        Divides ugen graph by `expr`.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = ugentools.WhiteNoise.kr()
                >>> expr = ugentools.SinOsc.ar()
                >>> result = ugen_graph / expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
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

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
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

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
                SynthDef ... {
                    const_0:11.5 -> 0_Dust[0:density]
                    0_Dust[0] -> 1_BinaryOpUGen:FLOAT_DIVISION[0:left]
                    const_1:4.0 -> 1_BinaryOpUGen:FLOAT_DIVISION[1:right]
                }

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            self,
            expr,
            synthdeftools.BinaryOperator.FLOAT_DIVISION,
            )

    def __graph__(self):
        """
        Gets Graphviz representation of ugen graph.

        Returns GraphvizGraph instance.
        """
        synthdef = self._clone()
        result = synthdef.__graph__()
        return result

    def __ge__(self, expr):
        """
        Tests if ugen graph if greater than or equal to `expr`.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = ugentools.WhiteNoise.kr()
                >>> expr = ugentools.SinOsc.ar()
                >>> result = ugen_graph >= expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
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

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
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

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
                SynthDef ... {
                    const_0:11.5 -> 0_Dust[0:density]
                    0_Dust[0] -> 1_BinaryOpUGen:GREATER_THAN_OR_EQUAL[0:left]
                    const_1:4.0 -> 1_BinaryOpUGen:GREATER_THAN_OR_EQUAL[1:right]
                }

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            self,
            expr,
            synthdeftools.BinaryOperator.GREATER_THAN_OR_EQUAL,
            )

    def __gt__(self, expr):
        """
        Tests if ugen graph if greater than `expr`.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = ugentools.WhiteNoise.kr()
                >>> expr = ugentools.SinOsc.ar()
                >>> result = ugen_graph > expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
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

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
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

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
                SynthDef ... {
                    const_0:11.5 -> 0_Dust[0:density]
                    0_Dust[0] -> 1_BinaryOpUGen:GREATER_THAN[0:left]
                    const_1:4.0 -> 1_BinaryOpUGen:GREATER_THAN[1:right]
                }

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            self,
            expr,
            synthdeftools.BinaryOperator.GREATER_THAN,
            )

    def __le__(self, expr):
        """
        Tests if ugen graph if less than or equal to `expr`.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = ugentools.WhiteNoise.kr()
                >>> expr = ugentools.SinOsc.ar()
                >>> result = ugen_graph <= expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
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

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
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

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
                SynthDef ... {
                    const_0:11.5 -> 0_Dust[0:density]
                    0_Dust[0] -> 1_BinaryOpUGen:LESS_THAN_OR_EQUAL[0:left]
                    const_1:4.0 -> 1_BinaryOpUGen:LESS_THAN_OR_EQUAL[1:right]
                }

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            self,
            expr,
            synthdeftools.BinaryOperator.LESS_THAN_OR_EQUAL,
            )

    def __lt__(self, expr):
        """
        Tests if ugen graph if less than `expr`.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = ugentools.WhiteNoise.kr()
                >>> expr = ugentools.SinOsc.ar()
                >>> result = ugen_graph < expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
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

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
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

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
                SynthDef ... {
                    const_0:11.5 -> 0_Dust[0:density]
                    0_Dust[0] -> 1_BinaryOpUGen:LESS_THAN[0:left]
                    const_1:4.0 -> 1_BinaryOpUGen:LESS_THAN[1:right]
                }

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            self,
            expr,
            synthdeftools.BinaryOperator.LESS_THAN,
            )

    def __mod__(self, expr):
        """
        Gets modulo of ugen graph and `expr`.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = ugentools.WhiteNoise.kr()
                >>> expr = ugentools.SinOsc.ar()
                >>> result = ugen_graph % expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
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

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
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

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
                SynthDef ... {
                    const_0:11.5 -> 0_Dust[0:density]
                    0_Dust[0] -> 1_BinaryOpUGen:MODULO[0:left]
                    const_1:4.0 -> 1_BinaryOpUGen:MODULO[1:right]
                }

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            self,
            expr,
            synthdeftools.BinaryOperator.MODULO,
            )

    def __mul__(self, expr):
        """
        Multiplies ugen graph by `expr`.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = ugentools.WhiteNoise.kr()
                >>> expr = ugentools.SinOsc.ar()
                >>> result = ugen_graph * expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
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

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
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

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
                SynthDef ... {
                    const_0:11.5 -> 0_Dust[0:density]
                    0_Dust[0] -> 1_BinaryOpUGen:MULTIPLICATION[0:left]
                    const_1:4.0 -> 1_BinaryOpUGen:MULTIPLICATION[1:right]
                }

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            self,
            expr,
            synthdeftools.BinaryOperator.MULTIPLICATION,
            )

    def __neg__(self):
        """
        Negates ugen graph.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = ugentools.WhiteNoise.ar()
                >>> result = -ugen_graph
                >>> result
                UnaryOpUGen.ar()

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
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

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
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
        """
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_unary_op(
            self,
            synthdeftools.UnaryOperator.NEGATIVE,
            )

    def __pow__(self, expr):
        """
        Raises ugen graph to the power of `expr`.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = ugentools.WhiteNoise.kr()
                >>> expr = ugentools.SinOsc.ar()
                >>> result = ugen_graph ** expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
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

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
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

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
                SynthDef ... {
                    const_0:11.5 -> 0_Dust[0:density]
                    0_Dust[0] -> 1_BinaryOpUGen:POWER[0:left]
                    const_1:4.0 -> 1_BinaryOpUGen:POWER[1:right]
                }

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            self,
            expr,
            synthdeftools.BinaryOperator.POWER,
            )

    def __rpow__(self, expr):
        """
        Raises `expr` to the power of ugen graph.

        ..  container:: example

            **Example 1:**

            ::

                >>> expr = 1.5
                >>> ugen_graph = ugentools.SinOsc.ar()
                >>> result = expr ** ugen_graph
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
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

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
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
        """
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            expr,
            self,
            synthdeftools.BinaryOperator.POWER,
            )

    def __radd__(self, expr):
        """
        Adds ugen graph to `expr`.

        ..  container:: example

            **Example 1:**

            ::

                >>> expr = 1.5
                >>> ugen_graph = ugentools.SinOsc.ar()
                >>> result = expr + ugen_graph
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
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

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
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
        """
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            expr,
            self,
            synthdeftools.BinaryOperator.ADDITION,
            )

    def __rdiv__(self, expr):
        """
        Divides `expr` by ugen graph.

        ..  container:: example

            **Example 1:**

            ::

                >>> expr = 1.5
                >>> ugen_graph = ugentools.SinOsc.ar()
                >>> result = expr / ugen_graph
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
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

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
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
        """
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            expr,
            self,
            synthdeftools.BinaryOperator.FLOAT_DIVISION,
            )

    def __rmod__(self, expr):
        """
        Gets modulo of `expr` and ugen graph.

        ..  container:: example

            **Example 1:**

            ::

                >>> expr = 1.5
                >>> ugen_graph = ugentools.SinOsc.ar()
                >>> result = expr % ugen_graph
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
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

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
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
        """
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            expr,
            self,
            synthdeftools.BinaryOperator.FLOAT_DIVISION,
            )

    def __rmul__(self, expr):
        """
        Multiplies `expr` by ugen graph.

        ..  container:: example

            **Example 1:**

            ::

                >>> expr = 1.5
                >>> ugen_graph = ugentools.SinOsc.ar()
                >>> result = expr * ugen_graph
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
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

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
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
        """
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            expr,
            self,
            synthdeftools.BinaryOperator.MULTIPLICATION,
            )

    def __rsub__(self, expr):
        """
        Subtracts ugen graph from `expr`.

        ..  container:: example

            **Example 1:**

            ::

                >>> expr = 1.5
                >>> ugen_graph = ugentools.SinOsc.ar()
                >>> result = expr - ugen_graph
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
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

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
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
        """
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            expr,
            self,
            synthdeftools.BinaryOperator.SUBTRACTION,
            )

    def __str__(self):
        """
        Gets string representation of ugen graph.

        ..  container:: example

            ::

                >>> ugen_graph = ugentools.SinOsc.ar()
                >>> print(str(ugen_graph))
                SynthDef ... {
                    const_0:440.0 -> 0_SinOsc[0:frequency]
                    const_1:0.0 -> 0_SinOsc[1:phase]
                }

        ..  container:: example

            ::

                >>> ugen_graph = ugentools.SinOsc.ar(frequency=[1, 2, 3])
                >>> print(str(ugen_graph))
                SynthDef 4015dac116b25c54b4a6f02bcb5859cb {
                    const_0:1.0 -> 0_SinOsc[0:frequency]
                    const_1:0.0 -> 0_SinOsc[1:phase]
                    const_2:2.0 -> 1_SinOsc[0:frequency]
                    const_1:0.0 -> 1_SinOsc[1:phase]
                    const_3:3.0 -> 2_SinOsc[0:frequency]
                    const_1:0.0 -> 2_SinOsc[1:phase]
                }

        Returns string.
        """
        synthdef = self._clone()
        result = str(synthdef)
        return result

    def __sub__(self, expr):
        """
        Subtracts `expr` from ugen graph.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = ugentools.WhiteNoise.kr()
                >>> expr = ugentools.SinOsc.ar()
                >>> result = ugen_graph - expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
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

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
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

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
                SynthDef ... {
                    const_0:11.5 -> 0_Dust[0:density]
                    0_Dust[0] -> 1_BinaryOpUGen:SUBTRACTION[0:left]
                    const_1:4.0 -> 1_BinaryOpUGen:SUBTRACTION[1:right]
                }

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        return UGenMethodMixin._compute_binary_op(
            self,
            expr,
            synthdeftools.BinaryOperator.SUBTRACTION,
            )

    __truediv__ = __div__
    __rtruediv__ = __rdiv__

    ### PRIVATE METHODS ###

    def _clone(self):
        def recurse(uuid, ugen, all_ugens):
            if hasattr(ugen, 'inputs'):
                for input_ in ugen.inputs:
                    if not isinstance(input_, synthdeftools.OutputProxy):
                        continue
                    input_ = input_.source
                    input_._uuid = uuid
                    recurse(uuid, input_, all_ugens)
            ugen._uuid = uuid
            if ugen not in all_ugens:
                all_ugens.append(ugen)

        from supriya.tools import synthdeftools
        from supriya.tools import ugentools
        builder = synthdeftools.SynthDefBuilder()
        ugens = copy.deepcopy(self)
        if not isinstance(ugens, synthdeftools.UGenArray):
            ugens = [ugens]
        all_ugens = []
        for ugen in ugens:
            if isinstance(ugen, synthdeftools.OutputProxy):
                ugen = ugen.source
            recurse(builder._uuid, ugen, all_ugens)
        for ugen in all_ugens:
            if isinstance(ugen, ugentools.UGen):
                builder._add_ugens(ugen)
            else:
                builder._add_parameter(ugen)
        return builder.build(optimize=False)

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
        sources = []
        ugens = []
        if len(self) == 1:
            sources = [self]
        else:
            sources = self
        for source in sources:
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

    """
    # ABSOLUTE_VALUE = 5
    # AMPLITUDE_TO_DB = 22
    ARCCOS = 32
    ARCSIN = 31
    ARCTAN = 33
    AS_FLOAT = 6
    AS_INT = 7
    BILINRAND = 40
    BIT_NOT = 4
    CEILING = 8
    COIN = 44
    COS = 29
    COSH = 35
    CUBED = 13
    # DB_TO_AMPLITUDE = 21
    DIGIT_VALUE = 45
    DISTORT = 42
    EXPONENTIAL = 15
    FLOOR = 9
    FRACTIONAL_PART = 10
    # HZ_TO_MIDI = 18
    # HZ_TO_OCTAVE = 24
    # HANNING_WINDOW = 49
    IS_NIL = 2
    LINRAND = 39
    LOG = 25
    LOG10 = 27
    LOG2 = 26
    # MIDI_TO_HZ = 17
    # SEMITONES_TO_RATIO = 19
    # NEGATIVE = 0
    NOT = 1
    NOT_NIL = 3
    # OCTAVE_TO_HZ = 23
    RAMP = 52
    RAND = 37
    RAND2 = 38
    # RATIO_TO_SEMITONES = 20
    # RECIPROCAL = 16
    # RECTANGLE_WINDOW = 48
    # S_CURVE = 53
    # SIGN = 11
    SILENCE = 46
    SIN = 28
    SINH = 34
    SOFTCLIP = 43
    # SQUARE_ROOT = 14
    # SQUARED = 12
    SUM3RAND = 41
    TAN = 30
    # TANH = 36
    THRU = 47
    # TRIANGLE_WINDOW = 51
    # WELCH_WINDOW = 50
    """

    """
    # ABSOLUTE_DIFFERENCE = 38  # |a - b|
    # ADDITION = 0
    AMCLIP = 40
    ATAN2 = 22
    BIT_AND = 14
    BIT_OR = 15
    BIT_XOR = 16
    CLIP2 = 42
    DIFFERENCE_OF_SQUARES = 34  # a*a - b*b
    # EQUAL = 6
    EXCESS = 43
    EXPRANDRANGE = 48
    FLOAT_DIVISION = 4
    FILL = 29
    FIRST_ARG = 46
    FOLD2 = 44
    GREATEST_COMMON_DIVISOR = 18
    GREATER_THAN_OR_EQUAL = 11
    GREATER_THAN = 9
    HYPOT = 23
    HYPOTX = 24
    INTEGER_DIVISION = 3
    LEAST_COMMON_MULTIPLE = 17
    LESS_THAN_OR_EQUAL = 10
    LESS_THAN = 8
    # MAXIMUM = 13
    # MINIMUM = 12
    # MODULO = 5
    # MULTIPLICATION = 2
    # NOT_EQUAL = 7
    # POWER = 25
    RANDRANGE = 47
    RING1 = 30  # a * (b + 1) == a * b + a
    RING2 = 31  # a * b + a + b
    RING3 = 32  # a*a*b
    RING4 = 33  # a*a*b - a*b*b
    ROUND = 19
    ROUND_UP = 20
    SCALE_NEG = 41
    SHIFT_LEFT = 26
    SHIFT_RIGHT = 27
    SQUARE_OF_DIFFERENCE = 37  # (a - b)^2
    SQUARE_OF_SUM = 36  # (a + b)^2
    # SUBTRACTION = 1
    SUM_OF_SQUARES = 35  # a*a + b*b
    THRESHOLD = 39
    TRUNCATION = 21
    UNSIGNED_SHIFT = 28
    WRAP2 = 45
    """

    def absolute_difference(self, expr):
        """
        Calculates absolute difference between ugen graph and `expr`.

        ..  container:: example

            ::

                >>> ugen_graph = ugentools.SinOsc.ar()
                >>> expr = ugentools.WhiteNoise.kr()
                >>> result = ugen_graph.absolute_difference(expr)

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
                SynthDef ... {
                    const_0:440.0 -> 0_SinOsc[0:frequency]
                    const_1:0.0 -> 0_SinOsc[1:phase]
                    0_SinOsc[0] -> 2_BinaryOpUGen:ABSOLUTE_DIFFERENCE[0:left]
                    1_WhiteNoise[0] -> 2_BinaryOpUGen:ABSOLUTE_DIFFERENCE[1:right]
                }

        Returns ugen graph.
        """
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_binary_op(
            self,
            expr,
            synthdeftools.BinaryOperator.ABSOLUTE_DIFFERENCE,
            )

    def amplitude_to_db(self):
        """
        Converts ugen graph from amplitude to decibels.

        ..  container:: example

            ::

                >>> ugen_graph = ugentools.WhiteNoise.ar()
                >>> result = ugen_graph.amplitude_to_db()

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
                SynthDef ... {
                    0_WhiteNoise[0] -> 1_UnaryOpUGen:AMPLITUDE_TO_DB[0:source]
                }

        Returns ugen graph.
        """
        from supriya import synthdeftools
        return self._compute_unary_op(
            self,
            synthdeftools.UnaryOperator.AMPLITUDE_TO_DB,
            )

    def ceiling(self):
        """
        Calculates the ceiling of ugen graph.

        ::

            >>> source = ugentools.DC.ar(source=0.5)
            >>> operation = source.ceiling()
            >>> print(operation)
            SynthDef ... {
                const_0:0.5 -> 0_DC[0:source]
                0_DC[0] -> 1_UnaryOpUGen:CEILING[0:source]
            }

        Returns ugen graph.
        """
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            self,
            synthdeftools.UnaryOperator.CEILING,
            )

    def clip(self, minimum, maximum):
        """
        Clips ugen graph.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = ugentools.WhiteNoise.ar()
                >>> result = ugen_graph.clip(-0.25, 0.25)

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
                SynthDef ... {
                    0_WhiteNoise[0] -> 1_Clip[0:source]
                    const_0:-0.25 -> 1_Clip[1:minimum]
                    const_1:0.25 -> 1_Clip[2:maximum]
                }

        ..  container:: example

            **Example 2:**

            ::

                >>> ugen_graph = ugentools.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ...     )
                >>> result = ugen_graph.clip(-0.25, 0.25)

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
                SynthDef ... {
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

        """
        from supriya.tools import ugentools
        return self._compute_ugen_map(
            ugentools.Clip,
            minimum=minimum,
            maximum=maximum,
            )

    def cubed(self):
        """
        Calculates the cube of ugen graph.

        ::

            >>> source = ugentools.DC.ar(source=0.5)
            >>> operation = source.cubed()
            >>> print(operation)
            SynthDef ... {
                const_0:0.5 -> 0_DC[0:source]
                0_DC[0] -> 1_UnaryOpUGen:CUBED[0:source]
            }

        Returns ugen graph.
        """
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            self,
            synthdeftools.UnaryOperator.CUBED,
            )

    def db_to_amplitude(self):
        """
        Converts ugen graph from decibels to amplitude.

        ..  container:: example

            ::

                >>> ugen_graph = ugentools.WhiteNoise.ar()
                >>> result = ugen_graph.db_to_amplitude()

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
                SynthDef ... {
                    0_WhiteNoise[0] -> 1_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
                }

        Returns ugen graph.
        """
        from supriya import synthdeftools
        return self._compute_unary_op(
            self,
            synthdeftools.UnaryOperator.DB_TO_AMPLITUDE,
            )

    def distort(self):
        """
        Distorts ugen graph non-linearly.

        ::

            >>> source = ugentools.DC.ar(source=0.5)
            >>> operation = source.distort()
            >>> print(operation)
            SynthDef ... {
                const_0:0.5 -> 0_DC[0:source]
                0_DC[0] -> 1_UnaryOpUGen:DISTORT[0:source]
            }

        Returns ugen graph.
        """
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            self,
            synthdeftools.UnaryOperator.DISTORT,
            )

    def exponential(self):
        """
        Calculates the natural exponential function of ugen graph.

        ::

            >>> source = ugentools.DC.ar(source=0.5)
            >>> operation = source.exponential()
            >>> print(operation)
            SynthDef ... {
                const_0:0.5 -> 0_DC[0:source]
                0_DC[0] -> 1_UnaryOpUGen:EXPONENTIAL[0:source]
            }

        Returns ugen graph.
        """
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            self,
            synthdeftools.UnaryOperator.EXPONENTIAL,
            )

    def floor(self):
        """
        Calculates the floor of ugen graph.

        ::

            >>> source = ugentools.DC.ar(source=0.5)
            >>> operation = source.floor()
            >>> print(operation)
            SynthDef ... {
                const_0:0.5 -> 0_DC[0:source]
                0_DC[0] -> 1_UnaryOpUGen:FLOOR[0:source]
            }

        Returns ugen graph.
        """
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            self,
            synthdeftools.UnaryOperator.FLOOR,
            )

    def fractional_part(self):
        """
        Calculates the fraction part of ugen graph.

        ::

            >>> source = ugentools.DC.ar(source=0.5)
            >>> operation = source.fractional_part()
            >>> print(operation)
            SynthDef ... {
                const_0:0.5 -> 0_DC[0:source]
                0_DC[0] -> 1_UnaryOpUGen:FRACTIONAL_PART[0:source]
            }

        Returns ugen graph.
        """
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            self,
            synthdeftools.UnaryOperator.FRACTIONAL_PART,
            )

    def hanning_window(self):
        """
        Calculates Hanning-window of ugen graph.

        ..  container:: example

            ::

                >>> ugen_graph = ugentools.LFNoise2.ar()
                >>> result = ugen_graph.hanning_window()

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
                SynthDef ... {
                    const_0:500.0 -> 0_LFNoise2[0:frequency]
                    0_LFNoise2[0] -> 1_UnaryOpUGen:HANNING_WINDOW[0:source]
                }

        Returns ugen graph.
        """
        from supriya import synthdeftools
        return self._compute_unary_op(
            self,
            synthdeftools.UnaryOperator.HANNING_WINDOW
            )

    def hz_to_midi(self):
        """
        Converts ugen graph from Hertz to midi note number.

        ..  container:: example

            ::

                >>> ugen_graph = ugentools.WhiteNoise.ar()
                >>> result = ugen_graph.hz_to_midi()

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
                SynthDef ... {
                    0_WhiteNoise[0] -> 1_UnaryOpUGen:HZ_TO_MIDI[0:source]
                }

        Returns ugen graph.
        """
        from supriya import synthdeftools
        return self._compute_unary_op(
            self,
            synthdeftools.UnaryOperator.HZ_TO_MIDI,
            )

    def hz_to_octave(self):
        """
        Converts ugen graph from Hertz to octave number.

        ..  container:: example

            ::

                >>> ugen_graph = ugentools.WhiteNoise.ar()
                >>> result = ugen_graph.hz_to_octave()

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
                SynthDef ... {
                    0_WhiteNoise[0] -> 1_UnaryOpUGen:HZ_TO_OCTAVE[0:source]
                }

        Returns ugen graph.
        """
        from supriya import synthdeftools
        return self._compute_unary_op(
            self,
            synthdeftools.UnaryOperator.HZ_TO_OCTAVE,
            )

    def is_equal_to(self, expr):
        """
        Calculates equality between ugen graph and `expr`.

        ::

            >>> left = ugentools.SinOsc.ar()
            >>> right = ugentools.WhiteNoise.kr()
            >>> operation = left.is_equal_to(right)
            >>> print(operation)
            SynthDef ... {
                const_0:440.0 -> 0_SinOsc[0:frequency]
                const_1:0.0 -> 0_SinOsc[1:phase]
                0_SinOsc[0] -> 2_BinaryOpUGen:EQUAL[0:left]
                1_WhiteNoise[0] -> 2_BinaryOpUGen:EQUAL[1:right]
            }

        Returns ugen graph.
        """
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_binary_op(
            self,
            expr,
            synthdeftools.BinaryOperator.EQUAL,
            )

    def is_not_equal_to(self, expr):
        """
        Calculates inequality between ugen graph and `expr`.

        ::

            >>> left = ugentools.SinOsc.ar()
            >>> right = ugentools.WhiteNoise.kr()
            >>> operation = left.is_not_equal_to(right)
            >>> print(operation)
            SynthDef ... {
                const_0:440.0 -> 0_SinOsc[0:frequency]
                const_1:0.0 -> 0_SinOsc[1:phase]
                0_SinOsc[0] -> 2_BinaryOpUGen:NOT_EQUAL[0:left]
                1_WhiteNoise[0] -> 2_BinaryOpUGen:NOT_EQUAL[1:right]
            }

        Returns ugen graph.
        """
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_binary_op(
            self,
            expr,
            synthdeftools.BinaryOperator.NOT_EQUAL,
            )

    def lag(
        self,
        lag_time=0.5,
        ):
        """
        Lags ugen graph.

        ..  container:: example

            ::

                >>> ugen_graph = ugentools.WhiteNoise.ar()
                >>> result = ugen_graph.lag(0.5)

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
                SynthDef ... {
                    0_WhiteNoise[0] -> 1_Lag[0:source]
                    const_0:0.5 -> 1_Lag[1:lag_time]
                }

        ..  container:: example

            ::

                >>> ugen_graph = ugentools.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ...     )
                >>> result = ugen_graph.lag(0.5)

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
                SynthDef ... {
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

        """
        from supriya.tools import ugentools
        return self._compute_ugen_map(
            ugentools.Lag,
            lag_time=lag_time,
            )

    def log(self):
        """
        Calculates the natural logarithm of ugen graph.

        ::

            >>> source = ugentools.DC.ar(source=0.5)
            >>> operation = source.log()
            >>> print(operation)
            SynthDef ... {
                const_0:0.5 -> 0_DC[0:source]
                0_DC[0] -> 1_UnaryOpUGen:LOG[0:source]
            }

        Returns ugen graph.
        """
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            self,
            synthdeftools.UnaryOperator.LOG,
            )

    def log2(self):
        """
        Calculates the base-2 logarithm of ugen graph.

        ::

            >>> source = ugentools.DC.ar(source=0.5)
            >>> operation = source.log2()
            >>> print(operation)
            SynthDef ... {
                const_0:0.5 -> 0_DC[0:source]
                0_DC[0] -> 1_UnaryOpUGen:LOG2[0:source]
            }

        Returns ugen graph.
        """
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            self,
            synthdeftools.UnaryOperator.LOG2,
            )

    def log10(self):
        """
        Calculates the base-10 logarithm of ugen graph.

        ::

            >>> source = ugentools.DC.ar(source=0.5)
            >>> operation = source.log10()
            >>> print(operation)
            SynthDef ... {
                const_0:0.5 -> 0_DC[0:source]
                0_DC[0] -> 1_UnaryOpUGen:LOG10[0:source]
            }

        Returns ugen graph.
        """
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            self,
            synthdeftools.UnaryOperator.LOG10,
            )

    def maximum(self, expr):
        """
        Calculates maximum between ugen graph and `expr`.

        ::

            >>> left = ugentools.SinOsc.ar()
            >>> right = ugentools.WhiteNoise.kr()
            >>> operation = left.maximum(right)
            >>> print(operation)
            SynthDef ... {
                const_0:440.0 -> 0_SinOsc[0:frequency]
                const_1:0.0 -> 0_SinOsc[1:phase]
                0_SinOsc[0] -> 2_BinaryOpUGen:MAXIMUM[0:left]
                1_WhiteNoise[0] -> 2_BinaryOpUGen:MAXIMUM[1:right]
            }

        Returns ugen graph.
        """
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_binary_op(
            self,
            expr,
            synthdeftools.BinaryOperator.MAXIMUM,
            )

    def midi_to_hz(self):
        """
        Converts ugen graph from midi note number to Hertz.

        ..  container:: example

            ::

                >>> ugen_graph = ugentools.WhiteNoise.ar()
                >>> result = ugen_graph.midi_to_hz()

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
                SynthDef ... {
                    0_WhiteNoise[0] -> 1_UnaryOpUGen:MIDI_TO_HZ[0:source]
                }

        Returns ugen graph.
        """
        from supriya import synthdeftools
        return self._compute_unary_op(
            self,
            synthdeftools.UnaryOperator.MIDI_TO_HZ,
            )

    def minimum(self, expr):
        """
        Calculates minimum between ugen graph and `expr`.

        ::

            >>> left = ugentools.SinOsc.ar()
            >>> right = ugentools.WhiteNoise.kr()
            >>> operation = left.minimum(right)
            >>> print(operation)
            SynthDef f80c0a7b300911e9eff0e8760f5fab18 {
                const_0:440.0 -> 0_SinOsc[0:frequency]
                const_1:0.0 -> 0_SinOsc[1:phase]
                0_SinOsc[0] -> 2_BinaryOpUGen:MINIMUM[0:left]
                1_WhiteNoise[0] -> 2_BinaryOpUGen:MINIMUM[1:right]
            }

        Returns ugen graph.
        """
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_binary_op(
            self,
            expr,
            synthdeftools.BinaryOperator.MINIMUM,
            )

    def octave_to_hz(self):
        """
        Converts ugen graph from octave number to Hertz.

        ..  container:: example

            ::

                >>> ugen_graph = ugentools.WhiteNoise.ar()
                >>> result = ugen_graph.octave_to_hz()

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
                SynthDef ... {
                    0_WhiteNoise[0] -> 1_UnaryOpUGen:OCTAVE_TO_HZ[0:source]
                }

        Returns ugen graph.
        """
        from supriya import synthdeftools
        return self._compute_unary_op(
            self,
            synthdeftools.UnaryOperator.OCTAVE_TO_HZ,
            )

    def power(self, expr):
        """
        Raises ugen graph to the power of `expr`.

        ::

            >>> left = ugentools.SinOsc.ar()
            >>> right = ugentools.WhiteNoise.kr()
            >>> operation = left.power(right)
            >>> print(operation)
            SynthDef ... {
                const_0:440.0 -> 0_SinOsc[0:frequency]
                const_1:0.0 -> 0_SinOsc[1:phase]
                0_SinOsc[0] -> 2_BinaryOpUGen:POWER[0:left]
                1_WhiteNoise[0] -> 2_BinaryOpUGen:POWER[1:right]
            }

        Returns ugen graph.
        """
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_binary_op(
            self,
            expr,
            synthdeftools.BinaryOperator.POWER,
            )

    def ratio_to_semitones(self):
        """
        Converts ugen graph from frequency ratio to semitone distance.

        ..  container:: example

            ::

                >>> ugen_graph = ugentools.WhiteNoise.ar()
                >>> result = ugen_graph.ratio_to_semitones()

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
                SynthDef ... {
                    0_WhiteNoise[0] -> 1_UnaryOpUGen:RATIO_TO_SEMITONES[0:source]
                }

        Returns ugen graph.
        """
        from supriya import synthdeftools
        return self._compute_unary_op(
            self,
            synthdeftools.UnaryOperator.RATIO_TO_SEMITONES,
            )

    def rectangle_window(self):
        """
        Calculates rectangle-window of ugen graph.

        ..  container:: example

            ::

                >>> ugen_graph = ugentools.LFNoise2.ar()
                >>> result = ugen_graph.rectangle_window()

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
                SynthDef ... {
                    const_0:500.0 -> 0_LFNoise2[0:frequency]
                    0_LFNoise2[0] -> 1_UnaryOpUGen:RECTANGLE_WINDOW[0:source]
                }

        Returns ugen graph.
        """
        from supriya import synthdeftools
        return self._compute_unary_op(
            self,
            synthdeftools.UnaryOperator.RECTANGLE_WINDOW
            )

    def reciprocal(self):
        """
        Calculates reciprocal of ugen graph.

        ..  container:: example

            ::

                >>> ugen_graph = ugentools.LFNoise2.ar()
                >>> result = ugen_graph.reciprocal()

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
                SynthDef ... {
                    const_0:500.0 -> 0_LFNoise2[0:frequency]
                    0_LFNoise2[0] -> 1_UnaryOpUGen:RECIPROCAL[0:source]
                }

        Returns ugen graph.
        """
        from supriya import synthdeftools
        return self._compute_unary_op(
            self,
            synthdeftools.UnaryOperator.RECIPROCAL
            )

    def s_curve(self):
        """
        Calculates S-curve of ugen graph.

        ..  container:: example

            ::

                >>> ugen_graph = ugentools.LFNoise2.ar()
                >>> result = ugen_graph.s_curve()

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
                SynthDef ... {
                    const_0:500.0 -> 0_LFNoise2[0:frequency]
                    0_LFNoise2[0] -> 1_UnaryOpUGen:S_CURVE[0:source]
                }

        Returns ugen graph.
        """
        from supriya import synthdeftools
        return self._compute_unary_op(
            self,
            synthdeftools.UnaryOperator.S_CURVE
            )

    def scale(
        self,
        input_minimum,
        input_maximum,
        output_minimum,
        output_maximum,
        exponential=False,
        ):
        """
        Scales ugen graph from `input_minimum` and `input_maximum` to
        `output_minimum` and `output_maximum`.

        ..  container:: example

            ::

                >>> ugen_graph = ugentools.WhiteNoise.ar()
                >>> result = ugen_graph.scale(-1, 1, 0.5, 0.75)

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
                SynthDef ... {
                    0_WhiteNoise[0] -> 1_MulAdd[0:source]
                    const_0:0.125 -> 1_MulAdd[1:multiplier]
                    const_1:0.625 -> 1_MulAdd[2:addend]
                }

        ..  container:: example

            ::

                >>> ugen_graph = ugentools.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ...     )
                >>> result = ugen_graph.scale(-1, 1, 0.5, 0.75, exponential=True)

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
                SynthDef ... {
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

        """
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

    def semitones_to_ratio(self):
        """
        Converts ugen graph from semitone distance to frequency ratio.

        ..  container:: example

            ::

                >>> ugen_graph = ugentools.WhiteNoise.ar()
                >>> result = ugen_graph.semitones_to_ratio()

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
                SynthDef ... {
                    0_WhiteNoise[0] -> 1_UnaryOpUGen:SEMITONES_TO_RATIO[0:source]
                }

        Returns ugen graph.
        """
        from supriya import synthdeftools
        return self._compute_unary_op(
            self,
            synthdeftools.UnaryOperator.SEMITONES_TO_RATIO,
            )

    def sign(self):
        """
        Calculates sign of ugen graph.

        ..  container:: example

            ::

                >>> ugen_graph = ugentools.LFNoise2.ar()
                >>> result = ugen_graph.sign()

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
                SynthDef ... {
                    const_0:500.0 -> 0_LFNoise2[0:frequency]
                    0_LFNoise2[0] -> 1_UnaryOpUGen:SIGN[0:source]
                }

        Returns ugen graph.
        """
        from supriya import synthdeftools
        return self._compute_unary_op(
            self,
            synthdeftools.UnaryOperator.SIGN
            )

    def softclip(self):
        """
        Distorts ugen graph non-linearly.
        """
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            self,
            synthdeftools.UnaryOperator.SOFTCLIP,
            )

    def square_root(self):
        """
        Calculates square root of ugen graph.
        """
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            self,
            synthdeftools.UnaryOperator.SQUARE_ROOT,
            )

    def squared(self):
        """
        Calculates square of ugen graph.
        """
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            self,
            synthdeftools.UnaryOperator.SQUARED,
            )

    def sum(self):
        """
        Sums ugen graph.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = ugentools.LFNoise2.ar()
                >>> result = ugen_graph.sum()

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
                SynthDef ... {
                    const_0:500.0 -> 0_LFNoise2[0:frequency]
                }

        ..  container:: example

            **Example 2:**

            ::

                >>> ugen_graph = ugentools.SinOsc.ar([440, 442, 443])
                >>> result = ugen_graph.sum()

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
                SynthDef ... {
                    const_0:440.0 -> 0_SinOsc[0:frequency]
                    const_1:0.0 -> 0_SinOsc[1:phase]
                    const_2:442.0 -> 1_SinOsc[0:frequency]
                    const_1:0.0 -> 1_SinOsc[1:phase]
                    const_3:443.0 -> 2_SinOsc[0:frequency]
                    const_1:0.0 -> 2_SinOsc[1:phase]
                    0_SinOsc[0] -> 3_Sum3[0:input_one]
                    1_SinOsc[0] -> 3_Sum3[1:input_two]
                    2_SinOsc[0] -> 3_Sum3[2:input_three]
                }

        Returns ugen graph.
        """
        from supriya.tools import ugentools
        return ugentools.Mix.new(self)

    def tanh(self):
        """
        Calculates hyperbolic tangent of ugen graph.

        ..  container:: example

            ::

                >>> ugen_graph = ugentools.LFNoise2.ar()
                >>> result = ugen_graph.tanh()

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
                SynthDef ... {
                    const_0:500.0 -> 0_LFNoise2[0:frequency]
                    0_LFNoise2[0] -> 1_UnaryOpUGen:TANH[0:source]
                }

        Returns ugen graph.
        """
        from supriya import synthdeftools
        return self._compute_unary_op(
            self,
            synthdeftools.UnaryOperator.TANH
            )

    def transpose(self, semitones):
        """
        Transposes ugen graph by `semitones`.

        ..  container:: example

            ::

                >>> ugen_graph = ugentools.LFNoise2.ar()
                >>> result = ugen_graph.transpose([0, 3, 7])

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
                SynthDef ... {
                    const_0:500.0 -> 0_LFNoise2[0:frequency]
                    0_LFNoise2[0] -> 1_UnaryOpUGen:HZ_TO_MIDI[0:source]
                    1_UnaryOpUGen:HZ_TO_MIDI[0] -> 2_UnaryOpUGen:MIDI_TO_HZ[0:source]
                    1_UnaryOpUGen:HZ_TO_MIDI[0] -> 3_BinaryOpUGen:ADDITION[0:left]
                    const_1:3.0 -> 3_BinaryOpUGen:ADDITION[1:right]
                    3_BinaryOpUGen:ADDITION[0] -> 4_UnaryOpUGen:MIDI_TO_HZ[0:source]
                    1_UnaryOpUGen:HZ_TO_MIDI[0] -> 5_BinaryOpUGen:ADDITION[0:left]
                    const_2:7.0 -> 5_BinaryOpUGen:ADDITION[1:right]
                    5_BinaryOpUGen:ADDITION[0] -> 6_UnaryOpUGen:MIDI_TO_HZ[0:source]
                }

        Returns ugen graph.
        """
        return (self.hz_to_midi() + semitones).midi_to_hz()

    def triangle_window(self):
        """
        Calculates triangle-window of ugen graph.

        ..  container:: example

            ::

                >>> ugen_graph = ugentools.LFNoise2.ar()
                >>> result = ugen_graph.triangle_window()

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
                SynthDef ... {
                    const_0:500.0 -> 0_LFNoise2[0:frequency]
                    0_LFNoise2[0] -> 1_UnaryOpUGen:TRIANGLE_WINDOW[0:source]
                }

        Returns ugen graph.
        """
        from supriya import synthdeftools
        return self._compute_unary_op(
            self,
            synthdeftools.UnaryOperator.TRIANGLE_WINDOW
            )

    def welch_window(self):
        """
        Calculates Welch-window of ugen graph.

        ..  container:: example

            ::

                >>> ugen_graph = ugentools.LFNoise2.ar()
                >>> result = ugen_graph.welch_window()

            ::

                >>> graph(result)  # doctest: +SKIP

            ..  doctest::

                >>> print(result)
                SynthDef ... {
                    const_0:500.0 -> 0_LFNoise2[0:frequency]
                    0_LFNoise2[0] -> 1_UnaryOpUGen:WELCH_WINDOW[0:source]
                }

        Returns ugen graph.
        """
        from supriya import synthdeftools
        return self._compute_unary_op(
            self,
            synthdeftools.UnaryOperator.WELCH_WINDOW
            )
