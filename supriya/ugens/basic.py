from typing import Any, Sequence, SupportsInt, Union

from .. import utils
from ..enums import CalculationRate
from ..typing import CalculationRateLike
from ..utils import flatten
from .core import (
    PseudoUGen,
    UGen,
    UGenOperable,
    UGenScalar,
    UGenScalarInput,
    UGenVector,
    UGenVectorInput,
    param,
    ugen,
)


class Mix(PseudoUGen):
    """
    A down-to-mono signal mixer.

    .. container:: example

        ::

            >>> from supriya.ugens import DC, Mix, SynthDefBuilder

        ::

            >>> with SynthDefBuilder() as builder:
            ...     oscillators = [DC.ar(source=1) for _ in range(5)]
            ...     mix = Mix.new(oscillators)
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

    .. container:: example

        ::

            >>> with SynthDefBuilder() as builder:
            ...     oscillators = [DC.ar(source=1) for _ in range(15)]
            ...     mix = Mix.new(oscillators)
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

    ### PUBLIC METHODS ###

    @classmethod
    def new(cls, sources):
        if not isinstance(sources, Sequence):
            sources = [sources]
        sources = list(flatten(sources, terminal_types=UGenScalar))
        summed_sources = []
        for part in utils.group_by_count(sources, 4):
            if len(part) == 4:
                summed_sources.extend(
                    Sum4.new(
                        input_one=part[0],
                        input_two=part[1],
                        input_three=part[2],
                        input_four=part[3],
                    )
                )
            elif len(part) == 3:
                summed_sources.extend(
                    Sum3.new(
                        input_one=part[0],
                        input_two=part[1],
                        input_three=part[2],
                    )
                )
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

        .. container:: example

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
                            channel_count: 4
                            source: SinOsc.ar/0[0]
                            position: LFNoise2.kr[0]
                            amplitude: 1.0
                            width: 2.0
                            orientation: 0.5
                    -   SinOsc.ar/1:
                            frequency: 660.0
                            phase: 0.0
                    -   PanAz.ar/1:
                            channel_count: 4
                            source: SinOsc.ar/1[0]
                            position: LFNoise2.kr[0]
                            amplitude: 1.0
                            width: 2.0
                            orientation: 0.5
                    -   SinOsc.ar/2:
                            frequency: 880.0
                            phase: 0.0
                    -   PanAz.ar/2:
                            channel_count: 4
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

            ::

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
                            channel_count: 4
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
                            channel_count: 4
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
                            channel_count: 4
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
        sources = list(flatten(sources, terminal_types=UGenScalar))
        mixes, parts = [], []
        for i in range(0, len(sources), channel_count):
            parts.append(sources[i : i + channel_count])
        for columns in zip(*parts):
            mixes.append(cls.new(columns))
        return UGenVector(*mixes)


@ugen(new=True)
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
        <MulAdd.ar()>
    """

    ### CLASS VARIABLES ###

    source = param()
    multiplier = param(1.0)
    addend = param(0.0)

    ### PRIVATE METHODS ###

    @classmethod
    def _new_single(
        cls,
        *,
        addend=0,
        multiplier=0,
        source=0,
        calculation_rate: CalculationRateLike = None,
        special_index: SupportsInt = 0,
        **kwargs: Union["UGenScalarInput", "UGenVectorInput"],
    ) -> UGenOperable:
        def _inputs_are_valid(source, multiplier, addend):
            if CalculationRate.from_expr(source) == CalculationRate.AUDIO:
                return True
            return (
                CalculationRate.from_expr(source) == CalculationRate.CONTROL
                and CalculationRate.from_expr(multiplier)
                in (
                    CalculationRate.CONTROL,
                    CalculationRate.SCALAR,
                )
                and CalculationRate.from_expr(addend)
                in (
                    CalculationRate.CONTROL,
                    CalculationRate.SCALAR,
                )
            )

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
        if _inputs_are_valid(source, multiplier, addend):
            return cls(
                addend=addend,
                multiplier=multiplier,
                calculation_rate=CalculationRate.from_expr(
                    (source, multiplier, addend)
                ),
                source=source,
            )
        if _inputs_are_valid(multiplier, source, addend):
            return cls(
                addend=addend,
                multiplier=source,
                calculation_rate=CalculationRate.from_expr(
                    (multiplier, source, addend)
                ),
                source=multiplier,
            )
        return (source * multiplier) + addend


@ugen(new=True)
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
        <Sum3.ar()>
    """

    input_one = param()
    input_two = param()
    input_three = param()

    @classmethod
    def _new_single(cls, *, input_one, input_two, input_three, **kwargs):
        if input_three == 0:
            ugen = input_one + input_two
        elif input_two == 0:
            ugen = input_one + input_three
        elif input_one == 0:
            ugen = input_two + input_three
        else:
            ugen = cls(
                calculation_rate=None,
                input_one=input_one,
                input_two=input_two,
                input_three=input_three,
            )
        return ugen

    def _postprocess_kwargs(
        self, *, calculation_rate: CalculationRate, **kwargs
    ) -> tuple[CalculationRate, dict[str, Any]]:
        inputs = sorted(
            [kwargs["input_one"], kwargs["input_two"], kwargs["input_three"]],
            key=lambda x: CalculationRate.from_expr(x),
            reverse=True,
        )
        calculation_rate = CalculationRate.from_expr(inputs)
        kwargs.update(
            input_one=inputs[0],
            input_two=inputs[1],
            input_three=inputs[2],
        )
        return calculation_rate, kwargs


@ugen(new=True)
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
        <Sum4.ar()>
    """

    input_one = param()
    input_two = param()
    input_three = param()
    input_four = param()

    @classmethod
    def _new_single(cls, *, input_one, input_two, input_three, input_four, **kwargs):
        if input_one == 0:
            ugen = Sum3._new_single(
                input_one=input_two, input_two=input_three, input_three=input_four
            )
        elif input_two == 0:
            ugen = Sum3._new_single(
                input_one=input_one, input_two=input_three, input_three=input_four
            )
        elif input_three == 0:
            ugen = Sum3._new_single(
                input_one=input_one, input_two=input_two, input_three=input_four
            )
        elif input_four == 0:
            ugen = Sum3._new_single(
                input_one=input_one, input_two=input_two, input_three=input_three
            )
        else:
            ugen = cls(
                calculation_rate=None,
                input_one=input_one,
                input_two=input_two,
                input_three=input_three,
                input_four=input_four,
            )
        return ugen

    def _postprocess_kwargs(
        self, *, calculation_rate: CalculationRate, **kwargs
    ) -> tuple[CalculationRate, dict[str, Any]]:
        inputs = sorted(
            [
                kwargs["input_one"],
                kwargs["input_two"],
                kwargs["input_three"],
                kwargs["input_four"],
            ],
            key=lambda x: CalculationRate.from_expr(x),
            reverse=True,
        )
        calculation_rate = CalculationRate.from_expr(inputs)
        kwargs.update(
            input_one=inputs[0],
            input_two=inputs[1],
            input_three=inputs[2],
            input_four=inputs[3],
        )
        return calculation_rate, kwargs
