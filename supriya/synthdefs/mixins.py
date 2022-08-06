import collections.abc
import copy

from supriya import BinaryOperator, SignalRange, UnaryOperator
from supriya.system import SupriyaObject


class UGenMethodMixin(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __abs__(self):
        """
        Gets absolute value of ugen graph.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.ar()
                >>> result = abs(ugen_graph)
                >>> result
                UnaryOpUGen.ar()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: f21696d155a2686700992f0e9a04a79c
                    ugens:
                    -   WhiteNoise.ar: null
                    -   UnaryOpUGen(ABSOLUTE_VALUE).ar:
                            source: WhiteNoise.ar[0]

        ..  container:: example

            **Example 2:**

            ::

                >>> ugen_graph = supriya.ugens.SinOsc.ar(
                ...     frequency=(440, 442, 443),
                ... )
                >>> result = abs(ugen_graph)
                >>> result
                UGenArray({3})

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 1d45df2f3d33d1b0641d2c464498f6c4
                    ugens:
                    -   SinOsc.ar/0:
                            frequency: 440.0
                            phase: 0.0
                    -   UnaryOpUGen(ABSOLUTE_VALUE).ar/0:
                            source: SinOsc.ar/0[0]
                    -   SinOsc.ar/1:
                            frequency: 442.0
                            phase: 0.0
                    -   UnaryOpUGen(ABSOLUTE_VALUE).ar/1:
                            source: SinOsc.ar/1[0]
                    -   SinOsc.ar/2:
                            frequency: 443.0
                            phase: 0.0
                    -   UnaryOpUGen(ABSOLUTE_VALUE).ar/2:
                            source: SinOsc.ar/2[0]

        Returns ugen graph.
        """
        return UGenMethodMixin._compute_unary_op(self, UnaryOperator.ABSOLUTE_VALUE)

    def __add__(self, expr):
        """
        Adds `expr` to ugen graph.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar()
                >>> result = ugen_graph + expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 6bf4339326d015532b7604cd7af9ad3b
                    ugens:
                    -   WhiteNoise.kr: null
                    -   SinOsc.ar:
                            frequency: 440.0
                            phase: 0.0
                    -   BinaryOpUGen(ADDITION).ar:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar[0]

        ..  container:: example

            **Example 2:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ... )
                >>> result = ugen_graph + expr
                >>> result
                UGenArray({3})

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: f4a3c1ed35cc5f6fe66b70a3bc520b10
                    ugens:
                    -   WhiteNoise.kr: null
                    -   SinOsc.ar/0:
                            frequency: 440.0
                            phase: 0.0
                    -   BinaryOpUGen(ADDITION).ar/0:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar/0[0]
                    -   SinOsc.ar/1:
                            frequency: 442.0
                            phase: 0.0
                    -   BinaryOpUGen(ADDITION).ar/1:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar/1[0]
                    -   SinOsc.ar/2:
                            frequency: 443.0
                            phase: 0.0
                    -   BinaryOpUGen(ADDITION).ar/2:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar/2[0]

        ..  container:: example

            **Example 3:**

            ::

                >>> ugen_graph = supriya.ugens.Dust.ar(
                ...     density=11.5,
                ... )
                >>> expr = 4
                >>> result = ugen_graph + expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: f79088cc154ef2b65c72a0f8de8336ce
                    ugens:
                    -   Dust.ar:
                            density: 11.5
                    -   BinaryOpUGen(ADDITION).ar:
                            left: Dust.ar[0]
                            right: 4.0

        Returns ugen graph.
        """
        return UGenMethodMixin._compute_binary_op(self, expr, BinaryOperator.ADDITION)

    def __div__(self, expr):
        """
        Divides ugen graph by `expr`.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar()
                >>> result = ugen_graph / expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 6da024a346859242c441fe03326d2adc
                    ugens:
                    -   WhiteNoise.kr: null
                    -   SinOsc.ar:
                            frequency: 440.0
                            phase: 0.0
                    -   BinaryOpUGen(FLOAT_DIVISION).ar:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar[0]

        ..  container:: example

            **Example 2:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ... )
                >>> result = ugen_graph / expr
                >>> result
                UGenArray({3})

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: be20d589dfccb721f56da8b002d86763
                    ugens:
                    -   WhiteNoise.kr: null
                    -   SinOsc.ar/0:
                            frequency: 440.0
                            phase: 0.0
                    -   BinaryOpUGen(FLOAT_DIVISION).ar/0:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar/0[0]
                    -   SinOsc.ar/1:
                            frequency: 442.0
                            phase: 0.0
                    -   BinaryOpUGen(FLOAT_DIVISION).ar/1:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar/1[0]
                    -   SinOsc.ar/2:
                            frequency: 443.0
                            phase: 0.0
                    -   BinaryOpUGen(FLOAT_DIVISION).ar/2:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar/2[0]

        ..  container:: example

            **Example 3:**

            ::

                >>> ugen_graph = supriya.ugens.Dust.ar(
                ...     density=11.5,
                ... )
                >>> expr = 4
                >>> result = ugen_graph / expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 672765c596fcaa083186b2f2b996ba1d
                    ugens:
                    -   Dust.ar:
                            density: 11.5
                    -   BinaryOpUGen(FLOAT_DIVISION).ar:
                            left: Dust.ar[0]
                            right: 4.0

        Returns ugen graph.
        """
        return UGenMethodMixin._compute_binary_op(
            self, expr, BinaryOperator.FLOAT_DIVISION
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

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar()
                >>> result = ugen_graph >= expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 9db96233abf1f610d027ff285691482d
                    ugens:
                    -   WhiteNoise.kr: null
                    -   SinOsc.ar:
                            frequency: 440.0
                            phase: 0.0
                    -   BinaryOpUGen(GREATER_THAN_OR_EQUAL).ar:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar[0]

        ..  container:: example

            **Example 2:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ... )
                >>> result = ugen_graph >= expr
                >>> result
                UGenArray({3})

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 6d43342b3787aa11a46cea54412407e1
                    ugens:
                    -   WhiteNoise.kr: null
                    -   SinOsc.ar/0:
                            frequency: 440.0
                            phase: 0.0
                    -   BinaryOpUGen(GREATER_THAN_OR_EQUAL).ar/0:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar/0[0]
                    -   SinOsc.ar/1:
                            frequency: 442.0
                            phase: 0.0
                    -   BinaryOpUGen(GREATER_THAN_OR_EQUAL).ar/1:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar/1[0]
                    -   SinOsc.ar/2:
                            frequency: 443.0
                            phase: 0.0
                    -   BinaryOpUGen(GREATER_THAN_OR_EQUAL).ar/2:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar/2[0]

        ..  container:: example

            **Example 3:**

            ::

                >>> ugen_graph = supriya.ugens.Dust.ar(
                ...     density=11.5,
                ... )
                >>> expr = 4
                >>> result = ugen_graph >= expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: b06931195bab8e6f6ca2e3a857e71a95
                    ugens:
                    -   Dust.ar:
                            density: 11.5
                    -   BinaryOpUGen(GREATER_THAN_OR_EQUAL).ar:
                            left: Dust.ar[0]
                            right: 4.0

        Returns ugen graph.
        """
        return UGenMethodMixin._compute_binary_op(
            self, expr, BinaryOperator.GREATER_THAN_OR_EQUAL
        )

    def __gt__(self, expr):
        """
        Tests if ugen graph if greater than `expr`.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar()
                >>> result = ugen_graph > expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 01bebf935112af62ffdd282a99581904
                    ugens:
                    -   WhiteNoise.kr: null
                    -   SinOsc.ar:
                            frequency: 440.0
                            phase: 0.0
                    -   BinaryOpUGen(GREATER_THAN).ar:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar[0]

        ..  container:: example

            **Example 2:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ... )
                >>> result = ugen_graph > expr
                >>> result
                UGenArray({3})

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 55642179864ad927e9d5cf6358367677
                    ugens:
                    -   WhiteNoise.kr: null
                    -   SinOsc.ar/0:
                            frequency: 440.0
                            phase: 0.0
                    -   BinaryOpUGen(GREATER_THAN).ar/0:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar/0[0]
                    -   SinOsc.ar/1:
                            frequency: 442.0
                            phase: 0.0
                    -   BinaryOpUGen(GREATER_THAN).ar/1:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar/1[0]
                    -   SinOsc.ar/2:
                            frequency: 443.0
                            phase: 0.0
                    -   BinaryOpUGen(GREATER_THAN).ar/2:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar/2[0]

        ..  container:: example

            **Example 3:**

            ::

                >>> ugen_graph = supriya.ugens.Dust.ar(
                ...     density=11.5,
                ... )
                >>> expr = 4
                >>> result = ugen_graph > expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 5177e03443ad31ee2664aae2201fb979
                    ugens:
                    -   Dust.ar:
                            density: 11.5
                    -   BinaryOpUGen(GREATER_THAN).ar:
                            left: Dust.ar[0]
                            right: 4.0

        Returns ugen graph.
        """
        return UGenMethodMixin._compute_binary_op(
            self, expr, BinaryOperator.GREATER_THAN
        )

    def __le__(self, expr):
        """
        Tests if ugen graph if less than or equal to `expr`.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar()
                >>> result = ugen_graph <= expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: fefc06cbbc3babb35046306c6d41e3c5
                    ugens:
                    -   WhiteNoise.kr: null
                    -   SinOsc.ar:
                            frequency: 440.0
                            phase: 0.0
                    -   BinaryOpUGen(LESS_THAN_OR_EQUAL).ar:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar[0]

        ..  container:: example

            **Example 2:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ... )
                >>> result = ugen_graph <= expr
                >>> result
                UGenArray({3})

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 53f29d793fd676fbca1d541e938b66ca
                    ugens:
                    -   WhiteNoise.kr: null
                    -   SinOsc.ar/0:
                            frequency: 440.0
                            phase: 0.0
                    -   BinaryOpUGen(LESS_THAN_OR_EQUAL).ar/0:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar/0[0]
                    -   SinOsc.ar/1:
                            frequency: 442.0
                            phase: 0.0
                    -   BinaryOpUGen(LESS_THAN_OR_EQUAL).ar/1:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar/1[0]
                    -   SinOsc.ar/2:
                            frequency: 443.0
                            phase: 0.0
                    -   BinaryOpUGen(LESS_THAN_OR_EQUAL).ar/2:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar/2[0]

        ..  container:: example

            **Example 3:**

            ::

                >>> ugen_graph = supriya.ugens.Dust.ar(
                ...     density=11.5,
                ... )
                >>> expr = 4
                >>> result = ugen_graph <= expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 3cf0414af96d130edf2e1b839f73036c
                    ugens:
                    -   Dust.ar:
                            density: 11.5
                    -   BinaryOpUGen(LESS_THAN_OR_EQUAL).ar:
                            left: Dust.ar[0]
                            right: 4.0

        Returns ugen graph.
        """
        return UGenMethodMixin._compute_binary_op(
            self, expr, BinaryOperator.LESS_THAN_OR_EQUAL
        )

    def __lt__(self, expr):
        """
        Tests if ugen graph if less than `expr`.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar()
                >>> result = ugen_graph < expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 844f34c0ffb28ecc24bd5cf0bae20b43
                    ugens:
                    -   WhiteNoise.kr: null
                    -   SinOsc.ar:
                            frequency: 440.0
                            phase: 0.0
                    -   BinaryOpUGen(LESS_THAN).ar:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar[0]

        ..  container:: example

            **Example 2:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ... )
                >>> result = ugen_graph < expr
                >>> result
                UGenArray({3})

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 14c1494fe4e153e690a8ef0a42e5834f
                    ugens:
                    -   WhiteNoise.kr: null
                    -   SinOsc.ar/0:
                            frequency: 440.0
                            phase: 0.0
                    -   BinaryOpUGen(LESS_THAN).ar/0:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar/0[0]
                    -   SinOsc.ar/1:
                            frequency: 442.0
                            phase: 0.0
                    -   BinaryOpUGen(LESS_THAN).ar/1:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar/1[0]
                    -   SinOsc.ar/2:
                            frequency: 443.0
                            phase: 0.0
                    -   BinaryOpUGen(LESS_THAN).ar/2:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar/2[0]

        ..  container:: example

            **Example 3:**

            ::

                >>> ugen_graph = supriya.ugens.Dust.ar(
                ...     density=11.5,
                ... )
                >>> expr = 4
                >>> result = ugen_graph < expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: e87d41791847aa80d8a3e56318e506e4
                    ugens:
                    -   Dust.ar:
                            density: 11.5
                    -   BinaryOpUGen(LESS_THAN).ar:
                            left: Dust.ar[0]
                            right: 4.0

        Returns ugen graph.
        """
        return UGenMethodMixin._compute_binary_op(self, expr, BinaryOperator.LESS_THAN)

    def __mod__(self, expr):
        """
        Gets modulo of ugen graph and `expr`.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar()
                >>> result = ugen_graph % expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: e4a06e157474f8d1ae213916f3cf585a
                    ugens:
                    -   WhiteNoise.kr: null
                    -   SinOsc.ar:
                            frequency: 440.0
                            phase: 0.0
                    -   BinaryOpUGen(MODULO).ar:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar[0]

        ..  container:: example

            **Example 2:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ... )
                >>> result = ugen_graph % expr
                >>> result
                UGenArray({3})

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 90badce1cf8fc1752b5eb99b29122a14
                    ugens:
                    -   WhiteNoise.kr: null
                    -   SinOsc.ar/0:
                            frequency: 440.0
                            phase: 0.0
                    -   BinaryOpUGen(MODULO).ar/0:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar/0[0]
                    -   SinOsc.ar/1:
                            frequency: 442.0
                            phase: 0.0
                    -   BinaryOpUGen(MODULO).ar/1:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar/1[0]
                    -   SinOsc.ar/2:
                            frequency: 443.0
                            phase: 0.0
                    -   BinaryOpUGen(MODULO).ar/2:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar/2[0]

        ..  container:: example

            **Example 3:**

            ::

                >>> ugen_graph = supriya.ugens.Dust.ar(
                ...     density=11.5,
                ... )
                >>> expr = 4
                >>> result = ugen_graph % expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: bfa60877061daf112516cc3ec8c7ff69
                    ugens:
                    -   Dust.ar:
                            density: 11.5
                    -   BinaryOpUGen(MODULO).ar:
                            left: Dust.ar[0]
                            right: 4.0

        Returns ugen graph.
        """
        return UGenMethodMixin._compute_binary_op(self, expr, BinaryOperator.MODULO)

    def __mul__(self, expr):
        """
        Multiplies ugen graph by `expr`.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar()
                >>> result = ugen_graph * expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: ea2b5e5cec4e2d5a1bef0a8dda522bd3
                    ugens:
                    -   WhiteNoise.kr: null
                    -   SinOsc.ar:
                            frequency: 440.0
                            phase: 0.0
                    -   BinaryOpUGen(MULTIPLICATION).ar:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar[0]

        ..  container:: example

            **Example 2:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ... )
                >>> result = ugen_graph * expr
                >>> result
                UGenArray({3})

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 9d353c198344b6be3635244197bc2a4b
                    ugens:
                    -   WhiteNoise.kr: null
                    -   SinOsc.ar/0:
                            frequency: 440.0
                            phase: 0.0
                    -   BinaryOpUGen(MULTIPLICATION).ar/0:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar/0[0]
                    -   SinOsc.ar/1:
                            frequency: 442.0
                            phase: 0.0
                    -   BinaryOpUGen(MULTIPLICATION).ar/1:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar/1[0]
                    -   SinOsc.ar/2:
                            frequency: 443.0
                            phase: 0.0
                    -   BinaryOpUGen(MULTIPLICATION).ar/2:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar/2[0]

        ..  container:: example

            **Example 3:**

            ::

                >>> ugen_graph = supriya.ugens.Dust.ar(
                ...     density=11.5,
                ... )
                >>> expr = 4
                >>> result = ugen_graph * expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 1735acd4add428d8ab317d00236b0fe7
                    ugens:
                    -   Dust.ar:
                            density: 11.5
                    -   BinaryOpUGen(MULTIPLICATION).ar:
                            left: Dust.ar[0]
                            right: 4.0

        Returns ugen graph.
        """
        return UGenMethodMixin._compute_binary_op(
            self, expr, BinaryOperator.MULTIPLICATION
        )

    def __neg__(self):
        """
        Negates ugen graph.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.ar()
                >>> result = -ugen_graph
                >>> result
                UnaryOpUGen.ar()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: a987a13f0593e4e4e070acffb11d5c3e
                    ugens:
                    -   WhiteNoise.ar: null
                    -   UnaryOpUGen(NEGATIVE).ar:
                            source: WhiteNoise.ar[0]

        ..  container:: example

            **Example 2:**

            ::

                >>> ugen_graph = supriya.ugens.SinOsc.ar(
                ...     frequency=(440, 442, 443),
                ... )
                >>> result = -ugen_graph
                >>> result
                UGenArray({3})

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: e5dfc1d4ecb11ed8170aaf11469a6443
                    ugens:
                    -   SinOsc.ar/0:
                            frequency: 440.0
                            phase: 0.0
                    -   UnaryOpUGen(NEGATIVE).ar/0:
                            source: SinOsc.ar/0[0]
                    -   SinOsc.ar/1:
                            frequency: 442.0
                            phase: 0.0
                    -   UnaryOpUGen(NEGATIVE).ar/1:
                            source: SinOsc.ar/1[0]
                    -   SinOsc.ar/2:
                            frequency: 443.0
                            phase: 0.0
                    -   UnaryOpUGen(NEGATIVE).ar/2:
                            source: SinOsc.ar/2[0]

        Returns ugen graph.
        """
        return UGenMethodMixin._compute_unary_op(self, UnaryOperator.NEGATIVE)

    def __pow__(self, expr):
        """
        Raises ugen graph to the power of `expr`.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar()
                >>> result = ugen_graph ** expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 3498b370c0575fb2c2ed45143ba2da4f
                    ugens:
                    -   WhiteNoise.kr: null
                    -   SinOsc.ar:
                            frequency: 440.0
                            phase: 0.0
                    -   BinaryOpUGen(POWER).ar:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar[0]

        ..  container:: example

            **Example 2:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ... )
                >>> result = ugen_graph ** expr
                >>> result
                UGenArray({3})

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 04e78034682f9ffd6628fbfd09a28c13
                    ugens:
                    -   WhiteNoise.kr: null
                    -   SinOsc.ar/0:
                            frequency: 440.0
                            phase: 0.0
                    -   BinaryOpUGen(POWER).ar/0:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar/0[0]
                    -   SinOsc.ar/1:
                            frequency: 442.0
                            phase: 0.0
                    -   BinaryOpUGen(POWER).ar/1:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar/1[0]
                    -   SinOsc.ar/2:
                            frequency: 443.0
                            phase: 0.0
                    -   BinaryOpUGen(POWER).ar/2:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar/2[0]

        ..  container:: example

            **Example 3:**

            ::

                >>> ugen_graph = supriya.ugens.Dust.ar(
                ...     density=11.5,
                ... )
                >>> expr = 4
                >>> result = ugen_graph ** expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 50b8e3b154bc85c98d76ced493a32731
                    ugens:
                    -   Dust.ar:
                            density: 11.5
                    -   BinaryOpUGen(POWER).ar:
                            left: Dust.ar[0]
                            right: 4.0

        Returns ugen graph.
        """
        return UGenMethodMixin._compute_binary_op(self, expr, BinaryOperator.POWER)

    def __rpow__(self, expr):
        """
        Raises `expr` to the power of ugen graph.

        ..  container:: example

            **Example 1:**

            ::

                >>> expr = 1.5
                >>> ugen_graph = supriya.ugens.SinOsc.ar()
                >>> result = expr ** ugen_graph
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: c450618c9e0fe5213629275da4e5e354
                    ugens:
                    -   SinOsc.ar:
                            frequency: 440.0
                            phase: 0.0
                    -   BinaryOpUGen(POWER).ar:
                            left: 1.5
                            right: SinOsc.ar[0]

        ..  container:: example

            **Example 2:**

            ::

                >>> expr = [220, 330]
                >>> ugen_graph = supriya.ugens.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ... )
                >>> result = expr ** ugen_graph
                >>> result
                UGenArray({3})

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: a614dc68313ee7ca2677e63fd499de0d
                    ugens:
                    -   SinOsc.ar/0:
                            frequency: 440.0
                            phase: 0.0
                    -   BinaryOpUGen(POWER).ar/0:
                            left: 220.0
                            right: SinOsc.ar/0[0]
                    -   SinOsc.ar/1:
                            frequency: 442.0
                            phase: 0.0
                    -   BinaryOpUGen(POWER).ar/1:
                            left: 330.0
                            right: SinOsc.ar/1[0]
                    -   SinOsc.ar/2:
                            frequency: 443.0
                            phase: 0.0
                    -   BinaryOpUGen(POWER).ar/2:
                            left: 220.0
                            right: SinOsc.ar/2[0]

        Returns ugen graph.
        """
        return UGenMethodMixin._compute_binary_op(expr, self, BinaryOperator.POWER)

    def __radd__(self, expr):
        """
        Adds ugen graph to `expr`.

        ..  container:: example

            **Example 1:**

            ::

                >>> expr = 1.5
                >>> ugen_graph = supriya.ugens.SinOsc.ar()
                >>> result = expr + ugen_graph
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: bb0592fad58b0bfa1a403c7ff6a400f3
                    ugens:
                    -   SinOsc.ar:
                            frequency: 440.0
                            phase: 0.0
                    -   BinaryOpUGen(ADDITION).ar:
                            left: 1.5
                            right: SinOsc.ar[0]

        ..  container:: example

            **Example 2:**

            ::

                >>> expr = [220, 330]
                >>> ugen_graph = supriya.ugens.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ... )
                >>> result = expr + ugen_graph
                >>> result
                UGenArray({3})

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 0ad0a3d4b7ddf8bb56807813efc62202
                    ugens:
                    -   SinOsc.ar/0:
                            frequency: 440.0
                            phase: 0.0
                    -   BinaryOpUGen(ADDITION).ar/0:
                            left: 220.0
                            right: SinOsc.ar/0[0]
                    -   SinOsc.ar/1:
                            frequency: 442.0
                            phase: 0.0
                    -   BinaryOpUGen(ADDITION).ar/1:
                            left: 330.0
                            right: SinOsc.ar/1[0]
                    -   SinOsc.ar/2:
                            frequency: 443.0
                            phase: 0.0
                    -   BinaryOpUGen(ADDITION).ar/2:
                            left: 220.0
                            right: SinOsc.ar/2[0]

        Returns ugen graph.
        """
        return UGenMethodMixin._compute_binary_op(expr, self, BinaryOperator.ADDITION)

    def __rdiv__(self, expr):
        """
        Divides `expr` by ugen graph.

        ..  container:: example

            **Example 1:**

            ::

                >>> expr = 1.5
                >>> ugen_graph = supriya.ugens.SinOsc.ar()
                >>> result = expr / ugen_graph
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: d79490206a430281b186b188d617f679
                    ugens:
                    -   SinOsc.ar:
                            frequency: 440.0
                            phase: 0.0
                    -   BinaryOpUGen(FLOAT_DIVISION).ar:
                            left: 1.5
                            right: SinOsc.ar[0]

        ..  container:: example

            **Example 2:**

            ::

                >>> expr = [220, 330]
                >>> ugen_graph = supriya.ugens.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ... )
                >>> result = expr / ugen_graph
                >>> result
                UGenArray({3})

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: d71b3081490f800d5136c87f5fef46d1
                    ugens:
                    -   SinOsc.ar/0:
                            frequency: 440.0
                            phase: 0.0
                    -   BinaryOpUGen(FLOAT_DIVISION).ar/0:
                            left: 220.0
                            right: SinOsc.ar/0[0]
                    -   SinOsc.ar/1:
                            frequency: 442.0
                            phase: 0.0
                    -   BinaryOpUGen(FLOAT_DIVISION).ar/1:
                            left: 330.0
                            right: SinOsc.ar/1[0]
                    -   SinOsc.ar/2:
                            frequency: 443.0
                            phase: 0.0
                    -   BinaryOpUGen(FLOAT_DIVISION).ar/2:
                            left: 220.0
                            right: SinOsc.ar/2[0]

        Returns ugen graph.
        """
        return UGenMethodMixin._compute_binary_op(
            expr, self, BinaryOperator.FLOAT_DIVISION
        )

    def __rmod__(self, expr):
        """
        Gets modulo of `expr` and ugen graph.

        ..  container:: example

            **Example 1:**

            ::

                >>> expr = 1.5
                >>> ugen_graph = supriya.ugens.SinOsc.ar()
                >>> result = expr % ugen_graph
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: d79490206a430281b186b188d617f679
                    ugens:
                    -   SinOsc.ar:
                            frequency: 440.0
                            phase: 0.0
                    -   BinaryOpUGen(FLOAT_DIVISION).ar:
                            left: 1.5
                            right: SinOsc.ar[0]

        ..  container:: example

            **Example 2:**

            ::

                >>> expr = [220, 330]
                >>> ugen_graph = supriya.ugens.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ... )
                >>> result = expr % ugen_graph
                >>> result
                UGenArray({3})

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: d71b3081490f800d5136c87f5fef46d1
                    ugens:
                    -   SinOsc.ar/0:
                            frequency: 440.0
                            phase: 0.0
                    -   BinaryOpUGen(FLOAT_DIVISION).ar/0:
                            left: 220.0
                            right: SinOsc.ar/0[0]
                    -   SinOsc.ar/1:
                            frequency: 442.0
                            phase: 0.0
                    -   BinaryOpUGen(FLOAT_DIVISION).ar/1:
                            left: 330.0
                            right: SinOsc.ar/1[0]
                    -   SinOsc.ar/2:
                            frequency: 443.0
                            phase: 0.0
                    -   BinaryOpUGen(FLOAT_DIVISION).ar/2:
                            left: 220.0
                            right: SinOsc.ar/2[0]

        Returns ugen graph.
        """
        return UGenMethodMixin._compute_binary_op(
            expr, self, BinaryOperator.FLOAT_DIVISION
        )

    def __rmul__(self, expr):
        """
        Multiplies `expr` by ugen graph.

        ..  container:: example

            **Example 1:**

            ::

                >>> expr = 1.5
                >>> ugen_graph = supriya.ugens.SinOsc.ar()
                >>> result = expr * ugen_graph
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: f60bbe0480298a7ae8b54de5a4c0260f
                    ugens:
                    -   SinOsc.ar:
                            frequency: 440.0
                            phase: 0.0
                    -   BinaryOpUGen(MULTIPLICATION).ar:
                            left: 1.5
                            right: SinOsc.ar[0]

        ..  container:: example

            **Example 2:**

            ::

                >>> expr = [220, 330]
                >>> ugen_graph = supriya.ugens.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ... )
                >>> result = expr * ugen_graph
                >>> result
                UGenArray({3})

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 0295153106bff55a2bf6db3b7184d301
                    ugens:
                    -   SinOsc.ar/0:
                            frequency: 440.0
                            phase: 0.0
                    -   BinaryOpUGen(MULTIPLICATION).ar/0:
                            left: 220.0
                            right: SinOsc.ar/0[0]
                    -   SinOsc.ar/1:
                            frequency: 442.0
                            phase: 0.0
                    -   BinaryOpUGen(MULTIPLICATION).ar/1:
                            left: 330.0
                            right: SinOsc.ar/1[0]
                    -   SinOsc.ar/2:
                            frequency: 443.0
                            phase: 0.0
                    -   BinaryOpUGen(MULTIPLICATION).ar/2:
                            left: 220.0
                            right: SinOsc.ar/2[0]

        Returns ugen graph.
        """
        return UGenMethodMixin._compute_binary_op(
            expr, self, BinaryOperator.MULTIPLICATION
        )

    def __rsub__(self, expr):
        """
        Subtracts ugen graph from `expr`.

        ..  container:: example

            **Example 1:**

            ::

                >>> expr = 1.5
                >>> ugen_graph = supriya.ugens.SinOsc.ar()
                >>> result = expr - ugen_graph
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 74e331121aa41f4d49a6d38a38ca4a9a
                    ugens:
                    -   SinOsc.ar:
                            frequency: 440.0
                            phase: 0.0
                    -   BinaryOpUGen(SUBTRACTION).ar:
                            left: 1.5
                            right: SinOsc.ar[0]

        ..  container:: example

            **Example 2:**

            ::

                >>> expr = [220, 330]
                >>> ugen_graph = supriya.ugens.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ... )
                >>> result = expr - ugen_graph
                >>> result
                UGenArray({3})

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 1ca2e8f3f541b9365413a0dbf9028e95
                    ugens:
                    -   SinOsc.ar/0:
                            frequency: 440.0
                            phase: 0.0
                    -   BinaryOpUGen(SUBTRACTION).ar/0:
                            left: 220.0
                            right: SinOsc.ar/0[0]
                    -   SinOsc.ar/1:
                            frequency: 442.0
                            phase: 0.0
                    -   BinaryOpUGen(SUBTRACTION).ar/1:
                            left: 330.0
                            right: SinOsc.ar/1[0]
                    -   SinOsc.ar/2:
                            frequency: 443.0
                            phase: 0.0
                    -   BinaryOpUGen(SUBTRACTION).ar/2:
                            left: 220.0
                            right: SinOsc.ar/2[0]

        Returns ugen graph.
        """
        return UGenMethodMixin._compute_binary_op(
            expr, self, BinaryOperator.SUBTRACTION
        )

    def __str__(self):
        """
        Gets string representation of ugen graph.

        ..  container:: example

            ::

                >>> ugen_graph = supriya.ugens.SinOsc.ar()
                >>> print(str(ugen_graph))
                synthdef:
                    name: c9b0ed62d4e0666b74166ff5ec09abe4
                    ugens:
                    -   SinOsc.ar:
                            frequency: 440.0
                            phase: 0.0

        ..  container:: example

            ::

                >>> ugen_graph = supriya.ugens.SinOsc.ar(frequency=[1, 2, 3])
                >>> print(str(ugen_graph))
                synthdef:
                    name: 4015dac116b25c54b4a6f02bcb5859cb
                    ugens:
                    -   SinOsc.ar/0:
                            frequency: 1.0
                            phase: 0.0
                    -   SinOsc.ar/1:
                            frequency: 2.0
                            phase: 0.0
                    -   SinOsc.ar/2:
                            frequency: 3.0
                            phase: 0.0

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

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar()
                >>> result = ugen_graph - expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: cd62fff8ff3ad7758d0f7ad82f39c7ce
                    ugens:
                    -   WhiteNoise.kr: null
                    -   SinOsc.ar:
                            frequency: 440.0
                            phase: 0.0
                    -   BinaryOpUGen(SUBTRACTION).ar:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar[0]

        ..  container:: example

            **Example 2:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ... )
                >>> result = ugen_graph - expr
                >>> result
                UGenArray({3})

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 9a8355f84507908cadf3cc63187ddab4
                    ugens:
                    -   WhiteNoise.kr: null
                    -   SinOsc.ar/0:
                            frequency: 440.0
                            phase: 0.0
                    -   BinaryOpUGen(SUBTRACTION).ar/0:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar/0[0]
                    -   SinOsc.ar/1:
                            frequency: 442.0
                            phase: 0.0
                    -   BinaryOpUGen(SUBTRACTION).ar/1:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar/1[0]
                    -   SinOsc.ar/2:
                            frequency: 443.0
                            phase: 0.0
                    -   BinaryOpUGen(SUBTRACTION).ar/2:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar/2[0]

        ..  container:: example

            **Example 3:**

            ::

                >>> ugen_graph = supriya.ugens.Dust.ar(
                ...     density=11.5,
                ... )
                >>> expr = 4
                >>> result = ugen_graph - expr
                >>> result
                BinaryOpUGen.ar()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 48ca704043ed00a2b6a55fd4b6b72cf1
                    ugens:
                    -   Dust.ar:
                            density: 11.5
                    -   BinaryOpUGen(SUBTRACTION).ar:
                            left: Dust.ar[0]
                            right: 4.0

        Returns ugen graph.
        """
        return UGenMethodMixin._compute_binary_op(
            self, expr, BinaryOperator.SUBTRACTION
        )

    __truediv__ = __div__
    __rtruediv__ = __rdiv__

    ### PRIVATE METHODS ###

    def _clone(self):
        def recurse(uuid, ugen, all_ugens):
            if hasattr(ugen, "inputs"):
                for input_ in ugen.inputs:
                    if not isinstance(input_, supriya.synthdefs.OutputProxy):
                        continue
                    input_ = input_.source
                    input_._uuid = uuid
                    recurse(uuid, input_, all_ugens)
            ugen._uuid = uuid
            if ugen not in all_ugens:
                all_ugens.append(ugen)

        import supriya.ugens

        builder = supriya.synthdefs.SynthDefBuilder()
        ugens = copy.deepcopy(self)
        if not isinstance(ugens, supriya.synthdefs.UGenArray):
            ugens = [ugens]
        all_ugens = []
        for ugen in ugens:
            if isinstance(ugen, supriya.synthdefs.OutputProxy):
                ugen = ugen.source
            recurse(builder._uuid, ugen, all_ugens)
        for ugen in all_ugens:
            if isinstance(ugen, supriya.synthdefs.UGen):
                builder._add_ugens(ugen)
            else:
                builder._add_parameter(ugen)
        return builder.build(optimize=False)

    @staticmethod
    def _compute_binary_op(left, right, operator):
        import supriya.synthdefs
        import supriya.ugens

        result = []
        if not isinstance(left, collections.abc.Sequence):
            left = (left,)
        if not isinstance(right, collections.abc.Sequence):
            right = (right,)
        dictionary = {"left": left, "right": right}
        operator = BinaryOperator.from_expr(operator)
        special_index = operator.value
        for expanded_dict in supriya.synthdefs.UGen._expand_dictionary(dictionary):
            left = expanded_dict["left"]
            right = expanded_dict["right"]
            calculation_rate = UGenMethodMixin._compute_binary_rate(left, right)
            ugen = supriya.synthdefs.BinaryOpUGen._new_single(
                calculation_rate=calculation_rate,
                left=left,
                right=right,
                special_index=special_index,
            )
            result.append(ugen)
        if len(result) == 1:
            return result[0]
        return supriya.synthdefs.UGenArray(result)

    @staticmethod
    def _compute_binary_rate(ugen_a, ugen_b):
        import supriya.synthdefs

        a_rate = supriya.CalculationRate.from_expr(ugen_a)
        b_rate = supriya.CalculationRate.from_expr(ugen_b)
        if (
            a_rate == supriya.CalculationRate.DEMAND
            or a_rate == supriya.CalculationRate.DEMAND
        ):
            return supriya.CalculationRate.DEMAND
        elif (
            a_rate == supriya.CalculationRate.AUDIO
            or b_rate == supriya.CalculationRate.AUDIO
        ):
            return supriya.CalculationRate.AUDIO
        elif (
            a_rate == supriya.CalculationRate.CONTROL
            or b_rate == supriya.CalculationRate.CONTROL
        ):
            return supriya.CalculationRate.CONTROL
        return supriya.CalculationRate.SCALAR

    def _compute_ugen_map(self, map_ugen, **kwargs):
        import supriya.synthdefs
        import supriya.ugens

        sources = []
        ugens = []
        if len(self) == 1:
            sources = [self]
        else:
            sources = self
        for source in sources:
            method = supriya.synthdefs.UGen._get_method_for_rate(map_ugen, source)
            ugen = method(source=source, **kwargs)
            ugens.extend(ugen)
        if 1 < len(ugens):
            return supriya.synthdefs.UGenArray(ugens)
        elif len(ugens) == 1:
            return ugens[0].source
        return []

    @staticmethod
    def _compute_unary_op(source, operator):
        import supriya.synthdefs
        import supriya.ugens

        result = []
        if not isinstance(source, collections.abc.Sequence):
            source = (source,)
        operator = UnaryOperator.from_expr(operator)
        special_index = operator.value
        for single_source in source:
            calculation_rate = supriya.CalculationRate.from_expr(single_source)
            ugen = supriya.synthdefs.UnaryOpUGen._new_single(
                calculation_rate=calculation_rate,
                source=single_source,
                special_index=special_index,
            )
            result.append(ugen)
        if len(result) == 1:
            return result[0]
        return supriya.synthdefs.UGenArray(result)

    def _get_output_proxy(self, i):
        import supriya.synthdefs

        if isinstance(i, int):
            if not (0 <= i < len(self)):
                raise IndexError(i, len(self))
            return supriya.synthdefs.OutputProxy(self, i)
        indices = i.indices(len(self))
        if not (0 <= indices[0] <= indices[1] <= len(self)):
            raise IndexError(i, indices, len(self))
        output_proxies = (
            supriya.synthdefs.OutputProxy(self, i) for i in range(*indices)
        )
        return supriya.synthdefs.UGenArray(output_proxies)

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

                >>> ugen_graph = supriya.ugens.SinOsc.ar()
                >>> expr = supriya.ugens.WhiteNoise.kr()
                >>> result = ugen_graph.absolute_difference(expr)

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: a6b274b5f30e1dfa86ac1d00ef1c169b
                    ugens:
                    -   SinOsc.ar:
                            frequency: 440.0
                            phase: 0.0
                    -   WhiteNoise.kr: null
                    -   BinaryOpUGen(ABSOLUTE_DIFFERENCE).ar:
                            left: SinOsc.ar[0]
                            right: WhiteNoise.kr[0]

        Returns ugen graph.
        """
        return self._compute_binary_op(self, expr, BinaryOperator.ABSOLUTE_DIFFERENCE)

    def amplitude_to_db(self):
        """
        Converts ugen graph from amplitude to decibels.

        ..  container:: example

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.ar()
                >>> result = ugen_graph.amplitude_to_db()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 73daa5fd8db0d28c03c3872c845fd3ed
                    ugens:
                    -   WhiteNoise.ar: null
                    -   UnaryOpUGen(AMPLITUDE_TO_DB).ar:
                            source: WhiteNoise.ar[0]

        Returns ugen graph.
        """
        return self._compute_unary_op(self, UnaryOperator.AMPLITUDE_TO_DB)

    def as_int(self):
        return self._compute_unary_op(self, UnaryOperator.AS_INT)

    def ceiling(self):
        """
        Calculates the ceiling of ugen graph.

        ::

            >>> source = supriya.ugens.DC.ar(source=0.5)
            >>> operation = source.ceiling()
            >>> print(operation)
            synthdef:
                name: c7b1855219f3364f731bdd2e4599b1d1
                ugens:
                -   DC.ar:
                        source: 0.5
                -   UnaryOpUGen(CEILING).ar:
                        source: DC.ar[0]

        Returns ugen graph.
        """
        return self._compute_unary_op(self, UnaryOperator.CEILING)

    def clip(self, minimum, maximum):
        """
        Clips ugen graph.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.ar()
                >>> result = ugen_graph.clip(-0.25, 0.25)

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: e710843b0e0fbc5e6185afc6cdf90149
                    ugens:
                    -   WhiteNoise.ar: null
                    -   Clip.ar:
                            source: WhiteNoise.ar[0]
                            minimum: -0.25
                            maximum: 0.25

        ..  container:: example

            **Example 2:**

            ::

                >>> ugen_graph = supriya.ugens.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ... )
                >>> result = ugen_graph.clip(-0.25, 0.25)

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 000e997ea0d7e8637c9f9040547baa50
                    ugens:
                    -   SinOsc.ar/0:
                            frequency: 440.0
                            phase: 0.0
                    -   Clip.ar/0:
                            source: SinOsc.ar/0[0]
                            minimum: -0.25
                            maximum: 0.25
                    -   SinOsc.ar/1:
                            frequency: 442.0
                            phase: 0.0
                    -   Clip.ar/1:
                            source: SinOsc.ar/1[0]
                            minimum: -0.25
                            maximum: 0.25
                    -   SinOsc.ar/2:
                            frequency: 443.0
                            phase: 0.0
                    -   Clip.ar/2:
                            source: SinOsc.ar/2[0]
                            minimum: -0.25
                            maximum: 0.25

        """
        import supriya.ugens

        return self._compute_ugen_map(
            supriya.ugens.Clip, minimum=minimum, maximum=maximum
        )

    def cubed(self):
        """
        Calculates the cube of ugen graph.

        ::

            >>> source = supriya.ugens.DC.ar(source=0.5)
            >>> operation = source.cubed()
            >>> print(operation)
            synthdef:
                name: ad344666e7f3f60edac95b1ea40c412d
                ugens:
                -   DC.ar:
                        source: 0.5
                -   UnaryOpUGen(CUBED).ar:
                        source: DC.ar[0]

        Returns ugen graph.
        """
        return self._compute_unary_op(self, UnaryOperator.CUBED)

    def db_to_amplitude(self):
        """
        Converts ugen graph from decibels to amplitude.

        ..  container:: example

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.ar()
                >>> result = ugen_graph.db_to_amplitude()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: fe82aae42b01b2b43d427cafd77c1c22
                    ugens:
                    -   WhiteNoise.ar: null
                    -   UnaryOpUGen(DB_TO_AMPLITUDE).ar:
                            source: WhiteNoise.ar[0]

        Returns ugen graph.
        """
        return self._compute_unary_op(self, UnaryOperator.DB_TO_AMPLITUDE)

    def distort(self):
        """
        Distorts ugen graph non-linearly.

        ::

            >>> source = supriya.ugens.DC.ar(source=0.5)
            >>> operation = source.distort()
            >>> print(operation)
            synthdef:
                name: bb632e15f448820d93b3880ad943617b
                ugens:
                -   DC.ar:
                        source: 0.5
                -   UnaryOpUGen(DISTORT).ar:
                        source: DC.ar[0]

        Returns ugen graph.
        """
        return self._compute_unary_op(self, UnaryOperator.DISTORT)

    def exponential(self):
        """
        Calculates the natural exponential function of ugen graph.

        ::

            >>> source = supriya.ugens.DC.ar(source=0.5)
            >>> operation = source.exponential()
            >>> print(operation)
            synthdef:
                name: f3b8b1036b3cceddf116c3f6a3c5a9a0
                ugens:
                -   DC.ar:
                        source: 0.5
                -   UnaryOpUGen(EXPONENTIAL).ar:
                        source: DC.ar[0]

        Returns ugen graph.
        """
        return self._compute_unary_op(self, UnaryOperator.EXPONENTIAL)

    def floor(self):
        """
        Calculates the floor of ugen graph.

        ::

            >>> source = supriya.ugens.DC.ar(source=0.5)
            >>> operation = source.floor()
            >>> print(operation)
            synthdef:
                name: 407228cfdb74bdd79b51c425fb8a7f77
                ugens:
                -   DC.ar:
                        source: 0.5
                -   UnaryOpUGen(FLOOR).ar:
                        source: DC.ar[0]

        Returns ugen graph.
        """
        return self._compute_unary_op(self, UnaryOperator.FLOOR)

    def fractional_part(self):
        """
        Calculates the fraction part of ugen graph.

        ::

            >>> source = supriya.ugens.DC.ar(source=0.5)
            >>> operation = source.fractional_part()
            >>> print(operation)
            synthdef:
                name: c663d5ee6c7c5347c043727c628af658
                ugens:
                -   DC.ar:
                        source: 0.5
                -   UnaryOpUGen(FRACTIONAL_PART).ar:
                        source: DC.ar[0]

        Returns ugen graph.
        """
        return self._compute_unary_op(self, UnaryOperator.FRACTIONAL_PART)

    def hanning_window(self):
        """
        Calculates Hanning-window of ugen graph.

        ..  container:: example

            ::

                >>> ugen_graph = supriya.ugens.LFNoise2.ar()
                >>> result = ugen_graph.hanning_window()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 18cb43db42ae3499f2c233e83df877fd
                    ugens:
                    -   LFNoise2.ar:
                            frequency: 500.0
                    -   UnaryOpUGen(HANNING_WINDOW).ar:
                            source: LFNoise2.ar[0]

        Returns ugen graph.
        """
        return self._compute_unary_op(self, UnaryOperator.HANNING_WINDOW)

    def hz_to_midi(self):
        """
        Converts ugen graph from Hertz to midi note number.

        ..  container:: example

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.ar()
                >>> result = ugen_graph.hz_to_midi()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 227a6ae85bc89b3af939cff32f54e36a
                    ugens:
                    -   WhiteNoise.ar: null
                    -   UnaryOpUGen(HZ_TO_MIDI).ar:
                            source: WhiteNoise.ar[0]

        Returns ugen graph.
        """
        return self._compute_unary_op(self, UnaryOperator.HZ_TO_MIDI)

    def hz_to_octave(self):
        """
        Converts ugen graph from Hertz to octave number.

        ..  container:: example

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.ar()
                >>> result = ugen_graph.hz_to_octave()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: e4fd4ca786d453fc5dfb955c63b6fbf6
                    ugens:
                    -   WhiteNoise.ar: null
                    -   UnaryOpUGen(HZ_TO_OCTAVE).ar:
                            source: WhiteNoise.ar[0]

        Returns ugen graph.
        """
        return self._compute_unary_op(self, UnaryOperator.HZ_TO_OCTAVE)

    def is_equal_to(self, expr):
        """
        Calculates equality between ugen graph and `expr`.

        ::

            >>> left = supriya.ugens.SinOsc.ar()
            >>> right = supriya.ugens.WhiteNoise.kr()
            >>> operation = left.is_equal_to(right)
            >>> print(operation)
            synthdef:
                name: 8287d890708ce26adff4968d63d494a0
                ugens:
                -   SinOsc.ar:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(EQUAL).ar:
                        left: SinOsc.ar[0]
                        right: WhiteNoise.kr[0]

        Returns ugen graph.
        """
        return self._compute_binary_op(self, expr, BinaryOperator.EQUAL)

    def is_not_equal_to(self, expr):
        """
        Calculates inequality between ugen graph and `expr`.

        ::

            >>> left = supriya.ugens.SinOsc.ar()
            >>> right = supriya.ugens.WhiteNoise.kr()
            >>> operation = left.is_not_equal_to(right)
            >>> print(operation)
            synthdef:
                name: b9f77aa86bc08a3b023d8f664afef05d
                ugens:
                -   SinOsc.ar:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(NOT_EQUAL).ar:
                        left: SinOsc.ar[0]
                        right: WhiteNoise.kr[0]

        Returns ugen graph.
        """
        return self._compute_binary_op(self, expr, BinaryOperator.NOT_EQUAL)

    def lag(self, lag_time=0.5):
        """
        Lags ugen graph.

        ..  container:: example

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.ar()
                >>> result = ugen_graph.lag(0.5)

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 6c3e2cc1a3d54ecfaa49d567a84eae77
                    ugens:
                    -   WhiteNoise.ar: null
                    -   Lag.ar:
                            source: WhiteNoise.ar[0]
                            lag_time: 0.5

        ..  container:: example

            ::

                >>> ugen_graph = supriya.ugens.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ... )
                >>> result = ugen_graph.lag(0.5)

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 67098a4ddab35f6e1333a80a226bf559
                    ugens:
                    -   SinOsc.ar/0:
                            frequency: 440.0
                            phase: 0.0
                    -   Lag.ar/0:
                            source: SinOsc.ar/0[0]
                            lag_time: 0.5
                    -   SinOsc.ar/1:
                            frequency: 442.0
                            phase: 0.0
                    -   Lag.ar/1:
                            source: SinOsc.ar/1[0]
                            lag_time: 0.5
                    -   SinOsc.ar/2:
                            frequency: 443.0
                            phase: 0.0
                    -   Lag.ar/2:
                            source: SinOsc.ar/2[0]
                            lag_time: 0.5

        """
        import supriya.ugens

        return self._compute_ugen_map(supriya.ugens.Lag, lag_time=lag_time)

    def log(self):
        """
        Calculates the natural logarithm of ugen graph.

        ::

            >>> source = supriya.ugens.DC.ar(source=0.5)
            >>> operation = source.log()
            >>> print(operation)
            synthdef:
                name: 4da44dab9d935efd1cf098b4d7cec420
                ugens:
                -   DC.ar:
                        source: 0.5
                -   UnaryOpUGen(LOG).ar:
                        source: DC.ar[0]

        Returns ugen graph.
        """
        return self._compute_unary_op(self, UnaryOperator.LOG)

    def log2(self):
        """
        Calculates the base-2 logarithm of ugen graph.

        ::

            >>> source = supriya.ugens.DC.ar(source=0.5)
            >>> operation = source.log2()
            >>> print(operation)
            synthdef:
                name: f956f79a387ffbeb409326046397b4dd
                ugens:
                -   DC.ar:
                        source: 0.5
                -   UnaryOpUGen(LOG2).ar:
                        source: DC.ar[0]

        Returns ugen graph.
        """
        return self._compute_unary_op(self, UnaryOperator.LOG2)

    def log10(self):
        """
        Calculates the base-10 logarithm of ugen graph.

        ::

            >>> source = supriya.ugens.DC.ar(source=0.5)
            >>> operation = source.log10()
            >>> print(operation)
            synthdef:
                name: 122d9333b8ac76164782d00707d3386a
                ugens:
                -   DC.ar:
                        source: 0.5
                -   UnaryOpUGen(LOG10).ar:
                        source: DC.ar[0]

        Returns ugen graph.
        """
        return self._compute_unary_op(self, UnaryOperator.LOG10)

    def maximum(self, expr):
        """
        Calculates maximum between ugen graph and `expr`.

        ::

            >>> left = supriya.ugens.SinOsc.ar()
            >>> right = supriya.ugens.WhiteNoise.kr()
            >>> operation = left.maximum(right)
            >>> print(operation)
            synthdef:
                name: dcdca07fb0439c8b4321f42803d18c32
                ugens:
                -   SinOsc.ar:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(MAXIMUM).ar:
                        left: SinOsc.ar[0]
                        right: WhiteNoise.kr[0]

        Returns ugen graph.
        """
        return self._compute_binary_op(self, expr, BinaryOperator.MAXIMUM)

    def midi_to_hz(self):
        """
        Converts ugen graph from midi note number to Hertz.

        ..  container:: example

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.ar()
                >>> result = ugen_graph.midi_to_hz()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 5faaa2c74715175625d774b20952f263
                    ugens:
                    -   WhiteNoise.ar: null
                    -   UnaryOpUGen(MIDI_TO_HZ).ar:
                            source: WhiteNoise.ar[0]

        Returns ugen graph.
        """
        return self._compute_unary_op(self, UnaryOperator.MIDI_TO_HZ)

    def minimum(self, expr):
        """
        Calculates minimum between ugen graph and `expr`.

        ::

            >>> left = supriya.ugens.SinOsc.ar()
            >>> right = supriya.ugens.WhiteNoise.kr()
            >>> operation = left.minimum(right)
            >>> print(operation)
            synthdef:
                name: f80c0a7b300911e9eff0e8760f5fab18
                ugens:
                -   SinOsc.ar:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(MINIMUM).ar:
                        left: SinOsc.ar[0]
                        right: WhiteNoise.kr[0]

        Returns ugen graph.
        """
        return self._compute_binary_op(self, expr, BinaryOperator.MINIMUM)

    def octave_to_hz(self):
        """
        Converts ugen graph from octave number to Hertz.

        ..  container:: example

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.ar()
                >>> result = ugen_graph.octave_to_hz()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 04c00b0f32088eb5e4cef0549aed6d96
                    ugens:
                    -   WhiteNoise.ar: null
                    -   UnaryOpUGen(OCTAVE_TO_HZ).ar:
                            source: WhiteNoise.ar[0]

        Returns ugen graph.
        """
        return self._compute_unary_op(self, UnaryOperator.OCTAVE_TO_HZ)

    def power(self, expr):
        """
        Raises ugen graph to the power of `expr`.

        ::

            >>> left = supriya.ugens.SinOsc.ar()
            >>> right = supriya.ugens.WhiteNoise.kr()
            >>> operation = left.power(right)
            >>> print(operation)
            synthdef:
                name: 06d6d3fe992bff8fce9ef55db6863c2a
                ugens:
                -   SinOsc.ar:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(POWER).ar:
                        left: SinOsc.ar[0]
                        right: WhiteNoise.kr[0]

        Returns ugen graph.
        """
        return self._compute_binary_op(self, expr, BinaryOperator.POWER)

    def range(self, minimum=0.0, maximum=1.0):
        if self.signal_range == SignalRange.BIPOLAR:
            return self.scale(-1, 1, minimum, maximum)
        return self.scale(0, 1, minimum, maximum)

    def exponential_range(self, minimum=0.01, maximum=1.0):
        if self.signal_range == SignalRange.BIPOLAR:
            return self.linexp(-1, 1, minimum, maximum)
        return self.linexp(0, 1, minimum, maximum)

    def ratio_to_semitones(self):
        """
        Converts ugen graph from frequency ratio to semitone distance.

        ..  container:: example

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.ar()
                >>> result = ugen_graph.ratio_to_semitones()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 2e23630ade4fab35fc821c190b7f33db
                    ugens:
                    -   WhiteNoise.ar: null
                    -   UnaryOpUGen(RATIO_TO_SEMITONES).ar:
                            source: WhiteNoise.ar[0]

        Returns ugen graph.
        """
        return self._compute_unary_op(self, UnaryOperator.RATIO_TO_SEMITONES)

    def rectangle_window(self):
        """
        Calculates rectangle-window of ugen graph.

        ..  container:: example

            ::

                >>> ugen_graph = supriya.ugens.LFNoise2.ar()
                >>> result = ugen_graph.rectangle_window()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 0d296187bbdb205f3a283f301a5fad61
                    ugens:
                    -   LFNoise2.ar:
                            frequency: 500.0
                    -   UnaryOpUGen(RECTANGLE_WINDOW).ar:
                            source: LFNoise2.ar[0]

        Returns ugen graph.
        """
        return self._compute_unary_op(self, UnaryOperator.RECTANGLE_WINDOW)

    def reciprocal(self):
        """
        Calculates reciprocal of ugen graph.

        ..  container:: example

            ::

                >>> ugen_graph = supriya.ugens.LFNoise2.ar()
                >>> result = ugen_graph.reciprocal()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 2e1c714d0def9d5c310197861d725559
                    ugens:
                    -   LFNoise2.ar:
                            frequency: 500.0
                    -   UnaryOpUGen(RECIPROCAL).ar:
                            source: LFNoise2.ar[0]

        Returns ugen graph.
        """
        return self._compute_unary_op(self, UnaryOperator.RECIPROCAL)

    def s_curve(self):
        """
        Calculates S-curve of ugen graph.

        ..  container:: example

            ::

                >>> ugen_graph = supriya.ugens.LFNoise2.ar()
                >>> result = ugen_graph.s_curve()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 21bcaf49922e2c4124d4cadba85c00ac
                    ugens:
                    -   LFNoise2.ar:
                            frequency: 500.0
                    -   UnaryOpUGen(S_CURVE).ar:
                            source: LFNoise2.ar[0]

        Returns ugen graph.
        """
        return self._compute_unary_op(self, UnaryOperator.S_CURVE)

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

                >>> ugen_graph = supriya.ugens.WhiteNoise.ar()
                >>> result = ugen_graph.scale(-1, 1, 0.5, 0.75)

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: e2295e64ed7b9c949ec22ccdc82520e3
                    ugens:
                    -   WhiteNoise.ar: null
                    -   MulAdd.ar:
                            source: WhiteNoise.ar[0]
                            multiplier: 0.125
                            addend: 0.625

        ..  container:: example

            ::

                >>> ugen_graph = supriya.ugens.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ... )
                >>> result = ugen_graph.scale(-1, 1, 0.5, 0.75, exponential=True)

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 88dca305143542bd40a82d8a6a337306
                    ugens:
                    -   SinOsc.ar/0:
                            frequency: 440.0
                            phase: 0.0
                    -   LinExp.ar/0:
                            source: SinOsc.ar/0[0]
                            input_minimum: -1.0
                            input_maximum: 1.0
                            output_minimum: 0.5
                            output_maximum: 0.75
                    -   SinOsc.ar/1:
                            frequency: 442.0
                            phase: 0.0
                    -   LinExp.ar/1:
                            source: SinOsc.ar/1[0]
                            input_minimum: -1.0
                            input_maximum: 1.0
                            output_minimum: 0.5
                            output_maximum: 0.75
                    -   SinOsc.ar/2:
                            frequency: 443.0
                            phase: 0.0
                    -   LinExp.ar/2:
                            source: SinOsc.ar/2[0]
                            input_minimum: -1.0
                            input_maximum: 1.0
                            output_minimum: 0.5
                            output_maximum: 0.75

        """
        import supriya.ugens

        map_ugen = supriya.ugens.LinLin
        if exponential:
            map_ugen = supriya.ugens.LinExp
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

                >>> ugen_graph = supriya.ugens.WhiteNoise.ar()
                >>> result = ugen_graph.semitones_to_ratio()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: f77ac2c24b06f8e620817f14285c2877
                    ugens:
                    -   WhiteNoise.ar: null
                    -   UnaryOpUGen(SEMITONES_TO_RATIO).ar:
                            source: WhiteNoise.ar[0]

        Returns ugen graph.
        """
        return self._compute_unary_op(self, UnaryOperator.SEMITONES_TO_RATIO)

    def sign(self):
        """
        Calculates sign of ugen graph.

        ..  container:: example

            ::

                >>> ugen_graph = supriya.ugens.LFNoise2.ar()
                >>> result = ugen_graph.sign()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 6f62abd8306dbf1aae66c09dd98203b5
                    ugens:
                    -   LFNoise2.ar:
                            frequency: 500.0
                    -   UnaryOpUGen(SIGN).ar:
                            source: LFNoise2.ar[0]

        Returns ugen graph.
        """
        return self._compute_unary_op(self, UnaryOperator.SIGN)

    def softclip(self):
        """
        Distorts ugen graph non-linearly.
        """
        return self._compute_unary_op(self, UnaryOperator.SOFTCLIP)

    def square_root(self):
        """
        Calculates square root of ugen graph.
        """
        return self._compute_unary_op(self, UnaryOperator.SQUARE_ROOT)

    def squared(self):
        """
        Calculates square of ugen graph.
        """
        return self._compute_unary_op(self, UnaryOperator.SQUARED)

    def sum(self):
        """
        Sums ugen graph.

        ..  container:: example

            **Example 1:**

            ::

                >>> ugen_graph = supriya.ugens.LFNoise2.ar()
                >>> result = ugen_graph.sum()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 350f2065d4edc69244399dcaff5a1ceb
                    ugens:
                    -   LFNoise2.ar:
                            frequency: 500.0

        ..  container:: example

            **Example 2:**

            ::

                >>> ugen_graph = supriya.ugens.SinOsc.ar([440, 442, 443])
                >>> result = ugen_graph.sum()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: a1d26283f87b8b445db982ff0e831fb7
                    ugens:
                    -   SinOsc.ar/0:
                            frequency: 440.0
                            phase: 0.0
                    -   SinOsc.ar/1:
                            frequency: 442.0
                            phase: 0.0
                    -   SinOsc.ar/2:
                            frequency: 443.0
                            phase: 0.0
                    -   Sum3.ar:
                            input_one: SinOsc.ar/0[0]
                            input_two: SinOsc.ar/1[0]
                            input_three: SinOsc.ar/2[0]

        Returns ugen graph.
        """
        import supriya.ugens

        return supriya.ugens.Mix.new(self)

    def tanh(self):
        """
        Calculates hyperbolic tangent of ugen graph.

        ..  container:: example

            ::

                >>> ugen_graph = supriya.ugens.LFNoise2.ar()
                >>> result = ugen_graph.tanh()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: e74aa9abf6e389d8ca39d2c9828d81be
                    ugens:
                    -   LFNoise2.ar:
                            frequency: 500.0
                    -   UnaryOpUGen(TANH).ar:
                            source: LFNoise2.ar[0]

        Returns ugen graph.
        """
        return self._compute_unary_op(self, UnaryOperator.TANH)

    def transpose(self, semitones):
        """
        Transposes ugen graph by `semitones`.

        ..  container:: example

            ::

                >>> ugen_graph = supriya.ugens.LFNoise2.ar()
                >>> result = ugen_graph.transpose([0, 3, 7])

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: c481c3d42e3cfcee0267250247dab51f
                    ugens:
                    -   LFNoise2.ar:
                            frequency: 500.0
                    -   UnaryOpUGen(HZ_TO_MIDI).ar:
                            source: LFNoise2.ar[0]
                    -   UnaryOpUGen(MIDI_TO_HZ).ar/0:
                            source: UnaryOpUGen(HZ_TO_MIDI).ar[0]
                    -   BinaryOpUGen(ADDITION).ar/0:
                            left: UnaryOpUGen(HZ_TO_MIDI).ar[0]
                            right: 3.0
                    -   UnaryOpUGen(MIDI_TO_HZ).ar/1:
                            source: BinaryOpUGen(ADDITION).ar/0[0]
                    -   BinaryOpUGen(ADDITION).ar/1:
                            left: UnaryOpUGen(HZ_TO_MIDI).ar[0]
                            right: 7.0
                    -   UnaryOpUGen(MIDI_TO_HZ).ar/2:
                            source: BinaryOpUGen(ADDITION).ar/1[0]

        Returns ugen graph.
        """
        return (self.hz_to_midi() + semitones).midi_to_hz()

    def triangle_window(self):
        """
        Calculates triangle-window of ugen graph.

        ..  container:: example

            ::

                >>> ugen_graph = supriya.ugens.LFNoise2.ar()
                >>> result = ugen_graph.triangle_window()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: ebb1820b9d08a639565b5090b53681db
                    ugens:
                    -   LFNoise2.ar:
                            frequency: 500.0
                    -   UnaryOpUGen(TRIANGLE_WINDOW).ar:
                            source: LFNoise2.ar[0]

        Returns ugen graph.
        """
        return self._compute_unary_op(self, UnaryOperator.TRIANGLE_WINDOW)

    def welch_window(self):
        """
        Calculates Welch-window of ugen graph.

        ..  container:: example

            ::

                >>> ugen_graph = supriya.ugens.LFNoise2.ar()
                >>> result = ugen_graph.welch_window()

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: ...
                    ugens:
                    -   LFNoise2.ar:
                            frequency: 500.0
                    -   UnaryOpUGen(WELCH_WINDOW).ar:
                            source: LFNoise2.ar[0]

        Returns ugen graph.
        """
        return self._compute_unary_op(self, UnaryOperator.WELCH_WINDOW)


