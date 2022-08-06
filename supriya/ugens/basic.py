import collections

from supriya import CalculationRate, utils
from supriya.synthdefs import PseudoUGen, UGen


class Mix(PseudoUGen):
    """
    A down-to-mono signal mixer.

    ..  container:: example

        ::

            >>> with supriya.synthdefs.SynthDefBuilder() as builder:
            ...     oscillators = [supriya.ugens.DC.ar(1) for _ in range(5)]
            ...     mix = supriya.ugens.Mix.new(oscillators)
            ...
            >>> synthdef = builder.build(name="mix1", optimize=False)
            >>> supriya.graph(synthdef)  # doctest: +SKIP

        ::

            >>> print(synthdef)
            synthdef:
                name: mix1
                ugens:
                -   DC.ar/0:
                        source: 1.0
                -   DC.ar/1:
                        source: 1.0
                -   DC.ar/2:
                        source: 1.0
                -   DC.ar/3:
                        source: 1.0
                -   Sum4.ar:
                        input_one: DC.ar/0[0]
                        input_two: DC.ar/1[0]
                        input_three: DC.ar/2[0]
                        input_four: DC.ar/3[0]
                -   DC.ar/4:
                        source: 1.0
                -   BinaryOpUGen(ADDITION).ar:
                        left: Sum4.ar[0]
                        right: DC.ar/4[0]

    ..  container:: example

        ::

            >>> with supriya.synthdefs.SynthDefBuilder() as builder:
            ...     oscillators = [supriya.ugens.DC.ar(1) for _ in range(15)]
            ...     mix = supriya.ugens.Mix.new(oscillators)
            ...
            >>> synthdef = builder.build("mix2")
            >>> supriya.graph(synthdef)  # doctest: +SKIP

        ::

            >>> print(synthdef)
            synthdef:
                name: mix2
                ugens:
                -   DC.ar/0:
                        source: 1.0
                -   DC.ar/1:
                        source: 1.0
                -   DC.ar/2:
                        source: 1.0
                -   DC.ar/3:
                        source: 1.0
                -   Sum4.ar/0:
                        input_one: DC.ar/0[0]
                        input_two: DC.ar/1[0]
                        input_three: DC.ar/2[0]
                        input_four: DC.ar/3[0]
                -   DC.ar/4:
                        source: 1.0
                -   DC.ar/5:
                        source: 1.0
                -   DC.ar/6:
                        source: 1.0
                -   DC.ar/7:
                        source: 1.0
                -   Sum4.ar/1:
                        input_one: DC.ar/4[0]
                        input_two: DC.ar/5[0]
                        input_three: DC.ar/6[0]
                        input_four: DC.ar/7[0]
                -   DC.ar/8:
                        source: 1.0
                -   DC.ar/9:
                        source: 1.0
                -   DC.ar/10:
                        source: 1.0
                -   DC.ar/11:
                        source: 1.0
                -   Sum4.ar/2:
                        input_one: DC.ar/8[0]
                        input_two: DC.ar/9[0]
                        input_three: DC.ar/10[0]
                        input_four: DC.ar/11[0]
                -   DC.ar/12:
                        source: 1.0
                -   DC.ar/13:
                        source: 1.0
                -   DC.ar/14:
                        source: 1.0
                -   Sum3.ar:
                        input_one: DC.ar/12[0]
                        input_two: DC.ar/13[0]
                        input_three: DC.ar/14[0]
                -   Sum4.ar/3:
                        input_one: Sum4.ar/0[0]
                        input_two: Sum4.ar/1[0]
                        input_three: Sum4.ar/2[0]
                        input_four: Sum3.ar[0]

    """

    ### PRIVATE METHODS ###

    @classmethod
    def _flatten_sources(cls, sources):
        import supriya.synthdefs

        flattened_sources = []
        for source in sources:
            if isinstance(source, supriya.synthdefs.UGenArray):
                flattened_sources.extend(source)
            else:
                flattened_sources.append(source)
        return supriya.synthdefs.UGenArray(flattened_sources)

    ### PUBLIC METHODS ###

    @classmethod
    def new(cls, sources):
        import supriya.synthdefs
        import supriya.ugens

        sources = cls._flatten_sources(sources)
        summed_sources = []
        for part in utils.group_iterable_by_count(sources, 4):
            if len(part) == 4:
                summed_sources.append(supriya.ugens.Sum4(*part))
            elif len(part) == 3:
                summed_sources.append(supriya.ugens.Sum3(*part))
            elif len(part) == 2:
                summed_sources.append(part[0] + part[1])
            else:
                summed_sources.append(part[0])
        if len(summed_sources) == 1:
            return summed_sources[0]
        return Mix.new(summed_sources)

    @classmethod
    def multichannel(cls, sources, channel_count):
        """
        Segment by channel count and mix down in parallel.

        ..  container:: example

            Combine panner outputs, first with first, second with second, etc.

            ::

                >>> source = supriya.ugens.SinOsc.ar(frequency=[440, 660, 880])
                >>> panner = supriya.ugens.PanAz.ar(
                ...     channel_count=4,
                ...     source=source,
                ...     position=supriya.ugens.LFNoise2.kr(),
                ... )
                >>> mix = supriya.ugens.Mix.multichannel(panner, channel_count=4)
                >>> out = supriya.ugens.Out.ar(bus=0, source=mix)
                >>> supriya.graph(out)  # doctest: +SKIP

            ::

                >>> print(out)
                synthdef:
                    name: ...
                    ugens:
                    -   SinOsc.ar/0:
                            frequency: 440.0
                            phase: 0.0
                    -   LFNoise2.kr:
                            frequency: 500.0
                    -   PanAz.ar/0:
                            source: SinOsc.ar/0[0]
                            position: LFNoise2.kr[0]
                            amplitude: 1.0
                            width: 2.0
                            orientation: 0.5
                    -   SinOsc.ar/1:
                            frequency: 660.0
                            phase: 0.0
                    -   PanAz.ar/1:
                            source: SinOsc.ar/1[0]
                            position: LFNoise2.kr[0]
                            amplitude: 1.0
                            width: 2.0
                            orientation: 0.5
                    -   SinOsc.ar/2:
                            frequency: 880.0
                            phase: 0.0
                    -   PanAz.ar/2:
                            source: SinOsc.ar/2[0]
                            position: LFNoise2.kr[0]
                            amplitude: 1.0
                            width: 2.0
                            orientation: 0.5
                    -   Sum3.ar/0:
                            input_one: PanAz.ar/0[0]
                            input_two: PanAz.ar/1[0]
                            input_three: PanAz.ar/2[0]
                    -   Sum3.ar/1:
                            input_one: PanAz.ar/0[1]
                            input_two: PanAz.ar/1[1]
                            input_three: PanAz.ar/2[1]
                    -   Sum3.ar/2:
                            input_one: PanAz.ar/0[2]
                            input_two: PanAz.ar/1[2]
                            input_three: PanAz.ar/2[2]
                    -   Sum3.ar/3:
                            input_one: PanAz.ar/0[3]
                            input_two: PanAz.ar/1[3]
                            input_three: PanAz.ar/2[3]
                    -   Out.ar:
                            bus: 0.0
                            source[0]: Sum3.ar/0[0]
                            source[1]: Sum3.ar/1[0]
                            source[2]: Sum3.ar/2[0]
                            source[3]: Sum3.ar/3[0]

            Compare with a non-multichannel mixdown:

                >>> mix = supriya.ugens.Mix.new(panner)
                >>> out = supriya.ugens.Out.ar(bus=0, source=mix)
                >>> supriya.graph(out)  # doctest: +SKIP

            ::

                >>> print(out)
                synthdef:
                    name: ...
                    ugens:
                    -   SinOsc.ar/0:
                            frequency: 440.0
                            phase: 0.0
                    -   LFNoise2.kr:
                            frequency: 500.0
                    -   PanAz.ar/0:
                            source: SinOsc.ar/0[0]
                            position: LFNoise2.kr[0]
                            amplitude: 1.0
                            width: 2.0
                            orientation: 0.5
                    -   Sum4.ar/0:
                            input_one: PanAz.ar/0[0]
                            input_two: PanAz.ar/0[1]
                            input_three: PanAz.ar/0[2]
                            input_four: PanAz.ar/0[3]
                    -   SinOsc.ar/1:
                            frequency: 660.0
                            phase: 0.0
                    -   PanAz.ar/1:
                            source: SinOsc.ar/1[0]
                            position: LFNoise2.kr[0]
                            amplitude: 1.0
                            width: 2.0
                            orientation: 0.5
                    -   Sum4.ar/1:
                            input_one: PanAz.ar/1[0]
                            input_two: PanAz.ar/1[1]
                            input_three: PanAz.ar/1[2]
                            input_four: PanAz.ar/1[3]
                    -   SinOsc.ar/2:
                            frequency: 880.0
                            phase: 0.0
                    -   PanAz.ar/2:
                            source: SinOsc.ar/2[0]
                            position: LFNoise2.kr[0]
                            amplitude: 1.0
                            width: 2.0
                            orientation: 0.5
                    -   Sum4.ar/2:
                            input_one: PanAz.ar/2[0]
                            input_two: PanAz.ar/2[1]
                            input_three: PanAz.ar/2[2]
                            input_four: PanAz.ar/2[3]
                    -   Sum3.ar:
                            input_one: Sum4.ar/0[0]
                            input_two: Sum4.ar/1[0]
                            input_three: Sum4.ar/2[0]
                    -   Out.ar:
                            bus: 0.0
                            source[0]: Sum3.ar[0]

        """
        import supriya.synthdefs

        sources = cls._flatten_sources(sources)
        mixes, parts = [], []
        for i in range(0, len(sources), channel_count):
            parts.append(sources[i : i + channel_count])
        for columns in zip(*parts):
            mixes.append(cls.new(columns))
        return supriya.synthdefs.UGenArray(mixes)


class MulAdd(UGen):
    """
    An Optimized multiplication / addition ugen.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> mul_add = supriya.ugens.MulAdd.new(
        ...     addend=0.5,
        ...     multiplier=-1.5,
        ...     source=source,
        ... )
        >>> mul_add
        MulAdd.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("multiplier", 1.0), ("addend", 0.0)]
    )

    ### INITIALIZER ###

    def __init__(self, addend=0.0, multiplier=1.0, calculation_rate=None, source=None):
        UGen.__init__(
            self,
            addend=addend,
            multiplier=multiplier,
            calculation_rate=calculation_rate,
            source=source,
        )

    ### PRIVATE METHODS ###

    @staticmethod
    def _inputs_are_valid(source, multiplier, addend):
        if CalculationRate.from_expr(source) == CalculationRate.AUDIO:
            return True
        if CalculationRate.from_expr(source) == CalculationRate.CONTROL:
            if CalculationRate.from_expr(multiplier) in (
                CalculationRate.CONTROL,
                CalculationRate.SCALAR,
            ):
                if CalculationRate.from_expr(addend) in (
                    CalculationRate.CONTROL,
                    CalculationRate.SCALAR,
                ):
                    return True
        return False

    @classmethod
    def _new_single(
        cls, addend=None, multiplier=None, calculation_rate=None, source=None
    ):
        if multiplier == 0.0:
            return addend
        minus = multiplier == -1
        no_multiplier = multiplier == 1
        no_addend = addend == 0
        if no_multiplier and no_addend:
            return source
        if minus and no_addend:
            return -source
        if no_addend:
            return source * multiplier
        if minus:
            return addend - source
        if no_multiplier:
            return source + addend
        if cls._inputs_are_valid(source, multiplier, addend):
            return cls(
                addend=addend,
                multiplier=multiplier,
                calculation_rate=calculation_rate,
                source=source,
            )
        if cls._inputs_are_valid(multiplier, source, addend):
            return cls(
                addend=addend,
                multiplier=source,
                calculation_rate=calculation_rate,
                source=multiplier,
            )
        return (source * multiplier) + addend

    ### PUBLIC METHODS ###

    @classmethod
    def new(cls, source=None, multiplier=1.0, addend=0.0):
        """
        Constructs a multiplication / addition ugen.

        ::

            >>> addend = 0.5
            >>> multiplier = 1.5
            >>> source = supriya.ugens.SinOsc.ar(frequency=[440, 442])
            >>> mul_add = supriya.ugens.MulAdd.new(
            ...     addend=addend,
            ...     multiplier=multiplier,
            ...     source=source,
            ... )
            >>> mul_add
            UGenArray({2})

        Returns ugen graph.
        """
        import supriya.synthdefs

        # TODO: handle case of array as source
        calculation_rate = supriya.CalculationRate.from_expr(
            (source, multiplier, addend)
        )
        ugen = cls._new_expanded(
            addend=addend,
            multiplier=multiplier,
            calculation_rate=calculation_rate,
            source=source,
        )
        return ugen


class Sum3(UGen):
    """
    A three-input summing unit generator.

    ::

        >>> input_one = supriya.ugens.SinOsc.ar()
        >>> input_two = supriya.ugens.SinOsc.ar(phase=0.1)
        >>> input_three = supriya.ugens.SinOsc.ar(phase=0.2)
        >>> supriya.ugens.Sum3.new(
        ...     input_one=input_one,
        ...     input_two=input_two,
        ...     input_three=input_three,
        ... )
        Sum3.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [("input_one", None), ("input_two", None), ("input_three", None)]
    )

    _valid_calculation_rates = ()

    ### INITIALIZER ###

    def __init__(self, input_one=None, input_two=None, input_three=None):
        inputs = [input_one, input_two, input_three]
        calculation_rate = CalculationRate.from_expr(inputs)
        inputs.sort(key=lambda x: CalculationRate.from_expr(x), reverse=True)
        inputs = tuple(inputs)
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            input_one=input_one,
            input_two=input_two,
            input_three=input_three,
        )

    ### PRIVATE METHODS ###

    @classmethod
    def _new_single(cls, input_one=None, input_two=None, input_three=None, **kwargs):
        if input_three == 0:
            ugen = input_one + input_two
        elif input_two == 0:
            ugen = input_one + input_three
        elif input_one == 0:
            ugen = input_two + input_three
        else:
            ugen = cls(
                input_one=input_one, input_two=input_two, input_three=input_three
            )
        return ugen