class UGenArray(UGenMethodMixin, collections.abc.Sequence):

    ### CLASS VARIABLES ###

    __slots__ = ("_ugens",)

    ### INITIALIZER ###

    def __init__(self, ugens):
        assert isinstance(ugens, collections.abc.Iterable)
        ugens = tuple(ugens)
        assert len(ugens)
        self._ugens = ugens

    ### SPECIAL METHODS ###

    def __getitem__(self, i):
        return self.ugens[i]

    def __len__(self):
        return len(self.ugens)

    def __repr__(self):
        return "{}({{{}}})".format(type(self).__name__, len(self))

    ### PUBLIC PROPERTIES ###

    @property
    def signal_range(self):
        return max(_.signal_range for _ in self)

    @property
    def ugens(self):
        return self._ugens


class OutputProxy(UGenMethodMixin):

    ### INITIALIZER ###

    def __init__(self, source=None, output_index=None):
        self._output_index = output_index
        self._source = source

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if type(self) != type(expr):
            return False
        if self._output_index != expr._output_index:
            return False
        if self._source != expr._source:
            return False
        return True

    def __hash__(self):
        hash_values = (type(self), self._output_index, self._source)
        return hash(hash_values)

    def __iter__(self):
        yield self

    def __len__(self):
        return 1

    def __repr__(self):
        return "{!r}[{}]".format(self.source, self.output_index)

    ### PRIVATE METHODS ###

    def _get_output_number(self):
        return self._output_index

    def _get_source(self):
        return self._source

    ### PUBLIC PROPERTIES ###

    @property
    def calculation_rate(self):
        return self.source.calculation_rate

    @property
    def has_done_flag(self):
        return self.source.has_done_flag

    @property
    def output_index(self):
        return self._output_index

    @property
    def signal_range(self):
        return self.source.signal_range

    @property
    def source(self):
        return self._source