class Sum4(UGen):
    """
    A four-input summing unit generator.

    ::

        >>> input_one = supriya.ugens.SinOsc.ar()
        >>> input_two = supriya.ugens.SinOsc.ar(phase=0.1)
        >>> input_three = supriya.ugens.SinOsc.ar(phase=0.2)
        >>> input_four = supriya.ugens.SinOsc.ar(phase=0.3)
        >>> supriya.ugens.Sum4.new(
        ...     input_one=input_one,
        ...     input_two=input_two,
        ...     input_three=input_three,
        ...     input_four=input_four,
        ... )
        Sum4.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [
            ("input_one", None),
            ("input_two", None),
            ("input_three", None),
            ("input_four", None),
        ]
    )

    _valid_calculation_rates = ()

    ### INITIALIZER ###

    def __init__(
        self, input_one=None, input_two=None, input_three=None, input_four=None
    ):
        inputs = [input_one, input_two, input_three, input_four]
        calculation_rate = CalculationRate.from_expr(inputs)
        inputs.sort(key=lambda x: CalculationRate.from_expr(x), reverse=True)
        inputs = tuple(inputs)
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            input_one=input_one,
            input_two=input_two,
            input_three=input_three,
            input_four=input_four,
        )

    ### PRIVATE METHODS ###

    @classmethod
    def _new_single(
        cls, input_one=None, input_two=None, input_three=None, input_four=None, **kwargs
    ):
        import supriya.ugens

        if input_one == 0:
            ugen = supriya.ugens.Sum3.new(
                input_one=input_two, input_two=input_three, input_three=input_four
            )
        elif input_two == 0:
            ugen = supriya.ugens.Sum3.new(
                input_one=input_one, input_two=input_three, input_three=input_four
            )
        elif input_three == 0:
            ugen = supriya.ugens.Sum3.new(
                input_one=input_one, input_two=input_two, input_three=input_four
            )
        elif input_four == 0:
            ugen = supriya.ugens.Sum3.new(
                input_one=input_one, input_two=input_two, input_three=input_three
            )
        else:
            ugen = cls(
                input_one=input_one,
                input_two=input_two,
                input_three=input_three,
                input_four=input_four,
            )
        return ugen
