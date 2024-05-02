import abc
import collections
import copy
import dataclasses
import hashlib
import inspect
import pathlib
import struct
import subprocess
import tempfile
import threading
import uuid
from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    NamedTuple,
    Optional,
    Protocol,
    Sequence,
    SupportsFloat,
    Tuple,
    Type,
    Union,
    cast,
)

from ..typing import CalculationRateLike, Default, Missing

try:
    from typing import TypeAlias
except ImportError:
    from typing_extensions import TypeAlias  # noqa

import uqbar.graphs
from uqbar.objects import new

from .. import sclang, utils
from ..enums import (
    BinaryOperator,
    CalculationRate,
    DoneAction,
    ParameterRate,
    SignalRange,
    UnaryOperator,
)


class Check(Enum):
    NONE = 0
    SAME_AS_FIRST = 1
    SAME_OR_SLOWER = 2


class Param(NamedTuple):
    default: Optional[Union[Default, Missing, float]] = None
    check: Check = Check.NONE
    unexpanded: bool = False


def _add_init(
    cls,
    params: Dict[str, "Param"],
    is_multichannel: bool,
    channel_count: int,
    fixed_channel_count: bool,
) -> None:
    parent_class = inspect.getmro(cls)[1]
    args = ["self", "*", "calculation_rate: CalculationRateLike"]
    body = []
    if is_multichannel and not fixed_channel_count:
        args.append(f"channel_count={channel_count or 1}")
        body.append("self._channel_count = channel_count")
    if fixed_channel_count:
        body.append(f"self._channel_count = {channel_count}")
    body.extend(
        [
            f"return {parent_class.__name__}.__init__(",
            "    self,",
            "    calculation_rate=CalculationRate.from_expr(calculation_rate),",
        ]
    )
    for key, param in params.items():
        value_repr = _format_value(param.default)
        type_ = "UGenInitVectorParam" if param.unexpanded else "UGenInitScalarParam"
        prefix = f"{key}: {type_}"
        args.append(
            f"{prefix} = {value_repr}"
            if not isinstance(param.default, Missing)
            else prefix
        )
        body.append(f"    {key}={key},")
    args.append("**kwargs")
    body.append("    **kwargs,")
    body.append(")")
    _create_fn(
        cls=cls,
        name="__init__",
        args=args,
        body=body,
        globals_={**_get_fn_globals(), parent_class.__name__: parent_class},
        return_type=None,
    )


def _add_param_fn(cls, name: str, index: int, unexpanded: bool) -> None:
    _create_fn(
        cls=cls,
        name=name,
        args=["self"],
        body=(
            [f"return UGenVector(*self._inputs[{index}:])"]
            if unexpanded
            else [f"return UGenVector(*self._inputs[{index}:{index} + 1])"]
        ),
        decorator=property,
        globals_=_get_fn_globals(),
        override=True,
        return_type=UGenVector,
    )


def _add_rate_fn(
    cls,
    rate: Optional[CalculationRate],
    params: Dict[str, "Param"],
    is_multichannel: bool,
    channel_count: int,
    fixed_channel_count: bool,
) -> None:
    args = ["cls"]
    if params:
        args.append("*")
    for key, param in params.items():
        value_repr = _format_value(param.default)
        prefix = f"{key}: UGenRateVectorParam"
        args.append(
            f"{prefix} = {value_repr}"
            if not isinstance(param.default, Missing)
            else prefix
        )
    body = ["return cls._new_expanded("]
    if rate is not None:
        body.append(f"    calculation_rate={rate!r},")
    if is_multichannel and not fixed_channel_count:
        args.append(f"channel_count: int = {channel_count or 1}")
        body.append("    channel_count=channel_count,")
    body.extend(f"    {name}={name}," for name in params)
    body.append(")")
    _create_fn(
        cls=cls,
        name=rate.token if rate is not None else "new",
        args=args,
        body=body,
        decorator=classmethod,
        globals_=_get_fn_globals(),
        return_type=cls,
    )


def _create_fn(
    *,
    cls,
    name: str,
    args: List[str],
    body: List[str],
    return_type,
    globals_: Optional[Dict[str, Type]] = None,
    decorator: Optional[Callable] = None,
    override: bool = False,
) -> None:
    if name in cls.__dict__ and not override:
        return
    globals_ = globals_ or {}
    locals_ = {"_return_type": return_type}
    args_ = ",\n        ".join(args)
    body_ = "\n".join(f"        {line}" for line in body)
    text = f"    def {name}(\n        {args_}\n    ) -> _return_type:\n{body_}"
    local_vars = ", ".join(locals_.keys())
    text = f"def __create_fn__({local_vars}):\n{text}\n    return {name}"
    namespace: Dict[str, Callable] = {}
    exec(text, globals_, namespace)
    value = namespace["__create_fn__"](**locals_)
    value.__qualname__ = f"{cls.__qualname__}.{value.__name__}"
    if decorator:
        value = decorator(value)
    setattr(cls, name, value)


def _format_value(value) -> str:
    if value == float("inf"):
        value_repr = 'float("inf")'
    elif value == float("-inf"):
        value_repr = 'float("-inf")'
    elif isinstance(value, Default):
        value_repr = "Default()"
    elif isinstance(value, Missing):
        value_repr = "Missing()"
    else:
        value_repr = repr(value)
    return value_repr


def _get_fn_globals():
    return {
        "CalculationRate": CalculationRate,
        "CalculationRateLike": CalculationRateLike,
        "Default": Default,
        "DoneAction": DoneAction,
        "Missing": Missing,
        "OutputProxy": OutputProxy,
        "Sequence": Sequence,
        "SupportsFloat": SupportsFloat,
        "UGenVector": UGenVector,
        "UGenInitScalarParam": UGenInitScalarParam,
        "UGenInitVectorParam": UGenInitVectorParam,
        "UGenOperable": UGenOperable,
        "UGenRateVectorParam": UGenRateVectorParam,
        "UGenSerializable": UGenSerializable,
        "Union": Union,
    }


def _process_class(
    cls: Type["UGen"],
    *,
    ar: bool = False,
    kr: bool = False,
    ir: bool = False,
    dr: bool = False,
    new: bool = False,
    has_done_flag: bool = False,
    is_input: bool = False,
    is_multichannel: bool = False,
    is_output: bool = False,
    is_pure: bool = False,
    is_width_first: bool = False,
    channel_count: int = 1,
    fixed_channel_count: bool = False,
    signal_range: Optional[int] = None,
) -> Type["UGen"]:
    params: Dict[str, Param] = {}
    unexpanded_input_names = []
    valid_calculation_rates = []
    for name, value in cls.__dict__.items():
        if not isinstance(value, Param):
            continue
        params[name] = value
        if value.unexpanded:
            unexpanded_input_names.append(name)
        _add_param_fn(cls, name, len(params) - 1, value.unexpanded)
    _add_init(cls, params, is_multichannel, channel_count, fixed_channel_count)
    for should_add, rate in [
        (ar, CalculationRate.AUDIO),
        (kr, CalculationRate.CONTROL),
        (ir, CalculationRate.SCALAR),
        (dr, CalculationRate.DEMAND),
        (new, None),
    ]:
        if not should_add:
            continue
        _add_rate_fn(
            cls, rate, params, is_multichannel, channel_count, fixed_channel_count
        )
        if rate is not None:
            valid_calculation_rates.append(rate)
    cls._has_done_flag = bool(has_done_flag)
    cls._is_input = bool(is_input)
    cls._is_output = bool(is_output)
    cls._is_pure = bool(is_pure)
    cls._is_width_first = bool(is_width_first)
    cls._ordered_input_names = {key: param.default for key, param in params.items()}
    cls._unexpanded_input_names = tuple(unexpanded_input_names)
    cls._valid_calculation_rates = tuple(valid_calculation_rates)
    if signal_range is not None:
        cls._signal_range = SignalRange.from_expr(signal_range)
    return cls


def param(
    default: Optional[Union[Default, Missing, float]] = Missing(),
    *,
    check: Check = Check.NONE,
    unexpanded: bool = False,
) -> Param:
    """
    Define a UGen parameter.

    Akin to dataclasses.field.
    """
    return Param(default, check, unexpanded)


def ugen(
    *,
    ar: bool = False,
    kr: bool = False,
    ir: bool = False,
    dr: bool = False,
    new: bool = False,
    has_done_flag: bool = False,
    is_input: bool = False,
    is_multichannel: bool = False,
    is_output: bool = False,
    is_pure: bool = False,
    is_width_first: bool = False,
    channel_count: int = 1,
    fixed_channel_count: bool = False,
    signal_range: Optional[int] = None,
) -> Callable[[Type["UGen"]], Type["UGen"]]:
    """
    Decorate a UGen class.

    Akin to dataclasses.dataclass.
    """

    def wrap(cls: Type[UGen]) -> Type[UGen]:
        return _process_class(
            cls,
            ar=ar,
            kr=kr,
            ir=ir,
            dr=dr,
            new=new,
            has_done_flag=has_done_flag,
            is_input=is_input,
            is_multichannel=is_multichannel,
            is_output=is_output,
            is_pure=is_pure,
            is_width_first=is_width_first,
            channel_count=channel_count,
            fixed_channel_count=fixed_channel_count,
            signal_range=signal_range,
        )

    if is_multichannel and fixed_channel_count:
        raise ValueError
    return wrap


class UGenOperable:

    ### SPECIAL METHODS ###

    def __abs__(self) -> "UGenOperable":
        """
        Gets absolute value of ugen graph.

        .. container:: example

            **Example 1:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.ar()
                >>> result = abs(ugen_graph)
                >>> result
                <UnaryOpUGen.ar(ABSOLUTE_VALUE)[0]>

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

        .. container:: example

            **Example 2:**

            ::

                >>> ugen_graph = supriya.ugens.SinOsc.ar(
                ...     frequency=(440, 442, 443),
                ... )
                >>> result = abs(ugen_graph)
                >>> result
                <UGenVector([<UnaryOpUGen.ar(ABSOLUTE_VALUE)[0]>, <UnaryOpUGen.ar(ABSOLUTE_VALUE)[0]>, <UnaryOpUGen.ar(ABSOLUTE_VALUE)[0]>])>

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
        return UGenOperable._compute_unary_op(self, UnaryOperator.ABSOLUTE_VALUE)

    def __add__(self, expr: "UGenOperand") -> "UGenOperable":
        """
        Adds `expr` to ugen graph.

        .. container:: example

            **Example 1:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar()
                >>> result = ugen_graph + expr
                >>> result
                <BinaryOpUGen.ar(ADDITION)[0]>

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

        .. container:: example

            **Example 2:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ... )
                >>> result = ugen_graph + expr
                >>> result
                <UGenVector([<BinaryOpUGen.ar(ADDITION)[0]>, <BinaryOpUGen.ar(ADDITION)[0]>, <BinaryOpUGen.ar(ADDITION)[0]>])>

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

        .. container:: example

            **Example 3:**

            ::

                >>> ugen_graph = supriya.ugens.Dust.ar(
                ...     density=11.5,
                ... )
                >>> expr = 4
                >>> result = ugen_graph + expr
                >>> result
                <BinaryOpUGen.ar(ADDITION)[0]>

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
        return UGenOperable._compute_binary_op(self, expr, BinaryOperator.ADDITION)

    def __and__(self, expr: "UGenOperand") -> "UGenOperable":
        """
        Computes the bitwise AND of the UGen graph and `expr`.

        .. container:: example

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar()
                >>> result = ugen_graph & expr
                >>> result
                <BinaryOpUGen.ar(BITWISE_AND)[0]>

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 9a5b4d1212b6b7fe299c21a8b1e401cc
                    ugens:
                    -   WhiteNoise.kr: null
                    -   SinOsc.ar:
                            frequency: 440.0
                            phase: 0.0
                    -   BinaryOpUGen(BITWISE_AND).ar:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar[0]
        """
        return UGenOperable._compute_binary_op(self, expr, BinaryOperator.BITWISE_AND)

    def __ceil__(self) -> "UGenOperable":
        """
        Calculates the ceiling of ugen graph.

        ::

            >>> import math
            >>> source = supriya.ugens.DC.ar(source=0.5)
            >>> operation = math.ceil(source)
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

    def __div__(self, expr: "UGenOperand") -> "UGenOperable":
        """
        Divides ugen graph by `expr`.

        .. container:: example

            **Example 1:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar()
                >>> result = ugen_graph / expr
                >>> result
                <BinaryOpUGen.ar(FLOAT_DIVISION)[0]>

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

        .. container:: example

            **Example 2:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ... )
                >>> result = ugen_graph / expr
                >>> result
                <UGenVector([<BinaryOpUGen.ar(FLOAT_DIVISION)[0]>, <BinaryOpUGen.ar(FLOAT_DIVISION)[0]>, <BinaryOpUGen.ar(FLOAT_DIVISION)[0]>])>

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

        .. container:: example

            **Example 3:**

            ::

                >>> ugen_graph = supriya.ugens.Dust.ar(
                ...     density=11.5,
                ... )
                >>> expr = 4
                >>> result = ugen_graph / expr
                >>> result
                <BinaryOpUGen.ar(FLOAT_DIVISION)[0]>

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
        return UGenOperable._compute_binary_op(
            self, expr, BinaryOperator.FLOAT_DIVISION
        )

    def __floor__(self) -> "UGenOperable":
        """
        Calculates the floor of ugen graph.

        ::

            >>> import math
            >>> source = supriya.ugens.DC.ar(source=0.5)
            >>> operation = math.floor(source)
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

    def __graph__(self):
        """
        Gets Graphviz representation of ugen graph.

        Returns GraphvizGraph instance.
        """
        synthdef = self._clone()
        result = synthdef.__graph__()
        return result

    def __ge__(self, expr: "UGenOperand") -> "UGenOperable":
        """
        Tests if ugen graph if greater than or equal to `expr`.

        .. container:: example

            **Example 1:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar()
                >>> result = ugen_graph >= expr
                >>> result
                <BinaryOpUGen.ar(GREATER_THAN_OR_EQUAL)[0]>

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

        .. container:: example

            **Example 2:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ... )
                >>> result = ugen_graph >= expr
                >>> result
                <UGenVector([<BinaryOpUGen.ar(GREATER_THAN_OR_EQUAL)[0]>, <BinaryOpUGen.ar(GREATER_THAN_OR_EQUAL)[0]>, <BinaryOpUGen.ar(GREATER_THAN_OR_EQUAL)[0]>])>

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

        .. container:: example

            **Example 3:**

            ::

                >>> ugen_graph = supriya.ugens.Dust.ar(
                ...     density=11.5,
                ... )
                >>> expr = 4
                >>> result = ugen_graph >= expr
                >>> result
                <BinaryOpUGen.ar(GREATER_THAN_OR_EQUAL)[0]>

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
        return UGenOperable._compute_binary_op(
            self, expr, BinaryOperator.GREATER_THAN_OR_EQUAL
        )

    def __gt__(self, expr: "UGenOperand") -> "UGenOperable":
        """
        Tests if ugen graph if greater than `expr`.

        .. container:: example

            **Example 1:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar()
                >>> result = ugen_graph > expr
                >>> result
                <BinaryOpUGen.ar(GREATER_THAN)[0]>

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

        .. container:: example

            **Example 2:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ... )
                >>> result = ugen_graph > expr
                >>> result
                <UGenVector([<BinaryOpUGen.ar(GREATER_THAN)[0]>, <BinaryOpUGen.ar(GREATER_THAN)[0]>, <BinaryOpUGen.ar(GREATER_THAN)[0]>])>

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

        .. container:: example

            **Example 3:**

            ::

                >>> ugen_graph = supriya.ugens.Dust.ar(
                ...     density=11.5,
                ... )
                >>> expr = 4
                >>> result = ugen_graph > expr
                >>> result
                <BinaryOpUGen.ar(GREATER_THAN)[0]>

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
        return UGenOperable._compute_binary_op(self, expr, BinaryOperator.GREATER_THAN)

    def __le__(self, expr: "UGenOperand") -> "UGenOperable":
        """
        Tests if ugen graph if less than or equal to `expr`.

        .. container:: example

            **Example 1:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar()
                >>> result = ugen_graph <= expr
                >>> result
                <BinaryOpUGen.ar(LESS_THAN_OR_EQUAL)[0]>

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

        .. container:: example

            **Example 2:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ... )
                >>> result = ugen_graph <= expr
                >>> result
                <UGenVector([<BinaryOpUGen.ar(LESS_THAN_OR_EQUAL)[0]>, <BinaryOpUGen.ar(LESS_THAN_OR_EQUAL)[0]>, <BinaryOpUGen.ar(LESS_THAN_OR_EQUAL)[0]>])>

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

        .. container:: example

            **Example 3:**

            ::

                >>> ugen_graph = supriya.ugens.Dust.ar(
                ...     density=11.5,
                ... )
                >>> expr = 4
                >>> result = ugen_graph <= expr
                >>> result
                <BinaryOpUGen.ar(LESS_THAN_OR_EQUAL)[0]>

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
        return UGenOperable._compute_binary_op(
            self, expr, BinaryOperator.LESS_THAN_OR_EQUAL
        )

    def __len__(self) -> int:
        raise NotImplementedError

    def __lt__(self, expr: "UGenOperand") -> "UGenOperable":
        """
        Tests if ugen graph if less than `expr`.

        .. container:: example

            **Example 1:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar()
                >>> result = ugen_graph < expr
                >>> result
                <BinaryOpUGen.ar(LESS_THAN)[0]>

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

        .. container:: example

            **Example 2:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ... )
                >>> result = ugen_graph < expr
                >>> result
                <UGenVector([<BinaryOpUGen.ar(LESS_THAN)[0]>, <BinaryOpUGen.ar(LESS_THAN)[0]>, <BinaryOpUGen.ar(LESS_THAN)[0]>])>

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

        .. container:: example

            **Example 3:**

            ::

                >>> ugen_graph = supriya.ugens.Dust.ar(
                ...     density=11.5,
                ... )
                >>> expr = 4
                >>> result = ugen_graph < expr
                >>> result
                <BinaryOpUGen.ar(LESS_THAN)[0]>

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
        return UGenOperable._compute_binary_op(self, expr, BinaryOperator.LESS_THAN)

    def __mod__(self, expr: "UGenOperand") -> "UGenOperable":
        """
        Gets modulo of ugen graph and `expr`.

        .. container:: example

            **Example 1:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar()
                >>> result = ugen_graph % expr
                >>> result
                <BinaryOpUGen.ar(MODULO)[0]>

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

        .. container:: example

            **Example 2:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ... )
                >>> result = ugen_graph % expr
                >>> result
                <UGenVector([<BinaryOpUGen.ar(MODULO)[0]>, <BinaryOpUGen.ar(MODULO)[0]>, <BinaryOpUGen.ar(MODULO)[0]>])>

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

        .. container:: example

            **Example 3:**

            ::

                >>> ugen_graph = supriya.ugens.Dust.ar(
                ...     density=11.5,
                ... )
                >>> expr = 4
                >>> result = ugen_graph % expr
                >>> result
                <BinaryOpUGen.ar(MODULO)[0]>

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
        return UGenOperable._compute_binary_op(self, expr, BinaryOperator.MODULO)

    def __mul__(self, expr: "UGenOperand") -> "UGenOperable":
        """
        Multiplies ugen graph by `expr`.

        .. container:: example

            **Example 1:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar()
                >>> result = ugen_graph * expr
                >>> result
                <BinaryOpUGen.ar(MULTIPLICATION)[0]>

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

        .. container:: example

            **Example 2:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ... )
                >>> result = ugen_graph * expr
                >>> result
                <UGenVector([<BinaryOpUGen.ar(MULTIPLICATION)[0]>, <BinaryOpUGen.ar(MULTIPLICATION)[0]>, <BinaryOpUGen.ar(MULTIPLICATION)[0]>])>

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

        .. container:: example

            **Example 3:**

            ::

                >>> ugen_graph = supriya.ugens.Dust.ar(
                ...     density=11.5,
                ... )
                >>> expr = 4
                >>> result = ugen_graph * expr
                >>> result
                <BinaryOpUGen.ar(MULTIPLICATION)[0]>

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
        return UGenOperable._compute_binary_op(
            self, expr, BinaryOperator.MULTIPLICATION
        )

    def __neg__(self) -> "UGenOperable":
        """
        Negates ugen graph.

        .. container:: example

            **Example 1:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.ar()
                >>> result = -ugen_graph
                >>> result
                <UnaryOpUGen.ar(NEGATIVE)[0]>

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

        .. container:: example

            **Example 2:**

            ::

                >>> ugen_graph = supriya.ugens.SinOsc.ar(
                ...     frequency=(440, 442, 443),
                ... )
                >>> result = -ugen_graph
                >>> result
                <UGenVector([<UnaryOpUGen.ar(NEGATIVE)[0]>, <UnaryOpUGen.ar(NEGATIVE)[0]>, <UnaryOpUGen.ar(NEGATIVE)[0]>])>

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
        return UGenOperable._compute_unary_op(self, UnaryOperator.NEGATIVE)

    def __or__(self, expr: "UGenOperand") -> "UGenOperable":
        """
        Computes the bitwise OR of the UGen graph and `expr`.

        .. container:: example

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar()
                >>> result = ugen_graph | expr
                >>> result
                <BinaryOpUGen.ar(BITWISE_OR)[0]>

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 333e2e7362f86138866f3f2a160f77dd
                    ugens:
                    -   WhiteNoise.kr: null
                    -   SinOsc.ar:
                            frequency: 440.0
                            phase: 0.0
                    -   BinaryOpUGen(BITWISE_OR).ar:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar[0]
        """
        return UGenOperable._compute_binary_op(self, expr, BinaryOperator.BITWISE_OR)

    def __pow__(self, expr: "UGenOperand") -> "UGenOperable":
        """
        Raises ugen graph to the power of `expr`.

        .. container:: example

            **Example 1:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar()
                >>> result = ugen_graph ** expr
                >>> result
                <BinaryOpUGen.ar(POWER)[0]>

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

        .. container:: example

            **Example 2:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ... )
                >>> result = ugen_graph ** expr
                >>> result
                <UGenVector([<BinaryOpUGen.ar(POWER)[0]>, <BinaryOpUGen.ar(POWER)[0]>, <BinaryOpUGen.ar(POWER)[0]>])>

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

        .. container:: example

            **Example 3:**

            ::

                >>> ugen_graph = supriya.ugens.Dust.ar(
                ...     density=11.5,
                ... )
                >>> expr = 4
                >>> result = ugen_graph ** expr
                >>> result
                <BinaryOpUGen.ar(POWER)[0]>

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
        return UGenOperable._compute_binary_op(self, expr, BinaryOperator.POWER)

    def __rpow__(self, expr: "UGenOperand") -> "UGenOperable":
        """
        Raises `expr` to the power of ugen graph.

        .. container:: example

            **Example 1:**

            ::

                >>> expr = 1.5
                >>> ugen_graph = supriya.ugens.SinOsc.ar()
                >>> result = expr ** ugen_graph
                >>> result
                <BinaryOpUGen.ar(POWER)[0]>

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

        .. container:: example

            **Example 2:**

            ::

                >>> expr = [220, 330]
                >>> ugen_graph = supriya.ugens.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ... )
                >>> result = expr ** ugen_graph
                >>> result
                <UGenVector([<BinaryOpUGen.ar(POWER)[0]>, <BinaryOpUGen.ar(POWER)[0]>, <BinaryOpUGen.ar(POWER)[0]>])>

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
        return UGenOperable._compute_binary_op(expr, self, BinaryOperator.POWER)

    def __radd__(self, expr: "UGenOperand") -> "UGenOperable":
        """
        Adds ugen graph to `expr`.

        .. container:: example

            **Example 1:**

            ::

                >>> expr = 1.5
                >>> ugen_graph = supriya.ugens.SinOsc.ar()
                >>> result = expr + ugen_graph
                >>> result
                <BinaryOpUGen.ar(ADDITION)[0]>

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

        .. container:: example

            **Example 2:**

            ::

                >>> expr = [220, 330]
                >>> ugen_graph = supriya.ugens.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ... )
                >>> result = expr + ugen_graph
                >>> result
                <UGenVector([<BinaryOpUGen.ar(ADDITION)[0]>, <BinaryOpUGen.ar(ADDITION)[0]>, <BinaryOpUGen.ar(ADDITION)[0]>])>

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
        return UGenOperable._compute_binary_op(expr, self, BinaryOperator.ADDITION)

    def __rdiv__(self, expr: "UGenOperand") -> "UGenOperable":
        """
        Divides `expr` by ugen graph.

        .. container:: example

            **Example 1:**

            ::

                >>> expr = 1.5
                >>> ugen_graph = supriya.ugens.SinOsc.ar()
                >>> result = expr / ugen_graph
                >>> result
                <BinaryOpUGen.ar(FLOAT_DIVISION)[0]>

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

        .. container:: example

            **Example 2:**

            ::

                >>> expr = [220, 330]
                >>> ugen_graph = supriya.ugens.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ... )
                >>> result = expr / ugen_graph
                >>> result
                <UGenVector([<BinaryOpUGen.ar(FLOAT_DIVISION)[0]>, <BinaryOpUGen.ar(FLOAT_DIVISION)[0]>, <BinaryOpUGen.ar(FLOAT_DIVISION)[0]>])>

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
        return UGenOperable._compute_binary_op(
            expr, self, BinaryOperator.FLOAT_DIVISION
        )

    def __rmod__(self, expr: "UGenOperand") -> "UGenOperable":
        """
        Gets modulo of `expr` and ugen graph.

        .. container:: example

            **Example 1:**

            ::

                >>> expr = 1.5
                >>> ugen_graph = supriya.ugens.SinOsc.ar()
                >>> result = expr % ugen_graph
                >>> result
                <BinaryOpUGen.ar(FLOAT_DIVISION)[0]>

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

        .. container:: example

            **Example 2:**

            ::

                >>> expr = [220, 330]
                >>> ugen_graph = supriya.ugens.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ... )
                >>> result = expr % ugen_graph
                >>> result
                <UGenVector([<BinaryOpUGen.ar(FLOAT_DIVISION)[0]>, <BinaryOpUGen.ar(FLOAT_DIVISION)[0]>, <BinaryOpUGen.ar(FLOAT_DIVISION)[0]>])>

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
        return UGenOperable._compute_binary_op(
            expr, self, BinaryOperator.FLOAT_DIVISION
        )

    def __rmul__(self, expr: "UGenOperand") -> "UGenOperable":
        """
        Multiplies `expr` by ugen graph.

        .. container:: example

            **Example 1:**

            ::

                >>> expr = 1.5
                >>> ugen_graph = supriya.ugens.SinOsc.ar()
                >>> result = expr * ugen_graph
                >>> result
                <BinaryOpUGen.ar(MULTIPLICATION)[0]>

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

        .. container:: example

            **Example 2:**

            ::

                >>> expr = [220, 330]
                >>> ugen_graph = supriya.ugens.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ... )
                >>> result = expr * ugen_graph
                >>> result
                <UGenVector([<BinaryOpUGen.ar(MULTIPLICATION)[0]>, <BinaryOpUGen.ar(MULTIPLICATION)[0]>, <BinaryOpUGen.ar(MULTIPLICATION)[0]>])>

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
        return UGenOperable._compute_binary_op(
            expr, self, BinaryOperator.MULTIPLICATION
        )

    def __rsub__(self, expr: "UGenOperand") -> "UGenOperable":
        """
        Subtracts ugen graph from `expr`.

        .. container:: example

            **Example 1:**

            ::

                >>> expr = 1.5
                >>> ugen_graph = supriya.ugens.SinOsc.ar()
                >>> result = expr - ugen_graph
                >>> result
                <BinaryOpUGen.ar(SUBTRACTION)[0]>

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

        .. container:: example

            **Example 2:**

            ::

                >>> expr = [220, 330]
                >>> ugen_graph = supriya.ugens.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ... )
                >>> result = expr - ugen_graph
                >>> result
                <UGenVector([<BinaryOpUGen.ar(SUBTRACTION)[0]>, <BinaryOpUGen.ar(SUBTRACTION)[0]>, <BinaryOpUGen.ar(SUBTRACTION)[0]>])>

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
        return UGenOperable._compute_binary_op(expr, self, BinaryOperator.SUBTRACTION)

    def __str__(self):
        """
        Gets string representation of ugen graph.

        .. container:: example

            ::

                >>> ugen_graph = supriya.ugens.SinOsc.ar()
                >>> print(str(ugen_graph))
                synthdef:
                    name: c9b0ed62d4e0666b74166ff5ec09abe4
                    ugens:
                    -   SinOsc.ar:
                            frequency: 440.0
                            phase: 0.0

        .. container:: example

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

    def __sub__(self, expr: "UGenOperand") -> "UGenOperable":
        """
        Subtracts `expr` from ugen graph.

        .. container:: example

            **Example 1:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar()
                >>> result = ugen_graph - expr
                >>> result
                <BinaryOpUGen.ar(SUBTRACTION)[0]>

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

        .. container:: example

            **Example 2:**

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ... )
                >>> result = ugen_graph - expr
                >>> result
                <UGenVector([<BinaryOpUGen.ar(SUBTRACTION)[0]>, <BinaryOpUGen.ar(SUBTRACTION)[0]>, <BinaryOpUGen.ar(SUBTRACTION)[0]>])>

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

        .. container:: example

            **Example 3:**

            ::

                >>> ugen_graph = supriya.ugens.Dust.ar(
                ...     density=11.5,
                ... )
                >>> expr = 4
                >>> result = ugen_graph - expr
                >>> result
                <BinaryOpUGen.ar(SUBTRACTION)[0]>

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
        return UGenOperable._compute_binary_op(self, expr, BinaryOperator.SUBTRACTION)

    def __xor__(self, expr: "UGenOperand") -> "UGenOperable":
        """
        Computes the bitwise XOR of the UGen graph and `expr`.

        .. container:: example

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.kr()
                >>> expr = supriya.ugens.SinOsc.ar()
                >>> result = ugen_graph ^ expr
                >>> result
                <BinaryOpUGen.ar(BITWISE_XOR)[0]>

            ::

                >>> supriya.graph(result)  # doctest: +SKIP

            ::

                >>> print(result)
                synthdef:
                    name: 355f2c7fa510863b921bb8c28bc4a682
                    ugens:
                    -   WhiteNoise.kr: null
                    -   SinOsc.ar:
                            frequency: 440.0
                            phase: 0.0
                    -   BinaryOpUGen(BITWISE_XOR).ar:
                            left: WhiteNoise.kr[0]
                            right: SinOsc.ar[0]
        """
        return UGenOperable._compute_binary_op(self, expr, BinaryOperator.BITWISE_XOR)

    __truediv__ = __div__
    __rtruediv__ = __rdiv__

    ### PRIVATE METHODS ###

    def _clone(self):
        def recurse(uuid, ugen, all_ugens):
            if hasattr(ugen, "inputs"):
                for input_ in ugen.inputs:
                    if not isinstance(input_, OutputProxy):
                        continue
                    input_ = input_.source
                    input_._uuid = uuid
                    recurse(uuid, input_, all_ugens)
            ugen._uuid = uuid
            if ugen not in all_ugens:
                all_ugens.append(ugen)

        from . import SynthDefBuilder

        builder = SynthDefBuilder()
        ugens = copy.deepcopy(self)
        if not isinstance(ugens, UGenVector):
            ugens = [ugens]
        all_ugens = []
        for u in ugens:
            if isinstance(u, OutputProxy):
                u = u.source
            recurse(builder._uuid, u, all_ugens)
        for u in all_ugens:
            if isinstance(u, UGen):
                builder._add_ugens(u)
            else:
                builder._add_parameter(u)
        return builder.build(optimize=False)

    @staticmethod
    def _compute_binary_op(left, right, operator) -> "UGenOperable":
        result: List[Union[OutputProxy, float]] = []
        if not isinstance(left, Sequence):
            left = (left,)
        if not isinstance(right, Sequence):
            right = (right,)
        dictionary = {"left": left, "right": right}
        operator = BinaryOperator.from_expr(operator)
        special_index = operator.value
        for expanded_dict in UGen._expand_dictionary(dictionary):
            left = expanded_dict["left"]
            right = expanded_dict["right"]
            ugen = BinaryOpUGen._new_single(
                calculation_rate=max(
                    [
                        CalculationRate.from_expr(left),
                        CalculationRate.from_expr(right),
                    ]
                ),
                left=left,
                right=right,
                special_index=special_index,
            )
            result.extend(ugen if not isinstance(ugen, (float, int)) else [ugen])
        if len(result) == 1:
            # TODO: remove cast(...)
            return cast(UGenOperable, result[0])
        return UGenVector(*result)

    def _compute_ugen_map(self, map_ugen, **kwargs):
        sources = []
        ugens = []
        if len(self) == 1:
            sources = [self]
        else:
            sources = self
        for source in sources:
            method = UGen._get_method_for_rate(map_ugen, source)
            ugen = method(source=source, **kwargs)
            ugens.extend(ugen)
        if 1 < len(ugens):
            return UGenVector(*ugens)
        elif len(ugens) == 1:
            return ugens[0].source
        return []

    @staticmethod
    def _compute_unary_op(source, operator) -> "UGenOperable":
        result: List[Union[OutputProxy, float]] = []
        if not isinstance(source, Sequence):
            source = (source,)
        operator = UnaryOperator.from_expr(operator)
        special_index = operator.value
        for single_source in source:
            calculation_rate = CalculationRate.from_expr(single_source)
            ugen = UnaryOpUGen._new_single(
                calculation_rate=calculation_rate,
                source=single_source,
                special_index=special_index,
            )
            result.extend(ugen if not isinstance(ugen, (float, int)) else [ugen])
        if len(result) == 1:
            # TODO: remove cast(...)
            return cast(UGenOperable, result[0])
        return UGenVector(*result)

    def _get_output_proxy(self, i):
        if isinstance(i, int):
            if not (0 <= i < len(self)):
                raise IndexError(i, len(self))
            return OutputProxy(source=self, output_index=i)
        indices = i.indices(len(self))
        if not (0 <= indices[0] <= indices[1] <= len(self)):
            raise IndexError(i, indices, len(self))
        output_proxies = (
            OutputProxy(source=self, output_index=i) for i in range(*indices)
        )
        return UGenVector(*output_proxies)

    ### PUBLIC METHODS ###

    def absdiff(self, expr: "UGenOperand") -> "UGenOperable":
        """
        Calculates absolute difference between ugen graph and `expr`.

        .. container:: example

            ::

                >>> ugen_graph = supriya.ugens.SinOsc.ar()
                >>> expr = supriya.ugens.WhiteNoise.kr()
                >>> result = ugen_graph.absdiff(expr)

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

    def amplitude_to_db(self) -> "UGenOperable":
        """
        Converts ugen graph from amplitude to decibels.

        .. container:: example

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

    def clip(
        self,
        minimum: Union[SupportsFloat, "UGenOperable"],
        maximum: Union[SupportsFloat, "UGenOperable"],
    ) -> "UGenOperable":
        """
        Clips ugen graph.

        .. container:: example

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

        .. container:: example

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
        from . import Clip

        return self._compute_ugen_map(Clip, minimum=minimum, maximum=maximum)

    def cubed(self) -> "UGenOperable":
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

    def db_to_amplitude(self) -> "UGenOperable":
        """
        Converts ugen graph from decibels to amplitude.

        .. container:: example

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

    def digit_value(self) -> "UGenOperable":
        return self._compute_unary_op(self, UnaryOperator.DIGIT_VALUE)

    def distort(self) -> "UGenOperable":
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

    def exponential(self) -> "UGenOperable":
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

    def fractional_part(self) -> "UGenOperable":
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

    def hanning_window(self) -> "UGenOperable":
        """
        Calculates Hanning-window of ugen graph.

        .. container:: example

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

    def hz_to_midi(self) -> "UGenOperable":
        """
        Converts ugen graph from Hertz to midi note number.

        .. container:: example

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

    def hz_to_octave(self) -> "UGenOperable":
        """
        Converts ugen graph from Hertz to octave number.

        .. container:: example

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

    def is_equal_to(self, expr: "UGenOperand") -> "UGenOperable":
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

    def is_not_equal_to(self, expr: "UGenOperand") -> "UGenOperable":
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

    def lagged(self, lag_time=0.5) -> "UGenOperable":
        """
        Lags ugen graph.

        .. container:: example

            ::

                >>> ugen_graph = supriya.ugens.WhiteNoise.ar()
                >>> result = ugen_graph.lagged(0.5)

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

        .. container:: example

            ::

                >>> ugen_graph = supriya.ugens.SinOsc.ar(
                ...     frequency=[440, 442, 443],
                ... )
                >>> result = ugen_graph.lagged(0.5)

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
        from . import Lag

        return self._compute_ugen_map(Lag, lag_time=lag_time)

    def log(self) -> "UGenOperable":
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

    def log2(self) -> "UGenOperable":
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

    def log10(self) -> "UGenOperable":
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

    def max(self, expr: "UGenOperand") -> "UGenOperable":
        """
        Calculates maximum between ugen graph and `expr`.

        ::

            >>> left = supriya.ugens.SinOsc.ar()
            >>> right = supriya.ugens.WhiteNoise.kr()
            >>> operation = left.max(right)
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

    def midi_to_hz(self) -> "UGenOperable":
        """
        Converts ugen graph from midi note number to Hertz.

        .. container:: example

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

    def min(self, expr: "UGenOperand") -> "UGenOperable":
        """
        Calculates minimum between ugen graph and `expr`.

        ::

            >>> left = supriya.ugens.SinOsc.ar()
            >>> right = supriya.ugens.WhiteNoise.kr()
            >>> operation = left.min(right)
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

    def octave_to_hz(self) -> "UGenOperable":
        """
        Converts ugen graph from octave number to Hertz.

        .. container:: example

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

    def ratio_to_semitones(self) -> "UGenOperable":
        """
        Converts ugen graph from frequency ratio to semitone distance.

        .. container:: example

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

    def rectangle_window(self) -> "UGenOperable":
        """
        Calculates rectangle-window of ugen graph.

        .. container:: example

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

    def reciprocal(self) -> "UGenOperable":
        """
        Calculates reciprocal of ugen graph.

        .. container:: example

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

    def s_curve(self) -> "UGenOperable":
        """
        Calculates S-curve of ugen graph.

        .. container:: example

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
    ) -> "UGenOperable":
        """
        Scales ugen graph from `input_minimum` and `input_maximum` to `output_minimum` and `output_maximum`.

        .. container:: example

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

        .. container:: example

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
        from . import LinExp, LinLin

        return self._compute_ugen_map(
            LinExp if exponential else LinLin,
            input_minimum=input_minimum,
            input_maximum=input_maximum,
            output_minimum=output_minimum,
            output_maximum=output_maximum,
        )

    def semitones_to_ratio(self) -> "UGenOperable":
        """
        Converts ugen graph from semitone distance to frequency ratio.

        .. container:: example

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

    def sign(self) -> "UGenOperable":
        """
        Calculates sign of ugen graph.

        .. container:: example

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

    def softclip(self) -> "UGenOperable":
        """
        Distorts ugen graph non-linearly.
        """
        return self._compute_unary_op(self, UnaryOperator.SOFTCLIP)

    def sqrt(self) -> "UGenOperable":
        """
        Calculates square root of ugen graph.
        """
        return self._compute_unary_op(self, UnaryOperator.SQUARE_ROOT)

    def squared(self) -> "UGenOperable":
        """
        Calculates square of ugen graph.
        """
        return self._compute_unary_op(self, UnaryOperator.SQUARED)

    def sum(self) -> "UGenOperable":
        """
        Sums ugen graph.

        .. container:: example

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

        .. container:: example

            **Example 2:**

            ::

                >>> ugen_graph = supriya.ugens.SinOsc.ar(frequency=[440, 442, 443])
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
        from . import Mix

        return Mix.new(self)

    def tanh(self) -> "UGenOperable":
        """
        Calculates hyperbolic tangent of ugen graph.

        .. container:: example

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

    def transpose(self, semitones) -> "UGenOperable":
        """
        Transposes ugen graph by `semitones`.

        .. container:: example

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

    def triangle_window(self) -> "UGenOperable":
        """
        Calculates triangle-window of ugen graph.

        .. container:: example

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

    def welch_window(self) -> "UGenOperable":
        """
        Calculates Welch-window of ugen graph.

        .. container:: example

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

    @property
    def signal_range(self):
        raise NotImplementedError


class UGenSerializable(Protocol):
    def serialize(self) -> Sequence[Union[SupportsFloat, "OutputProxy"]]:
        pass


class UGenVector(UGenOperable, Sequence):

    ### INITIALIZER ###

    def __init__(self, *ugens):
        self._ugens = tuple(ugens)

    ### SPECIAL METHODS ###

    def __getitem__(self, i):
        return self.ugens[i]

    def __len__(self):
        return len(self.ugens)

    def __repr__(self):
        return f"<{type(self).__name__}([{', '.join(repr(x) for x in self)}])>"

    ### PUBLIC PROPERTIES ###

    @property
    def signal_range(self):
        return max(_.signal_range for _ in self)

    @property
    def ugens(self):
        return self._ugens


class OutputProxy(UGenOperable):
    ### INITIALIZER ###

    def __init__(self, *, source: "UGen", output_index: int) -> None:
        self._output_index = output_index
        self._source = source

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if not isinstance(expr, type(self)):
            return False
        if self._output_index != expr._output_index:
            return False
        if self._source != expr._source:
            return False
        return True

    def __hash__(self) -> int:
        hash_values = (type(self), self._output_index, self._source)
        return hash(hash_values)

    def __iter__(self):
        yield self

    def __len__(self) -> int:
        return 1

    def __repr__(self) -> str:
        return repr(self.source).replace(">", f"[{self.output_index}]>")

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
    def output_index(self) -> int:
        return self._output_index

    @property
    def signal_range(self) -> SignalRange:
        return self.source.signal_range

    @property
    def source(self):
        return self._source


class UGen(UGenOperable):
    """
    A UGen.
    """

    ### CLASS VARIABLES ###

    _default_channel_count = 1

    _has_settable_channel_count = False

    _has_done_flag = False

    _is_input = False

    _is_output = False

    _is_pure = False

    _is_width_first = False

    _ordered_input_names: Dict[
        str, Union[Default, Missing, SupportsFloat, str, None]
    ] = {}

    _signal_range: int = SignalRange.BIPOLAR

    _unexpanded_input_names: Tuple[str, ...] = ()

    _valid_calculation_rates: Tuple[int, ...] = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        calculation_rate: CalculationRateLike = None,
        special_index: int = 0,
        **kwargs,
    ) -> None:
        calculation_rate_ = CalculationRate.from_expr(calculation_rate)
        if self._valid_calculation_rates:
            assert calculation_rate_ in self._valid_calculation_rates
        calculation_rate_, kwargs = self._postprocess_kwargs(
            calculation_rate=calculation_rate_, **kwargs
        )
        self._calculation_rate = calculation_rate_
        self._inputs: List[SupportsFloat] = []
        self._input_names: List[str] = []
        self._special_index = special_index
        ugenlike_prototype = (UGen, Parameter)
        for input_name in self._ordered_input_names:
            input_value = None
            if input_name in kwargs:
                input_value = kwargs.pop(input_name)
                # print(type(self).__name__, input_name, type(input_value))
            if isinstance(input_value, ugenlike_prototype):
                assert len(input_value) == 1
                input_value = input_value[0]
            else:
                try:
                    input_value = float(input_value)  # type: ignore
                except TypeError:
                    pass
            if self._is_unexpanded_input_name(input_name):
                if not isinstance(input_value, Sequence):
                    input_value = (input_value,)
                if isinstance(input_value, Sequence):
                    input_value = tuple(input_value)
                elif not self._is_valid_input(input_value):
                    raise ValueError(input_name, input_value)
            elif not self._is_valid_input(input_value):
                raise ValueError(input_name, input_value)
            self._configure_input(input_name, input_value)
        if kwargs:
            raise ValueError(kwargs)
        assert all(isinstance(_, (OutputProxy, float)) for _ in self.inputs)
        self._validate_inputs()
        self._uuid = None
        if SynthDefBuilder._active_builders:
            builder = SynthDefBuilder._active_builders[-1]
            self._uuid = builder._uuid
            builder._add_ugens(self)
        self._check_inputs_share_same_uuid()

    ### SPECIAL METHODS ###

    def __getitem__(self, i):
        """
        Gets output proxy at index `i`.

        ::

            >>> ugen = supriya.ugens.SinOsc.ar().source
            >>> ugen[0]
            <SinOsc.ar()[0]>

        Returns output proxy.
        """
        return self._get_output_proxy(i)

    def __len__(self):
        """
        Gets number of ugen outputs.

        Returns integer.
        """
        return getattr(self, "_channel_count", self._default_channel_count)

    def __repr__(self):
        """
        Gets interpreter representation of ugen.

        ::

            >>> ugen = supriya.ugens.SinOsc.ar().source
            >>> repr(ugen)
            '<SinOsc.ar()>'

        ::

            >>> ugen = supriya.ugens.WhiteNoise.kr().source
            >>> repr(ugen)
            '<WhiteNoise.kr()>'

        ::

            >>> ugen = supriya.ugens.Rand.ir().source
            >>> repr(ugen)
            '<Rand.ir()>'

        Returns string.
        """
        return f"<{type(self).__name__}.{self.calculation_rate.token}()>"

    ### PRIVATE METHODS ###

    @staticmethod
    def _as_audio_rate_input(expr):
        from . import DC, K2A, Silence

        if isinstance(expr, (int, float)):
            if expr == 0:
                return Silence.ar()
            return DC.ar(expr)
        elif isinstance(expr, (UGen, OutputProxy)):
            if expr.calculation_rate == CalculationRate.AUDIO:
                return expr
            return K2A.ar(source=expr)
        elif isinstance(expr, Iterable):
            return UGenVector(*(UGen._as_audio_rate_input(x) for x in expr))
        raise ValueError(expr)

    def _add_constant_input(self, name, value):
        self._inputs.append(float(value))
        self._input_names.append(name)

    def _add_ugen_input(self, name, ugen, output_index=None):
        if isinstance(ugen, OutputProxy):
            output_proxy = ugen
        else:
            output_proxy = OutputProxy(source=ugen, output_index=output_index)
        self._inputs.append(output_proxy)
        self._input_names.append(name)

    def _check_inputs_share_same_uuid(self):
        for input_ in self.inputs:
            if not isinstance(input_, OutputProxy):
                continue
            if input_.source._uuid != self._uuid:
                message = "UGen input in different scope: {!r}"
                message = message.format(input_.source)
                raise ValueError(message)

    def _check_rate_same_as_first_input_rate(self):
        first_input_rate = CalculationRate.from_expr(self.inputs[0])
        return self.calculation_rate == first_input_rate

    def _check_range_of_inputs_at_audio_rate(self, start=None, stop=None):
        if self.calculation_rate != CalculationRate.AUDIO:
            return True
        for input_ in self.inputs[start:stop]:
            calculation_rate = CalculationRate.from_expr(input_)
            if calculation_rate != CalculationRate.AUDIO:
                return False
        return True

    def _configure_input(self, name, value):
        ugen_prototype = (OutputProxy, Parameter, UGen)
        if hasattr(value, "__float__"):
            self._add_constant_input(name, float(value))
        elif isinstance(value, ugen_prototype):
            self._add_ugen_input(name, value._get_source(), value._get_output_number())
        elif isinstance(value, Sequence):
            if name not in self._unexpanded_input_names:
                raise ValueError(name, self._unexpanded_input_names)
            for i, x in enumerate(value):
                if hasattr(x, "__float__"):
                    self._add_constant_input((name, i), float(x))
                elif isinstance(x, ugen_prototype):
                    self._add_ugen_input(
                        (name, i), x._get_source(), x._get_output_number()
                    )
                else:
                    raise Exception("{!r} {!r}".format(value, x))
        else:
            raise ValueError(f"Invalid input: {value!r}")

    @classmethod
    def _expand_dictionary(cls, kwargs, unexpanded_input_names=()):
        """
        Expands a dictionary into multichannel dictionaries.

        ::

            >>> dictionary = {"foo": 0, "bar": [1, 2], "baz": [3, 4, 5]}
            >>> result = UGen._expand_dictionary(dictionary)
            >>> for x in result:
            ...     sorted(x.items())
            ...
            [('bar', 1), ('baz', 3), ('foo', 0)]
            [('bar', 2), ('baz', 4), ('foo', 0)]
            [('bar', 1), ('baz', 5), ('foo', 0)]

        ::

            >>> dictionary = {"bus": [8, 9], "source": [1, 2, 3]}
            >>> result = UGen._expand_dictionary(
            ...     dictionary,
            ...     unexpanded_input_names=("source",),
            ... )
            >>> for x in result:
            ...     sorted(x.items())
            ...
            [('bus', 8), ('source', [1, 2, 3])]
            [('bus', 9), ('source', [1, 2, 3])]
        """
        size = 0
        for k, v in kwargs.items():
            if isinstance(v, (OutputProxy, str)) or not hasattr(v, "__len__"):
                continue
            elif k in unexpanded_input_names:
                if all(
                    hasattr(x, "__len__") and not isinstance(x, OutputProxy) for x in v
                ):
                    size = max(size, len(v))
                else:
                    continue
            else:
                size = max(size, len(v))
        if not size:
            return [kwargs]
        results = []
        for i in range(size):
            new_kwargs = {}
            for k, v in kwargs.items():
                if isinstance(v, (OutputProxy, str)) or not hasattr(v, "__len__"):
                    new_kwargs[k] = v
                elif k in unexpanded_input_names:
                    if all(
                        hasattr(x, "__len__") and not isinstance(x, OutputProxy)
                        for x in v
                    ):
                        new_kwargs[k] = v[i % len(v)]
                    else:
                        new_kwargs[k] = v
                else:
                    try:
                        new_kwargs[k] = v[i % len(v)]
                    except TypeError:
                        new_kwargs[k] = v
            results.extend(cls._expand_dictionary(new_kwargs, unexpanded_input_names))
        return results

    def _get_done_action(self):
        if "done_action" not in self._ordered_input_names:
            return None
        return DoneAction.from_expr(int(self.done_action))

    @staticmethod
    def _get_method_for_rate(cls, calculation_rate):
        calculation_rate = CalculationRate.from_expr(calculation_rate)
        if calculation_rate == CalculationRate.AUDIO:
            return cls.ar
        elif calculation_rate == CalculationRate.CONTROL:
            return cls.kr
        elif calculation_rate == CalculationRate.SCALAR:
            if hasattr(cls, "ir"):
                return cls.ir
            return cls.kr
        return cls.new

    def _get_output_number(self):
        return 0

    def _get_outputs(self):
        return [self.calculation_rate] * len(self)

    def _get_source(self):
        return self

    def _is_unexpanded_input_name(self, input_name):
        if self._unexpanded_input_names:
            if input_name in self._unexpanded_input_names:
                return True
        return False

    def _is_valid_input(self, input_value):
        if isinstance(input_value, OutputProxy):
            return True
        elif hasattr(input_value, "__float__"):
            return True
        return False

    @classmethod
    def _new_expanded(cls, **kwargs) -> Union[OutputProxy, UGenVector]:
        output_proxies = []
        dictionaries = UGen._expand_dictionary(
            kwargs,
            unexpanded_input_names=cls._unexpanded_input_names,
        )
        for input_dict in dictionaries:
            if isinstance(ugen := cls._new_single(**input_dict), OutputProxy):
                output_proxies.append(ugen)
            elif len(ugen):
                output_proxies.extend(ugen[:])
            else:
                output_proxies.append(ugen)
        if len(output_proxies) == 1:
            return output_proxies[0]
        return UGenVector(*output_proxies)

    @classmethod
    def _new_single(cls, **kwargs):
        return cls(**kwargs)

    def _optimize_graph(self, sort_bundles):
        if self._is_pure:
            self._perform_dead_code_elimination(sort_bundles)

    def _perform_dead_code_elimination(self, sort_bundles):
        sort_bundle = sort_bundles.get(self, None)
        if not sort_bundle or sort_bundle.descendants:
            return
        del sort_bundles[self]
        for antecedent in tuple(sort_bundle.antecedents):
            antecedent_bundle = sort_bundles.get(antecedent, None)
            if not antecedent_bundle:
                continue
            antecedent_bundle.descendants.remove(self)
            antecedent._optimize_graph(sort_bundles)

    def _postprocess_kwargs(
        self, *, calculation_rate: CalculationRate, **kwargs
    ) -> Tuple[CalculationRate, Dict[str, Any]]:
        return calculation_rate, kwargs

    def _validate_inputs(self):
        pass

    ### PRIVATE PROPERTIES ###

    @property
    def _has_done_action(self) -> bool:
        return "done_action" in self._ordered_input_names

    ### PUBLIC PROPERTIES ###

    @property
    def calculation_rate(self):
        """
        Gets calculation-rate of ugen.

        ::

            >>> ugen = supriya.ugens.SinOsc.ar(
            ...     frequency=supriya.ugens.WhiteNoise.kr(),
            ...     phase=0.5,
            ... )
            >>> ugen.calculation_rate
            CalculationRate.AUDIO

        Returns calculation-rate.
        """
        return self._calculation_rate

    @property
    def has_done_flag(self) -> bool:
        return self._has_done_flag

    @property
    def inputs(self):
        """
        Gets inputs of ugen.

        ::

            >>> ugen = supriya.ugens.SinOsc.ar(
            ...     frequency=supriya.ugens.WhiteNoise.kr(),
            ...     phase=0.5,
            ... ).source
            >>> for input_ in ugen.inputs:
            ...     input_
            ...
            <WhiteNoise.kr()[0]>
            0.5

        Returns tuple.
        """
        return tuple(self._inputs)

    @property
    def is_input_ugen(self) -> bool:
        return self._is_input

    @property
    def is_output_ugen(self) -> bool:
        return self._is_output

    @property
    def outputs(self) -> Tuple[OutputProxy, ...]:
        """
        Gets outputs of ugen.

        ::

            >>> ugen = supriya.ugens.SinOsc.ar(
            ...     frequency=supriya.ugens.WhiteNoise.kr(),
            ...     phase=0.5,
            ... ).source
            >>> ugen.outputs
            (CalculationRate.AUDIO,)

        Returns tuple.
        """
        return tuple(self._get_outputs())

    @property
    def signal_range(self):
        """
        Gets signal range of ugen.

        ::

            >>> ugen = supriya.ugens.SinOsc.ar()
            >>> ugen.signal_range
            SignalRange.BIPOLAR

        A bipolar signal range indicates that the ugen generates signals above and below
        zero.

        A unipolar signal range indicates that the ugen only generates signals of 0 or
        greater.

        Returns signal range.
        """
        return self._signal_range

    @property
    def special_index(self):
        """
        Gets special index of ugen.

        ::

            >>> ugen = supriya.ugens.SinOsc.ar(
            ...     frequency=supriya.ugens.WhiteNoise.kr(),
            ...     phase=0.5,
            ... ).source
            >>> ugen.special_index
            0

        The `special index` of most ugens will be 0. SuperColliders's synth definition
        file format uses the special index to store the operator id for binary and unary
        operator ugens, and the parameter index of controls.

        Returns integer.
        """
        return self._special_index


UGenOperand: TypeAlias = Union[
    SupportsFloat, UGenOperable, Sequence[Union[SupportsFloat, UGenOperable]]
]

UGenInitScalarParam: TypeAlias = Union[SupportsFloat, OutputProxy]

UGenInitVectorParam: TypeAlias = Union[Sequence[UGenInitScalarParam], UGenSerializable]

UGenRateScalarParam: TypeAlias = Union[SupportsFloat, UGenOperable, UGenSerializable]

UGenRateVectorParam: TypeAlias = Union[
    UGenRateScalarParam, Sequence[UGenRateScalarParam]
]


@ugen(is_pure=True)
class UnaryOpUGen(UGen):
    """
    A unary operator ugen, created by applying a unary operator to a ugen.

    ::

        >>> ugen = supriya.ugens.SinOsc.ar()
        >>> unary_op_ugen = abs(ugen)
        >>> unary_op_ugen
        <UnaryOpUGen.ar(ABSOLUTE_VALUE)[0]>

    ::

        >>> unary_op_ugen.source.operator
        UnaryOperator.ABSOLUTE_VALUE
    """

    source = param()

    def __repr__(self) -> str:
        return f"<{type(self).__name__}.{self.calculation_rate.token}({self.operator.name})>"

    @property
    def operator(self) -> UnaryOperator:
        """
        Gets operator of UnaryOpUgen.

        ::

            >>> source = supriya.ugens.SinOsc.ar()
            >>> unary_op_ugen = -source
            >>> unary_op_ugen.source.operator
            UnaryOperator.NEGATIVE

        Returns unary operator.
        """
        return UnaryOperator(self.special_index)


@ugen(is_pure=True)
class BinaryOpUGen(UGen):
    """
    A binary operator ugen, created by applying a binary operator to two ugens.

    ::

        >>> left_operand = supriya.ugens.SinOsc.ar()
        >>> right_operand = supriya.ugens.WhiteNoise.kr()
        >>> binary_op_ugen = left_operand * right_operand
        >>> binary_op_ugen
        <BinaryOpUGen.ar(MULTIPLICATION)[0]>

    ::

        >>> binary_op_ugen.source.operator
        BinaryOperator.MULTIPLICATION
    """

    left = param()
    right = param()

    def __init__(
        self,
        *,
        calculation_rate: CalculationRateLike,
        left: UGenInitScalarParam,
        right: UGenInitScalarParam,
        special_index: int,
    ) -> None:
        super().__init__(
            calculation_rate=calculation_rate,
            left=left,
            right=right,
            special_index=special_index,
        )

    def __repr__(self) -> str:
        return f"<{type(self).__name__}.{self.calculation_rate.token}({self.operator.name})>"

    @classmethod
    def _new_single(
        cls, calculation_rate=None, special_index=None, left=None, right=None, **kwargs
    ):
        a = left
        b = right
        if special_index == BinaryOperator.MULTIPLICATION:
            if a == 0:
                return 0
            if b == 0:
                return 0
            if a == 1:
                return b
            if a == -1:
                return -b
            if b == 1:
                return a
            if b == -1:
                return -a
        if special_index == BinaryOperator.ADDITION:
            if a == 0:
                return b
            if b == 0:
                return a
        if special_index == BinaryOperator.SUBTRACTION:
            if a == 0:
                return -b
            if b == 0:
                return a
        if special_index == BinaryOperator.FLOAT_DIVISION:
            if b == 1:
                return a
            if b == -1:
                return -a
        return cls(
            calculation_rate=calculation_rate,
            special_index=special_index,
            left=a,
            right=b,
        )

    @property
    def operator(self) -> BinaryOperator:
        """
        Gets operator of BinaryOpUgen.

        ::

            >>> left = supriya.ugens.SinOsc.ar()
            >>> right = supriya.ugens.WhiteNoise.kr()
            >>> binary_op_ugen = left / right
            >>> binary_op_ugen.source.operator
            BinaryOperator.FLOAT_DIVISION

        Returns binary operator.
        """
        return BinaryOperator(self.special_index)


class PseudoUGen:
    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError


@dataclasses.dataclass(unsafe_hash=True)
class Parameter(UGenOperable):
    lag: Optional[float] = None
    name: Optional[str] = None
    parameter_rate: ParameterRate = cast(ParameterRate, ParameterRate.CONTROL)
    value: Union[float, Tuple[float, ...]] = 0.0

    def __post_init__(self):
        try:
            self.value = float(self.value)
        except TypeError:
            self.value = tuple(float(_) for _ in self.value)
        self.parameter_rate = ParameterRate.from_expr(self.parameter_rate)
        self._uuid = None

    ### SPECIAL METHODS ###

    def __getitem__(self, i):
        return self._get_output_proxy(i)

    def __len__(self):
        if isinstance(self.value, float):
            return 1
        return len(self.value)

    ### PRIVATE METHODS ###

    def _get_source(self):
        return self

    def _get_output_number(self):
        return 0

    def _optimize_graph(self, sort_bundles):
        pass

    ### PUBLIC PROPERTIES ###

    @property
    def calculation_rate(self):
        if (name := self.parameter_rate.name) == "TRIGGER":
            return cast(CalculationRate, CalculationRate.CONTROL)
        return CalculationRate.from_expr(name)

    @property
    def has_done_flag(self):
        return False

    @property
    def inputs(self):
        return ()

    @property
    def signal_range(self):
        SignalRange.BIPOLAR


class Control(UGen):
    """
    A control-rate control ugen.

    Control ugens can be set and routed externally to interact with a running synth.
    Controls are created from the parameters of a synthesizer definition, and typically
    do not need to be created by hand.
    """

    ### INITIALIZER ###

    def __init__(self, parameters, calculation_rate=None, starting_control_index=0):
        coerced_parameters = []
        for parameter in parameters:
            if not isinstance(parameter, Parameter):
                parameter = Parameter(name=parameter, value=0)
            coerced_parameters.append(parameter)
        self._parameters = tuple(coerced_parameters)
        self._channel_count = len(self)
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            special_index=starting_control_index,
        )

    ### SPECIAL METHODS ###

    def __getitem__(self, i):
        """
        Gets output proxy at `i`, via index or control name.

        Returns output proxy.
        """
        if isinstance(i, int):
            if len(self) == 1:
                return OutputProxy(source=self, output_index=0)
            return OutputProxy(source=self, output_index=i)
        else:
            return self[self._get_control_index(i)]

    def __len__(self):
        """
        Gets number of ugen outputs.

        Equal to the number of control names.

        Returns integer.
        """
        return sum(len(_) for _ in self.parameters)

    ### PRIVATE METHODS ###

    def _get_control_index(self, control_name):
        for i, parameter in enumerate(self._parameters):
            if parameter.name == control_name:
                return i
        raise ValueError

    def _get_outputs(self):
        return [self.calculation_rate] * len(self)

    def _get_parameter_output_proxies(self):
        output_proxies = []
        for parameter in self.parameters:
            output_proxies.extend(parameter)
        return output_proxies

    ### PUBLIC PROPERTIES ###

    @property
    def controls(self):
        """
        Gets controls of control ugen.

        Returns ugen graph.
        """
        if len(self.parameters) == 1:
            result = self
        else:
            result = [OutputProxy(self, i) for i in range(len(self.parameters))]
        return result

    @property
    def parameters(self):
        """
        Gets control names associated with control.

        Returns tuple.
        """
        return self._parameters

    @property
    def starting_control_index(self):
        """
        Gets starting control index of control ugen.

        Equivalent to the control ugen's special index.

        Returns integer.
        """
        return self._special_index


class AudioControl(Control):
    """
    A trigger-rate control ugen.
    """

    def __init__(self, parameters, calculation_rate=None, starting_control_index=0):
        Control.__init__(
            self,
            parameters,
            calculation_rate=CalculationRate.AUDIO,
            starting_control_index=starting_control_index,
        )


class LagControl(Control):
    """
    A lagged control-rate control ugen.
    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([("lags", None)])

    _unexpanded_input_names = ("lags",)

    ### INITIALIZER ###

    def __init__(self, parameters, calculation_rate=None, starting_control_index=0):
        coerced_parameters = []
        for parameter in parameters:
            if not isinstance(parameter, Parameter):
                parameter = Parameter(name=parameter, value=0)
            coerced_parameters.append(parameter)
        self._parameters = tuple(coerced_parameters)
        lags = []
        for parameter in self._parameters:
            lag = parameter.lag or 0.0
            lags.extend([lag] * len(parameter))
        self._channel_count = len(self)
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            special_index=starting_control_index,
            lags=lags,
        )


class TrigControl(Control):
    """
    A trigger-rate control ugen.
    """

    ### CLASS VARIABLES ###

    ### INITIALIZER ##

    def __init__(self, parameters, calculation_rate=None, starting_control_index=0):
        Control.__init__(
            self,
            parameters,
            calculation_rate=CalculationRate.CONTROL,
            starting_control_index=starting_control_index,
        )


class SynthDef:
    """
    A synth definition.

    ::

        >>> from supriya import SynthDefBuilder, ugens
        >>> with SynthDefBuilder(frequency=440) as builder:
        ...     sin_osc = ugens.SinOsc.ar(frequency=builder["frequency"])
        ...     out = ugens.Out.ar(bus=0, source=sin_osc)
        ...
        >>> synthdef = builder.build()

    ::

        >>> supriya.graph(synthdef)  # doctest: +SKIP

    ::

        >>> from supriya import Server
        >>> server = Server().boot()

    ::

        >>> _ = server.add_synthdefs(synthdef)

    ::

        >>> _ = server.free_synthdefs(synthdef)

    ::

        >>> _ = server.quit()
    """

    ### INITIALIZER ###

    def __init__(
        self,
        ugens: Sequence[Union[Parameter, UGen, OutputProxy]],
        name: Optional[str] = None,
        optimize: bool = True,
    ) -> None:
        self._name = name
        ugens_: List[UGen] = list(
            ugen.source if isinstance(ugen, OutputProxy) else ugen
            for ugen in copy.deepcopy(ugens)
        )
        assert all(isinstance(_, UGen) for _ in ugens_)
        ugens_ = self._cleanup_pv_chains(ugens_)
        ugens_ = self._cleanup_local_bufs(ugens_)
        if optimize:
            ugens_ = self._optimize_ugen_graph(ugens_)
        ugens_ = self._sort_ugens_topologically(ugens_)
        self._ugens = tuple(ugens_)
        self._constants = self._collect_constants(self._ugens)
        self._control_ugens = self._collect_control_ugens(self._ugens)
        self._indexed_parameters = self._collect_indexed_parameters(self._control_ugens)
        self._compiled_ugen_graph = SynthDefCompiler.compile_ugen_graph(self)

    ### SPECIAL METHODS ###

    def __eq__(self, expr) -> bool:
        if not isinstance(expr, type(self)):
            return False
        if expr.name != self.name:
            return False
        if expr._compiled_ugen_graph != self._compiled_ugen_graph:
            return False
        return True

    def __graph__(self):
        r"""
        Graphs SynthDef.

        ::

            >>> from supriya.ugens import Out, SinOsc, SynthDefBuilder

        ::

            >>> with SynthDefBuilder(frequency=440) as builder:
            ...     sin_osc = SinOsc.ar(frequency=builder["frequency"])
            ...     out = Out.ar(bus=0, source=sin_osc)
            ...
            >>> synthdef = builder.build()
            >>> print(format(synthdef.__graph__(), "graphviz"))
            digraph synthdef_... {
                graph [bgcolor=transparent,
                    color=lightslategrey,
                    dpi=72,
                    fontname=Arial,
                    outputorder=edgesfirst,
                    overlap=prism,
                    penwidth=2,
                    rankdir=LR,
                    ranksep=1,
                    splines=spline,
                    style="dotted, rounded"];
                node [fontname=Arial,
                    fontsize=12,
                    penwidth=2,
                    shape=Mrecord,
                    style="filled, rounded"];
                edge [penwidth=2];
                ugen_0 [fillcolor=lightgoldenrod2,
                    label="<f_0> Control\n(control) | { { <f_1_0_0> frequency:\n440.0 } }"];
                ugen_1 [fillcolor=lightsteelblue2,
                    label="<f_0> SinOsc\n(audio) | { { <f_1_0_0> frequency | <f_1_0_1> phase:\n0.0 } | { <f_1_1_0> 0 } }"];
                ugen_2 [fillcolor=lightsteelblue2,
                    label="<f_0> Out\n(audio) | { { <f_1_0_0> bus:\n0.0 | <f_1_0_1> source } }"];
                ugen_0:f_1_0_0:e -> ugen_1:f_1_0_0:w [color=goldenrod];
                ugen_1:f_1_1_0:e -> ugen_2:f_1_0_1:w [color=steelblue];
            }

        Returns Graphviz graph.
        """
        return SynthDefGrapher.graph(self)

    def __hash__(self) -> int:
        hash_values = (type(self), self._name, self._compiled_ugen_graph)
        return hash(hash_values)

    def __repr__(self) -> str:
        return "<{}: {}>".format(type(self).__name__, self.actual_name)

    def __str__(self) -> str:
        """
        Gets string representation of synth definition.

        ::

            >>> from supriya.ugens import Out, SinOsc, SynthDefBuilder

        ::

            >>> with supriya.SynthDefBuilder() as builder:
            ...     sin_one = supriya.ugens.SinOsc.ar()
            ...     sin_two = supriya.ugens.SinOsc.ar(frequency=443)
            ...     source = sin_one + sin_two
            ...     out = supriya.ugens.Out.ar(bus=0, source=source)
            ...
            >>> synthdef = builder.build(name="test")

        ::

            >>> supriya.graph(synthdef)  # doctest: +SKIP

        ::

            >>> print(synthdef)
            synthdef:
                name: test
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(ADDITION).ar:
                        left: SinOsc.ar/0[0]
                        right: SinOsc.ar/1[0]
                -   Out.ar:
                        bus: 0.0
                        source[0]: BinaryOpUGen(ADDITION).ar[0]

        Returns string.
        """

        def get_ugen_names() -> Dict[UGen, str]:
            grouped_ugens: Dict[Tuple[Type[UGen], CalculationRate, int], List[UGen]] = (
                {}
            )
            named_ugens: Dict[UGen, str] = {}
            for ugen in self._ugens:
                key = (type(ugen), ugen.calculation_rate, ugen.special_index)
                grouped_ugens.setdefault(key, []).append(ugen)
            for ugen in self._ugens:
                parts = [type(ugen).__name__]
                if isinstance(ugen, BinaryOpUGen):
                    ugen_op = BinaryOperator.from_expr(ugen.special_index)
                    parts.append("(" + ugen_op.name + ")")
                elif isinstance(ugen, UnaryOpUGen):
                    ugen_op = UnaryOperator.from_expr(ugen.special_index)
                    parts.append("(" + ugen_op.name + ")")
                parts.append("." + ugen.calculation_rate.token)
                key = (type(ugen), ugen.calculation_rate, ugen.special_index)
                related_ugens = grouped_ugens[key]
                if len(related_ugens) > 1:
                    parts.append("/{}".format(related_ugens.index(ugen)))
                named_ugens[ugen] = "".join(parts)
            return named_ugens

        def get_parameter_name(
            input_: Union[Control, Parameter], output_index: int = 0
        ) -> str:
            if isinstance(input_, Parameter):
                return ":{}".format(input_.name)
            elif isinstance(input_, Control):
                # Handle array-like parameters
                value_index = 0
                for parameter in input_.parameters:
                    values = parameter.value
                    if isinstance(values, float):
                        values = [values]
                    for i in range(len(values)):
                        if value_index != output_index:
                            value_index += 1
                            continue
                        elif len(values) == 1:
                            return ":{}".format(parameter.name)
                        else:
                            return ":{}[{}]".format(parameter.name, i)
            return ""

        result = [
            "synthdef:",
            f"    name: {self.actual_name}",
            "    ugens:",
        ]
        ugen_dicts: List[Dict[str, Dict[str, Union[float, str]]]] = []
        named_ugens = get_ugen_names()
        for ugen in self._ugens:
            parameter_dict: Dict[str, Union[float, str]] = {}
            ugen_name = named_ugens[ugen]
            for input_name, input_ in zip(ugen._input_names, ugen._inputs):
                if isinstance(input_name, str):
                    argument_name = input_name
                else:
                    argument_name = f"{input_name[0]}[{input_name[1]}]"
                if isinstance(input_, SupportsFloat):
                    value: Union[float, str] = float(input_)
                else:
                    output_index = 0
                    if isinstance(input_, OutputProxy):
                        output_index = input_.output_index
                        input_ = input_.source
                    input_name = named_ugens[input_]
                    value = "{}[{}{}]".format(
                        input_name,
                        output_index,
                        get_parameter_name(input_, output_index),
                    )
                parameter_dict[argument_name] = value
            ugen_dicts.append({ugen_name: parameter_dict})
        for ugen_dict in ugen_dicts:
            for ugen_name, parameter_dict in ugen_dict.items():
                if not parameter_dict:
                    result.append(f"    -   {ugen_name}: null")
                    continue
                result.append(f"    -   {ugen_name}:")
                for parameter_name, parameter_value in parameter_dict.items():
                    result.append(f"            {parameter_name}: {parameter_value}")
        return "\n".join(result)

    ### PRIVATE METHODS ###

    @staticmethod
    def _build_control_mapping(parameters):
        control_mapping = {}
        scalar_parameters = []
        trigger_parameters = []
        audio_parameters = []
        control_parameters = []
        mapping = {
            ParameterRate.AUDIO: audio_parameters,
            ParameterRate.CONTROL: control_parameters,
            ParameterRate.SCALAR: scalar_parameters,
            ParameterRate.TRIGGER: trigger_parameters,
        }
        for parameter in parameters:
            mapping[parameter.parameter_rate].append(parameter)
        for filtered_parameters in mapping.values():
            filtered_parameters.sort(key=lambda x: x.name)
        control_ugens = []
        starting_control_index = 0
        if scalar_parameters:
            control = Control(
                parameters=scalar_parameters,
                calculation_rate=CalculationRate.SCALAR,
                starting_control_index=starting_control_index,
            )
            control_ugens.append(control)
            for parameter in scalar_parameters:
                starting_control_index += len(parameter)
            for i, output_proxy in enumerate(control._get_parameter_output_proxies()):
                control_mapping[output_proxy] = control[i]
        if trigger_parameters:
            control = TrigControl(
                parameters=trigger_parameters,
                starting_control_index=starting_control_index,
            )
            control_ugens.append(control)
            for parameter in trigger_parameters:
                starting_control_index += len(parameter)
            for i, output_proxy in enumerate(control._get_parameter_output_proxies()):
                control_mapping[output_proxy] = control[i]
        if audio_parameters:
            control = AudioControl(
                parameters=audio_parameters,
                starting_control_index=starting_control_index,
            )
            control_ugens.append(control)
            for parameter in audio_parameters:
                starting_control_index += len(parameter)
            for i, output_proxy in enumerate(control._get_parameter_output_proxies()):
                control_mapping[output_proxy] = control[i]
        if control_parameters:
            if any(_.lag for _ in control_parameters):
                control = LagControl(
                    parameters=control_parameters,
                    calculation_rate=CalculationRate.CONTROL,
                    starting_control_index=starting_control_index,
                )
            else:
                control = Control(
                    parameters=control_parameters,
                    calculation_rate=CalculationRate.CONTROL,
                    starting_control_index=starting_control_index,
                )
            control_ugens.append(control)
            for parameter in control_parameters:
                starting_control_index += len(parameter)
            for i, output_proxy in enumerate(control._get_parameter_output_proxies()):
                control_mapping[output_proxy] = control[i]
        control_ugens = tuple(control_ugens)
        return control_ugens, control_mapping

    @staticmethod
    def _build_input_mapping(ugens):
        from . import PV_ChainUGen, PV_Copy

        input_mapping = {}
        for ugen in ugens:
            if not isinstance(ugen, PV_ChainUGen):
                continue
            if isinstance(ugen, PV_Copy):
                continue
            for i, input_ in enumerate(ugen.inputs):
                if not isinstance(input_, OutputProxy):
                    continue
                source = input_.source
                if not isinstance(source, PV_ChainUGen):
                    continue
                if source not in input_mapping:
                    input_mapping[source] = []
                input_mapping[source].append((ugen, i))
        return input_mapping

    @staticmethod
    def _cleanup_local_bufs(ugens):
        from . import LocalBuf, MaxLocalBufs

        local_bufs = []
        processed_ugens = []
        for ugen in ugens:
            if isinstance(ugen, OutputProxy):
                ugen = ugen.source
            if isinstance(ugen, MaxLocalBufs):
                continue
            if isinstance(ugen, LocalBuf):
                local_bufs.append(ugen)
            processed_ugens.append(ugen)
        if local_bufs:
            max_local_bufs = MaxLocalBufs.ir(maximum=len(local_bufs))
            for local_buf in local_bufs:
                inputs = list(local_buf.inputs[:2])
                inputs.append(max_local_bufs)
                local_buf._inputs = tuple(inputs)
            index = processed_ugens.index(local_bufs[0])
            processed_ugens[index:index] = [max_local_bufs.source]
        return tuple(processed_ugens)

    @staticmethod
    def _cleanup_pv_chains(ugens):
        from . import LocalBuf, PV_Copy

        input_mapping = SynthDef._build_input_mapping(ugens)
        for antecedent, descendants in input_mapping.items():
            if len(descendants) == 1:
                continue
            for descendant, input_index in descendants[:-1]:
                fft_size = antecedent.fft_size
                new_buffer = LocalBuf.ir(frame_count=fft_size)
                pv_copy = PV_Copy.kr(pv_chain_a=antecedent, pv_chain_b=new_buffer)
                inputs = list(descendant._inputs)
                inputs[input_index] = pv_copy
                descendant._inputs = tuple(inputs)
                index = ugens.index(descendant)
                replacement = []
                if isinstance(fft_size, UGenOperable):
                    replacement.append(fft_size)
                replacement.extend([new_buffer.source, pv_copy.source])
                ugens[index:index] = replacement
        return ugens

    @staticmethod
    def _collect_constants(ugens) -> Tuple[float, ...]:
        constants = []
        for ugen in ugens:
            for input_ in ugen._inputs:
                if not isinstance(input_, float):
                    continue
                if input_ not in constants:
                    constants.append(input_)
        return tuple(constants)

    @staticmethod
    def _collect_control_ugens(ugens):
        control_ugens = tuple(_ for _ in ugens if isinstance(_, Control))
        return control_ugens

    @staticmethod
    def _collect_indexed_parameters(control_ugens) -> Sequence[Tuple[int, Parameter]]:
        indexed_parameters = []
        parameters = {}
        for control_ugen in control_ugens:
            index = control_ugen.starting_control_index
            for parameter in control_ugen.parameters:
                parameters[parameter.name] = (index, parameter)
                index += len(parameter)
        for parameter_name in sorted(parameters):
            indexed_parameters.append(parameters[parameter_name])
        return tuple(indexed_parameters)

    @staticmethod
    def _extract_parameters(ugens):
        parameters = set()
        for ugen in ugens:
            if isinstance(ugen, Parameter):
                parameters.add(ugen)
        ugens = tuple(ugen for ugen in ugens if ugen not in parameters)
        parameters = tuple(sorted(parameters, key=lambda x: x.name))
        return ugens, parameters

    @staticmethod
    def _initialize_topological_sort(ugens):
        ugens = list(ugens)
        sort_bundles = collections.OrderedDict()
        width_first_antecedents = []
        # The UGens are in the order they were added to the SynthDef
        # and that order already mostly places inputs before outputs.
        # In sclang, the per-UGen width-first antecedents list is
        # updated at the moment the UGen is added to the SynthDef.
        # Because we don't store that state on UGens in supriya, we'll
        # do it here.
        for ugen in ugens:
            sort_bundles[ugen] = UGenSortBundle(ugen, width_first_antecedents)
            if ugen._is_width_first:
                width_first_antecedents.append(ugen)
        for ugen in ugens:
            sort_bundle = sort_bundles[ugen]
            sort_bundle._initialize_topological_sort(sort_bundles)
            sort_bundle.descendants[:] = sorted(
                sort_bundles[ugen].descendants, key=lambda x: ugens.index(ugen)
            )
        return sort_bundles

    @staticmethod
    def _optimize_ugen_graph(ugens):
        sort_bundles = SynthDef._initialize_topological_sort(ugens)
        for ugen in ugens:
            ugen._optimize_graph(sort_bundles)
        return tuple(sort_bundles)

    @staticmethod
    def _remap_controls(ugens, control_mapping):
        for ugen in ugens:
            inputs = list(ugen.inputs)
            for i, input_ in enumerate(inputs):
                if input_ in control_mapping:
                    output_proxy = control_mapping[input_]
                    inputs[i] = output_proxy
            ugen._inputs = tuple(inputs)

    @staticmethod
    def _sort_ugens_topologically(ugens):
        sort_bundles = SynthDef._initialize_topological_sort(ugens)
        available_ugens = []
        for ugen in reversed(ugens):
            sort_bundles[ugen]._make_available(available_ugens)
        out_stack = []
        while available_ugens:
            available_ugen = available_ugens.pop()
            sort_bundles[available_ugen]._schedule(
                available_ugens, out_stack, sort_bundles
            )
        return out_stack

    ### PUBLIC METHODS ###

    def compile(self, use_anonymous_name=False) -> bytes:
        synthdefs = [self]
        result = compile_synthdefs(synthdefs, use_anonymous_names=use_anonymous_name)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def actual_name(self) -> str:
        return self.name or self.anonymous_name

    @property
    def anonymous_name(self) -> str:
        md5 = hashlib.md5()
        md5.update(self._compiled_ugen_graph)
        anonymous_name = md5.hexdigest()
        return anonymous_name

    @property
    def audio_channel_count(self) -> int:
        return max(self.audio_input_channel_count, self.audio_output_channel_count)

    @property
    def audio_input_channel_count(self) -> int:
        """
        Gets audio input channel count of synthdef.

        ::

            >>> with supriya.SynthDefBuilder() as builder:
            ...     audio_in = supriya.ugens.In.ar(channel_count=1)
            ...     control_in = supriya.ugens.In.kr(channel_count=2)
            ...     sin = supriya.ugens.SinOsc.ar(
            ...         frequency=audio_in,
            ...     )
            ...     source = audio_in * control_in[1]
            ...     audio_out = supriya.ugens.Out.ar(source=[source] * 4)
            ...
            >>> synthdef = builder.build()

        ::

            >>> supriya.graph(synthdef)  # doctest: +SKIP

        ::

            >>> synthdef.audio_input_channel_count
            1

        Returns integer.
        """
        ugens = tuple(
            _ for _ in self.input_ugens if _.calculation_rate == CalculationRate.AUDIO
        )
        if len(ugens) == 1:
            return len(ugens[0])
        elif not ugens:
            return 0
        raise ValueError

    @property
    def audio_output_channel_count(self) -> int:
        """
        Gets audio output channel count of synthdef.

        ::

            >>> with supriya.SynthDefBuilder() as builder:
            ...     audio_in = supriya.ugens.In.ar(channel_count=1)
            ...     control_in = supriya.ugens.In.kr(channel_count=2)
            ...     sin = supriya.ugens.SinOsc.ar(
            ...         frequency=audio_in,
            ...     )
            ...     source = sin * control_in[0]
            ...     audio_out = supriya.ugens.Out.ar(source=[source] * 4)
            ...
            >>> synthdef = builder.build()
            >>> print(synthdef)
            synthdef:
                name: ...
                ugens:
                -   In.ar:
                        bus: 0.0
                -   SinOsc.ar:
                        frequency: In.ar[0]
                        phase: 0.0
                -   In.kr:
                        bus: 0.0
                -   BinaryOpUGen(MULTIPLICATION).ar:
                        left: SinOsc.ar[0]
                        right: In.kr[0]
                -   Out.ar:
                        bus: 0.0
                        source[0]: BinaryOpUGen(MULTIPLICATION).ar[0]
                        source[1]: BinaryOpUGen(MULTIPLICATION).ar[0]
                        source[2]: BinaryOpUGen(MULTIPLICATION).ar[0]
                        source[3]: BinaryOpUGen(MULTIPLICATION).ar[0]

        ::

            >>> supriya.graph(synthdef)  # doctest: +SKIP

        ::

            >>> synthdef.audio_output_channel_count
            4

        Returns integer.
        """
        ugens = tuple(
            _ for _ in self.output_ugens if _.calculation_rate == CalculationRate.AUDIO
        )
        if len(ugens) == 1:
            return len(ugens[0].source)
        elif not ugens:
            return 0
        raise ValueError

    @property
    def constants(self) -> Tuple[float, ...]:
        return self._constants

    @property
    def control_ugens(self) -> List[UGen]:
        return self._control_ugens

    @property
    def control_channel_count(self) -> int:
        return max(self.control_input_channel_count, self.control_output_channel_count)

    @property
    def control_input_channel_count(self) -> int:
        """
        Gets control input channel count of synthdef.

        ::

            >>> with supriya.SynthDefBuilder() as builder:
            ...     audio_in = supriya.ugens.In.ar(channel_count=1)
            ...     control_in = supriya.ugens.In.kr(channel_count=2)
            ...     sin = supriya.ugens.SinOsc.ar(
            ...         frequency=audio_in,
            ...     )
            ...     source = audio_in * control_in[1]
            ...     audio_out = supriya.ugens.Out.ar(source=[source] * 4)
            ...
            >>> synthdef = builder.build()

        ::

            >>> supriya.graph(synthdef)  # doctest: +SKIP

        ::

            >>> synthdef.control_input_channel_count
            2

        Returns integer.
        """
        ugens = tuple(
            _ for _ in self.input_ugens if _.calculation_rate == CalculationRate.CONTROL
        )
        if len(ugens) == 1:
            return len(ugens[0])
        elif not ugens:
            return 0
        raise ValueError

    @property
    def control_output_channel_count(self) -> int:
        """
        Gets control output channel count of synthdef.

        ::

            >>> with supriya.SynthDefBuilder() as builder:
            ...     audio_in = supriya.ugens.In.ar(channel_count=1)
            ...     control_in = supriya.ugens.In.kr(channel_count=2)
            ...     sin = supriya.ugens.SinOsc.ar(
            ...         frequency=audio_in,
            ...     )
            ...     source = audio_in * control_in[1]
            ...     audio_out = supriya.ugens.Out.ar(source=[source] * 4)
            ...
            >>> synthdef = builder.build()

        ::

            >>> supriya.graph(synthdef)  # doctest: +SKIP

        ::

            >>> synthdef.control_output_channel_count
            0

        Returns integer.
        """
        ugens = tuple(
            _
            for _ in self.output_ugens
            if _.calculation_rate == CalculationRate.CONTROL
        )
        if len(ugens) == 1:
            return len(ugens[0].source)
        elif not ugens:
            return 0
        raise ValueError

    @property
    def done_actions(self) -> List[DoneAction]:
        done_actions = set()
        for ugen in self.ugens:
            done_action = ugen._get_done_action()
            if done_action is not None:
                done_actions.add(done_action)
        return sorted(done_actions)

    @property
    def has_gate(self) -> bool:
        return "gate" in self.parameter_names

    @property
    def indexed_parameters(self) -> Sequence[Tuple[int, Parameter]]:
        return self._indexed_parameters

    @property
    def input_ugens(self) -> Tuple[UGen, ...]:
        return tuple(_ for _ in self.ugens if _.is_input_ugen)

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def output_ugens(self) -> Tuple[UGen, ...]:
        return tuple(_ for _ in self.ugens if _.is_output_ugen)

    @property
    def parameters(self) -> Dict[Optional[str], Parameter]:
        return {
            parameter.name: parameter for index, parameter in self.indexed_parameters
        }

    @property
    def parameter_names(self) -> List[Optional[str]]:
        return [parameter.name for index, parameter in self.indexed_parameters]

    @property
    def ugens(self) -> Tuple[UGen, ...]:
        return self._ugens


class UGenSortBundle:
    ### INITIALIZER ###

    def __init__(self, ugen, width_first_antecedents):
        self.antecedents = []
        self.descendants = []
        self.ugen = ugen
        self.width_first_antecedents = tuple(width_first_antecedents)

    ### PRIVATE METHODS ###

    def _initialize_topological_sort(self, sort_bundles):
        for input_ in self.ugen.inputs:
            if isinstance(input_, OutputProxy):
                input_ = input_.source
            elif not isinstance(input_, UGen):
                continue
            input_sort_bundle = sort_bundles[input_]
            if input_ not in self.antecedents:
                self.antecedents.append(input_)
            if self.ugen not in input_sort_bundle.descendants:
                input_sort_bundle.descendants.append(self.ugen)
        for input_ in self.width_first_antecedents:
            input_sort_bundle = sort_bundles[input_]
            if input_ not in self.antecedents:
                self.antecedents.append(input_)
            if self.ugen not in input_sort_bundle.descendants:
                input_sort_bundle.descendants.append(self.ugen)

    def _make_available(self, available_ugens):
        if not self.antecedents:
            if self.ugen not in available_ugens:
                available_ugens.append(self.ugen)

    def _schedule(self, available_ugens, out_stack, sort_bundles):
        for ugen in reversed(self.descendants):
            sort_bundle = sort_bundles[ugen]
            sort_bundle.antecedents.remove(self.ugen)
            sort_bundle._make_available(available_ugens)
        out_stack.append(self.ugen)

    ### PUBLIC METHODS ###

    def clear(self) -> None:
        self.antecedents[:] = []
        self.descendants[:] = []
        self.width_first_antecedents[:] = []


class SuperColliderSynthDef:
    ### INITIALIZER ###

    def __init__(self, name, body, rates=None):
        self._name = name
        self._body = body
        self._rates = rates

    ### PRIVATE METHODS ###

    def _build_sc_input(self, directory_path):
        input_ = []
        input_.append("a = SynthDef(")
        input_.append("    \\{}, {{".format(self.name))
        for line in self.body.splitlines():
            input_.append("    " + line)
        if self.rates:
            input_.append("}}, {});".format(self.rates))
        else:
            input_.append("});")
        input_.append('"Defined SynthDef".postln;')
        input_.append('a.writeDefFile("{}");'.format(directory_path))
        input_.append('"Wrote SynthDef".postln;')
        input_.append("0.exit;")
        input_ = "\n".join(input_)
        return input_

    ### PUBLIC METHODS ###

    def compile(self):
        sclang_path = sclang.find()
        with tempfile.TemporaryDirectory() as directory:
            directory_path = pathlib.Path(directory)
            sc_input = self._build_sc_input(directory_path)
            sc_file_path = directory_path / f"{self.name}.sc"
            sc_file_path.write_text(sc_input)
            command = [str(sclang_path), "-D", str(sc_file_path)]
            subprocess.run(command, timeout=10)
            result = (directory_path / f"{self.name}.scsyndef").read_bytes()
        return bytes(result)

    ### PUBLIC PROPERTIES ###

    @property
    def body(self):
        return self._body

    @property
    def rates(self):
        return self._rates

    @property
    def name(self):
        return self._name


_local = threading.local()
_local._active_builders = []


class SynthDefBuilder:
    """
    A SynthDef builder.

    ::

        >>> from supriya import ParameterRate
        >>> from supriya.ugens import Decay, Out, Parameter, SinOsc, SynthDefBuilder

    ::

        >>> builder = SynthDefBuilder(
        ...     frequency=440,
        ...     trigger=Parameter(
        ...         value=0,
        ...         parameter_rate=ParameterRate.TRIGGER,
        ...     ),
        ... )

    ::

        >>> with builder:
        ...     sin_osc = SinOsc.ar(
        ...         frequency=builder["frequency"],
        ...     )
        ...     decay = Decay.kr(
        ...         decay_time=0.5,
        ...         source=builder["trigger"],
        ...     )
        ...     enveloped_sin = sin_osc * decay
        ...     out = Out.ar(bus=0, source=enveloped_sin)
        ...

    ::

        >>> synthdef = builder.build()
        >>> supriya.graph(synthdef)  # doctest: +SKIP
    """

    ### CLASS VARIABLES ###

    _active_builders: List["SynthDefBuilder"] = _local._active_builders

    __slots__ = ("_name", "_parameters", "_ugens", "_uuid")

    ### INITIALIZER ###

    def __init__(self, name: Optional[str] = None, **kwargs) -> None:
        self._name = name
        self._uuid = uuid.uuid4()
        self._parameters: Dict[Optional[str], Parameter] = collections.OrderedDict()
        self._ugens: List[Union[Parameter, UGen]] = []
        for key, value in kwargs.items():
            self._add_parameter(key, value)

    ### SPECIAL METHODS ###

    def __enter__(self) -> "SynthDefBuilder":
        SynthDefBuilder._active_builders.append(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        SynthDefBuilder._active_builders.pop()

    def __getitem__(self, item: str) -> Parameter:
        return self._parameters[item]

    ### PRIVATE METHODS ###

    def _add_ugens(self, ugen: Union[OutputProxy, Parameter, UGen]):
        if isinstance(ugen, OutputProxy):
            source = ugen.source
        else:
            source = ugen
        if source._uuid != self._uuid:
            raise ValueError
        self._ugens.append(source)

    def _add_parameter(self, *args) -> Parameter:
        # TODO: Refactor without *args for clarity
        if 3 < len(args):
            raise ValueError(args)
        if len(args) == 1:
            assert isinstance(args[0], Parameter)
            name, value, parameter_rate = args[0].name, args[0], args[0].parameter_rate
        elif len(args) == 2:
            name, value = args
            if isinstance(value, Parameter):
                parameter_rate = value.parameter_rate
            else:
                parameter_rate = ParameterRate.CONTROL
                if name.startswith("a_"):
                    parameter_rate = ParameterRate.AUDIO
                elif name.startswith("i_"):
                    parameter_rate = ParameterRate.SCALAR
                elif name.startswith("t_"):
                    parameter_rate = ParameterRate.TRIGGER
        elif len(args) == 3:
            name, value, parameter_rate = args
            parameter_rate = ParameterRate.from_expr(parameter_rate)
        else:
            raise ValueError(args)
        if not isinstance(value, Parameter):
            parameter = Parameter(name=name, parameter_rate=parameter_rate, value=value)
        else:
            parameter = new(value, parameter_rate=parameter_rate, name=name)
        assert parameter._uuid is None
        parameter._uuid = self._uuid
        self._parameters[name] = parameter
        return parameter

    ### PUBLIC METHODS ###

    def build(self, name: Optional[str] = None, optimize: bool = True) -> SynthDef:
        # Calling build() creates controls each time, so strip out
        # previously created ones. This could be made cleaner by preventing
        # Control subclasses from being aggregated into SynthDefBuilders in
        # the first place.
        self._ugens[:] = [ugen for ugen in self._ugens if not isinstance(ugen, Control)]
        name = self.name or name
        with self:
            ugens: List[Union[Parameter, UGen]] = []
            ugens.extend(self._parameters.values())
            ugens.extend(self._ugens)
            ugens = copy.deepcopy(ugens)
            ugens, parameters = SynthDef._extract_parameters(ugens)
            (
                control_ugens,
                control_mapping,
            ) = SynthDef._build_control_mapping(parameters)
            SynthDef._remap_controls(ugens, control_mapping)
            ugens = control_ugens + ugens
            synthdef = SynthDef(ugens, name=name, optimize=optimize)
        return synthdef

    def poll_ugen(
        self,
        ugen: UGen,
        label: Optional[str] = None,
        trigger: Optional[UGen] = None,
        trigger_id: int = -1,
    ) -> None:
        from . import Impulse, Poll

        poll = Poll.new(
            source=ugen,
            label=label,
            trigger=trigger or Impulse.kr(frequency=1),
            trigger_id=trigger_id,
        )
        self._add_ugens(poll)

    ### PUBLIC PROPERTIES ###

    @property
    def name(self) -> Optional[str]:
        return self._name


def synthdef(*args: Union[str, Tuple[str, float]]) -> Callable[[Callable], SynthDef]:
    """
    Decorator for quickly constructing SynthDefs from functions.

    ::

        >>> from supriya import Envelope, synthdef
        >>> from supriya.ugens import EnvGen, Out, SinOsc

    ::

        >>> @synthdef()
        ... def sine(freq=440, amp=0.1, gate=1):
        ...     sig = SinOsc.ar(frequency=freq) * amp
        ...     env = EnvGen.kr(envelope=Envelope.adsr(), gate=gate, done_action=2)
        ...     Out.ar(bus=0, source=[sig * env] * 2)
        ...

    ::

        >>> print(sine)
        synthdef:
            name: sine
            ugens:
            -   Control.kr: null
            -   SinOsc.ar:
                    frequency: Control.kr[1:freq]
                    phase: 0.0
            -   BinaryOpUGen(MULTIPLICATION).ar/0:
                    left: SinOsc.ar[0]
                    right: Control.kr[0:amp]
            -   EnvGen.kr:
                    gate: Control.kr[2:gate]
                    level_scale: 1.0
                    level_bias: 0.0
                    time_scale: 1.0
                    done_action: 2.0
                    envelope[0]: 0.0
                    envelope[1]: 3.0
                    envelope[2]: 2.0
                    envelope[3]: -99.0
                    envelope[4]: 1.0
                    envelope[5]: 0.01
                    envelope[6]: 5.0
                    envelope[7]: -4.0
                    envelope[8]: 0.5
                    envelope[9]: 0.3
                    envelope[10]: 5.0
                    envelope[11]: -4.0
                    envelope[12]: 0.0
                    envelope[13]: 1.0
                    envelope[14]: 5.0
                    envelope[15]: -4.0
            -   BinaryOpUGen(MULTIPLICATION).ar/1:
                    left: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                    right: EnvGen.kr[0]
            -   Out.ar:
                    bus: 0.0
                    source[0]: BinaryOpUGen(MULTIPLICATION).ar/1[0]
                    source[1]: BinaryOpUGen(MULTIPLICATION).ar/1[0]

    ::

        >>> @synthdef("ar", ("kr", 0.5))
        ... def sine(freq=440, amp=0.1, gate=1):
        ...     sig = SinOsc.ar(frequency=freq) * amp
        ...     env = EnvGen.kr(envelope=Envelope.adsr(), gate=gate, done_action=2)
        ...     Out.ar(bus=0, source=[sig * env] * 2)
        ...

    ::

        >>> print(sine)
        synthdef:
            name: sine
            ugens:
            -   AudioControl.ar: null
            -   SinOsc.ar:
                    frequency: AudioControl.ar[0:freq]
                    phase: 0.0
            -   LagControl.kr:
                    lags[0]: 0.5
                    lags[1]: 0.0
            -   BinaryOpUGen(MULTIPLICATION).ar/0:
                    left: SinOsc.ar[0]
                    right: LagControl.kr[0:amp]
            -   EnvGen.kr:
                    gate: LagControl.kr[1:gate]
                    level_scale: 1.0
                    level_bias: 0.0
                    time_scale: 1.0
                    done_action: 2.0
                    envelope[0]: 0.0
                    envelope[1]: 3.0
                    envelope[2]: 2.0
                    envelope[3]: -99.0
                    envelope[4]: 1.0
                    envelope[5]: 0.01
                    envelope[6]: 5.0
                    envelope[7]: -4.0
                    envelope[8]: 0.5
                    envelope[9]: 0.3
                    envelope[10]: 5.0
                    envelope[11]: -4.0
                    envelope[12]: 0.0
                    envelope[13]: 1.0
                    envelope[14]: 5.0
                    envelope[15]: -4.0
            -   BinaryOpUGen(MULTIPLICATION).ar/1:
                    left: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                    right: EnvGen.kr[0]
            -   Out.ar:
                    bus: 0.0
                    source[0]: BinaryOpUGen(MULTIPLICATION).ar/1[0]
                    source[1]: BinaryOpUGen(MULTIPLICATION).ar/1[0]
    """

    def inner(func):
        signature = inspect.signature(func)
        builder = SynthDefBuilder()
        kwargs = {}
        for i, (name, parameter) in enumerate(signature.parameters.items()):
            rate = ParameterRate.CONTROL
            lag = None
            try:
                if isinstance(args[i], str):
                    rate_expr = args[i]
                else:
                    rate_expr, lag = args[i]
                rate = ParameterRate.from_expr(rate_expr)
            except (IndexError, TypeError):
                pass
            value = parameter.default
            if value is inspect._empty:
                value = 0.0
            parameter = Parameter(lag=lag, name=name, parameter_rate=rate, value=value)
            kwargs[name] = builder._add_parameter(parameter)
        with builder:
            func(**kwargs)
        return builder.build(name=func.__name__)

    return inner


class SynthDefGrapher:
    r"""
    Graphs SynthDefs.

    .. container:: example

        ::

            >>> ugen_graph = supriya.ugens.LFNoise2.ar()
            >>> result = ugen_graph.transpose([0, 3, 7])

        ::

            >>> supriya.graph(result)  # doctest: +SKIP

        ::

            >>> print(format(result.__graph__(), "graphviz"))
            digraph synthdef_c481c3d42e3cfcee0267250247dab51f {
                graph [bgcolor=transparent,
                    color=lightslategrey,
                    dpi=72,
                    fontname=Arial,
                    outputorder=edgesfirst,
                    overlap=prism,
                    penwidth=2,
                    rankdir=LR,
                    ranksep=1,
                    splines=spline,
                    style="dotted, rounded"];
                node [fontname=Arial,
                    fontsize=12,
                    penwidth=2,
                    shape=Mrecord,
                    style="filled, rounded"];
                edge [penwidth=2];
                ugen_0 [fillcolor=lightsteelblue2,
                    label="<f_0> LFNoise2\n(audio) | { { <f_1_0_0> frequency:\n500.0 } | { <f_1_1_0> 0 } }"];
                ugen_1 [fillcolor=lightsteelblue2,
                    label="<f_0> UnaryOpUGen\n[HZ_TO_MIDI]\n(audio) | { { <f_1_0_0> source } | { <f_1_1_0> 0 } }"];
                ugen_2 [fillcolor=lightsteelblue2,
                    label="<f_0> UnaryOpUGen\n[MIDI_TO_HZ]\n(audio) | { { <f_1_0_0> source } | { <f_1_1_0> 0 } }"];
                ugen_3 [fillcolor=lightsteelblue2,
                    label="<f_0> BinaryOpUGen\n[ADDITION]\n(audio) | { { <f_1_0_0> left | <f_1_0_1> right:\n3.0 } | { <f_1_1_0> 0 } }"];
                ugen_4 [fillcolor=lightsteelblue2,
                    label="<f_0> UnaryOpUGen\n[MIDI_TO_HZ]\n(audio) | { { <f_1_0_0> source } | { <f_1_1_0> 0 } }"];
                ugen_5 [fillcolor=lightsteelblue2,
                    label="<f_0> BinaryOpUGen\n[ADDITION]\n(audio) | { { <f_1_0_0> left | <f_1_0_1> right:\n7.0 } | { <f_1_1_0> 0 } }"];
                ugen_6 [fillcolor=lightsteelblue2,
                    label="<f_0> UnaryOpUGen\n[MIDI_TO_HZ]\n(audio) | { { <f_1_0_0> source } | { <f_1_1_0> 0 } }"];
                ugen_0:f_1_1_0:e -> ugen_1:f_1_0_0:w [color=steelblue];
                ugen_1:f_1_1_0:e -> ugen_2:f_1_0_0:w [color=steelblue];
                ugen_1:f_1_1_0:e -> ugen_3:f_1_0_0:w [color=steelblue];
                ugen_1:f_1_1_0:e -> ugen_5:f_1_0_0:w [color=steelblue];
                ugen_3:f_1_1_0:e -> ugen_4:f_1_0_0:w [color=steelblue];
                ugen_5:f_1_1_0:e -> ugen_6:f_1_0_0:w [color=steelblue];
            }
    """

    ### PRIVATE METHODS ###

    @staticmethod
    def _connect_nodes(synthdef, ugen_node_mapping):
        for ugen in synthdef.ugens:
            tail_node = ugen_node_mapping[ugen]
            for i, input_ in enumerate(ugen.inputs):
                if not isinstance(input_, OutputProxy):
                    continue
                tail_field = tail_node["inputs"][i]
                source = input_.source
                head_node = ugen_node_mapping[source]
                head_field = head_node["outputs"][input_.output_index]
                edge = uqbar.graphs.Edge(head_port_position="w", tail_port_position="e")
                edge.attach(head_field, tail_field)
                if source.calculation_rate == CalculationRate.CONTROL:
                    edge.attributes["color"] = "goldenrod"
                elif source.calculation_rate == CalculationRate.AUDIO:
                    edge.attributes["color"] = "steelblue"
                else:
                    edge.attributes["color"] = "salmon"

    @staticmethod
    def _create_ugen_input_group(ugen, ugen_index):
        if not ugen.inputs:
            return None
        input_group = uqbar.graphs.RecordGroup(name="inputs")
        for i, input_ in enumerate(ugen.inputs):
            label = ""
            input_name = None
            if i < len(ugen._ordered_input_names):
                input_name = tuple(ugen._ordered_input_names)[i]
            if input_name:
                # input_name = r'\n'.join(input_name.split('_'))
                if isinstance(input_, float):
                    label = r"{}:\n{}".format(input_name, input_)
                else:
                    label = input_name
            elif isinstance(input_, float):
                label = str(input_)
            label = label or None
            field = uqbar.graphs.RecordField(
                label=label, name="ugen_{}_input_{}".format(ugen_index, i)
            )
            input_group.append(field)
        return input_group

    @staticmethod
    def _create_ugen_node_mapping(synthdef):
        ugen_node_mapping = {}
        for ugen in synthdef.ugens:
            ugen_index = synthdef.ugens.index(ugen)
            node = uqbar.graphs.Node(name="ugen_{}".format(ugen_index))
            if ugen.calculation_rate == CalculationRate.CONTROL:
                node.attributes["fillcolor"] = "lightgoldenrod2"
            elif ugen.calculation_rate == CalculationRate.AUDIO:
                node.attributes["fillcolor"] = "lightsteelblue2"
            else:
                node.attributes["fillcolor"] = "lightsalmon2"
            title_field = SynthDefGrapher._create_ugen_title_field(ugen)
            node.append(title_field)
            group = uqbar.graphs.RecordGroup()
            input_group = SynthDefGrapher._create_ugen_input_group(ugen, ugen_index)
            if input_group is not None:
                group.append(input_group)
            output_group = SynthDefGrapher._create_ugen_output_group(
                synthdef, ugen, ugen_index
            )
            if output_group is not None:
                group.append(output_group)
            node.append(group)
            ugen_node_mapping[ugen] = node
        return ugen_node_mapping

    @staticmethod
    def _create_ugen_output_group(synthdef, ugen, ugen_index):
        if not ugen.outputs:
            return None
        output_group = uqbar.graphs.RecordGroup(name="outputs")
        for i, output in enumerate(ugen.outputs):
            label = str(i)
            if isinstance(ugen, Control):
                parameter_index = ugen.special_index + i
                parameter = dict(synthdef.indexed_parameters)[parameter_index]
                parameter_name = parameter.name
                # parameter_name = r'\n'.join(parameter.name.split('_'))
                label = r"{}:\n{}".format(parameter_name, parameter.value)
            field = uqbar.graphs.RecordField(
                label=label, name="ugen_{}_output_{}".format(ugen_index, i)
            )
            output_group.append(field)
        return output_group

    @staticmethod
    def _create_ugen_title_field(ugen):
        name = type(ugen).__name__
        calculation_rate = ugen.calculation_rate.name.lower()
        label_template = r"{name}\n({calculation_rate})"
        operator = None
        if isinstance(ugen, BinaryOpUGen):
            operator = BinaryOperator(ugen.special_index).name
            label_template = r"{name}\n[{operator}]\n({calculation_rate})"
        elif isinstance(ugen, UnaryOpUGen):
            operator = UnaryOperator(ugen.special_index).name
            label_template = r"{name}\n[{operator}]\n({calculation_rate})"
        title_field = uqbar.graphs.RecordField(
            label=label_template.format(
                name=name, operator=operator, calculation_rate=calculation_rate
            )
        )
        return title_field

    @staticmethod
    def _style_graph(graph):
        graph.attributes.update(
            {
                "bgcolor": "transparent",
                "color": "lightslategrey",
                "dpi": 72,
                "fontname": "Arial",
                "outputorder": "edgesfirst",
                "overlap": "prism",
                "penwidth": 2,
                "rankdir": "LR",
                "ranksep": 1,
                "splines": "spline",
                "style": ("dotted", "rounded"),
            }
        )
        graph.edge_attributes.update({"penwidth": 2})
        graph.node_attributes.update(
            {
                "fontname": "Arial",
                "fontsize": 12,
                "penwidth": 2,
                "shape": "Mrecord",
                "style": ("filled", "rounded"),
            }
        )

    ### PUBLIC METHODS ###

    @staticmethod
    def graph(synthdef):
        assert isinstance(synthdef, SynthDef)
        graph = uqbar.graphs.Graph(name="synthdef_{}".format(synthdef.actual_name))
        ugen_node_mapping = SynthDefGrapher._create_ugen_node_mapping(synthdef)
        for node in sorted(ugen_node_mapping.values(), key=lambda x: x.name):
            graph.append(node)
        SynthDefGrapher._connect_nodes(synthdef, ugen_node_mapping)
        SynthDefGrapher._style_graph(graph)
        return graph


def compile_synthdef(synthdef, use_anonymous_names=False):
    return SynthDefCompiler.compile_synthdef(synthdef, use_anonymous_names)


def compile_synthdefs(synthdefs, use_anonymous_names=False):
    return SynthDefCompiler.compile_synthdefs(synthdefs, use_anonymous_names)


def decompile_synthdef(value):
    return SynthDefDecompiler.decompile_synthdef(value)


def decompile_synthdefs(value):
    return SynthDefDecompiler.decompile_synthdefs(value)


class SynthDefCompiler:
    @staticmethod
    def compile_synthdef(synthdef, name):
        result = SynthDefCompiler.encode_string(name)
        result += synthdef._compiled_ugen_graph
        return result

    @staticmethod
    def compile_parameters(synthdef):
        result = []
        result.append(
            SynthDefCompiler.encode_unsigned_int_32bit(
                sum(len(_[1]) for _ in synthdef.indexed_parameters)
            )
        )
        for control_ugen in synthdef.control_ugens:
            for parameter in control_ugen.parameters:
                value = parameter.value
                if not isinstance(value, tuple):
                    value = (value,)
                for x in value:
                    result.append(SynthDefCompiler.encode_float(x))
        result.append(
            SynthDefCompiler.encode_unsigned_int_32bit(len(synthdef.indexed_parameters))
        )
        for index, parameter in synthdef.indexed_parameters:
            name = parameter.name
            result.append(SynthDefCompiler.encode_string(name))
            result.append(SynthDefCompiler.encode_unsigned_int_32bit(index))
        return bytes().join(result)

    @staticmethod
    def compile_synthdefs(synthdefs, use_anonymous_names=False):
        def flatten(value):
            if isinstance(value, Sequence) and not isinstance(
                value, (bytes, bytearray)
            ):
                return bytes().join(flatten(x) for x in value)
            return value

        result = []
        encoded_file_type_id = b"SCgf"
        result.append(encoded_file_type_id)
        encoded_file_version = SynthDefCompiler.encode_unsigned_int_32bit(2)
        result.append(encoded_file_version)
        encoded_synthdef_count = SynthDefCompiler.encode_unsigned_int_16bit(
            len(synthdefs)
        )
        result.append(encoded_synthdef_count)
        for synthdef in synthdefs:
            name = synthdef.name
            if not name or use_anonymous_names:
                name = synthdef.anonymous_name
            result.append(SynthDefCompiler.compile_synthdef(synthdef, name))
        result = flatten(result)
        result = bytes(result)
        return result

    @staticmethod
    def compile_ugen(ugen, synthdef):
        outputs = ugen._get_outputs()
        result = []
        result.append(SynthDefCompiler.encode_string(type(ugen).__name__))
        result.append(SynthDefCompiler.encode_unsigned_int_8bit(ugen.calculation_rate))
        result.append(SynthDefCompiler.encode_unsigned_int_32bit(len(ugen.inputs)))
        result.append(SynthDefCompiler.encode_unsigned_int_32bit(len(outputs)))
        result.append(
            SynthDefCompiler.encode_unsigned_int_16bit(int(ugen.special_index))
        )
        for input_ in ugen.inputs:
            result.append(SynthDefCompiler.compile_ugen_input_spec(input_, synthdef))
        for output in outputs:
            result.append(SynthDefCompiler.encode_unsigned_int_8bit(output))
        result = bytes().join(result)
        return result

    @staticmethod
    def compile_ugen_graph(synthdef):
        result = []
        result.append(
            SynthDefCompiler.encode_unsigned_int_32bit(len(synthdef.constants))
        )
        for constant in synthdef.constants:
            result.append(SynthDefCompiler.encode_float(constant))
        result.append(SynthDefCompiler.compile_parameters(synthdef))
        result.append(SynthDefCompiler.encode_unsigned_int_32bit(len(synthdef.ugens)))
        for ugen_index, ugen in enumerate(synthdef.ugens):
            result.append(SynthDefCompiler.compile_ugen(ugen, synthdef))
        result.append(SynthDefCompiler.encode_unsigned_int_16bit(0))
        result = bytes().join(result)
        return result

    @staticmethod
    def compile_ugen_input_spec(input_, synthdef):
        result = []
        if isinstance(input_, float):
            result.append(SynthDefCompiler.encode_unsigned_int_32bit(0xFFFFFFFF))
            constant_index = synthdef._constants.index(input_)
            result.append(SynthDefCompiler.encode_unsigned_int_32bit(constant_index))
        elif isinstance(input_, OutputProxy):
            ugen = input_.source
            output_index = input_.output_index
            ugen_index = synthdef._ugens.index(ugen)
            result.append(SynthDefCompiler.encode_unsigned_int_32bit(ugen_index))
            result.append(SynthDefCompiler.encode_unsigned_int_32bit(output_index))
        else:
            raise Exception("Unhandled input spec: {}".format(input_))
        return bytes().join(result)

    @staticmethod
    def encode_string(value):
        result = bytes(struct.pack(">B", len(value)))
        result += bytes(bytearray(value, encoding="ascii"))
        return result

    @staticmethod
    def encode_float(value):
        return bytes(struct.pack(">f", float(value)))

    @staticmethod
    def encode_unsigned_int_8bit(value):
        return bytes(struct.pack(">B", int(value)))

    @staticmethod
    def encode_unsigned_int_16bit(value):
        return bytes(struct.pack(">H", int(value)))

    @staticmethod
    def encode_unsigned_int_32bit(value):
        return bytes(struct.pack(">I", int(value)))


class SynthDefDecompiler:
    """
    SynthDef decompiler.

    ::

        >>> from supriya import ParameterRate
        >>> from supriya.ugens import Decay, Out, Parameter, SinOsc, SynthDefBuilder, decompile_synthdefs

    ::

        >>> with SynthDefBuilder(
        ...     frequency=440,
        ...     trigger=Parameter(
        ...         value=0.0,
        ...         parameter_rate=ParameterRate.TRIGGER,
        ...     ),
        ... ) as builder:
        ...     sin_osc = SinOsc.ar(frequency=builder["frequency"])
        ...     decay = Decay.kr(
        ...         decay_time=0.5,
        ...         source=builder["trigger"],
        ...     )
        ...     enveloped_sin = sin_osc * decay
        ...     out = Out.ar(bus=0, source=enveloped_sin)
        ...
        >>> synthdef = builder.build()
        >>> supriya.graph(synthdef)  # doctest: +SKIP

    ::

        >>> print(synthdef)
        synthdef:
            name: 001520731aee5371fefab6b505cf64dd
            ugens:
            -   TrigControl.kr: null
            -   Decay.kr:
                    source: TrigControl.kr[0:trigger]
                    decay_time: 0.5
            -   Control.kr: null
            -   SinOsc.ar:
                    frequency: Control.kr[0:frequency]
                    phase: 0.0
            -   BinaryOpUGen(MULTIPLICATION).ar:
                    left: SinOsc.ar[0]
                    right: Decay.kr[0]
            -   Out.ar:
                    bus: 0.0
                    source[0]: BinaryOpUGen(MULTIPLICATION).ar[0]

    ::

        >>> compiled_synthdef = synthdef.compile()
        >>> decompiled_synthdef = decompile_synthdefs(compiled_synthdef)[0]
        >>> supriya.graph(decompiled_synthdef)  # doctest: +SKIP

    ::

        >>> print(decompiled_synthdef)
        synthdef:
            name: 001520731aee5371fefab6b505cf64dd
            ugens:
            -   TrigControl.kr: null
            -   Decay.kr:
                    source: TrigControl.kr[0:trigger]
                    decay_time: 0.5
            -   Control.kr: null
            -   SinOsc.ar:
                    frequency: Control.kr[0:frequency]
                    phase: 0.0
            -   BinaryOpUGen(MULTIPLICATION).ar:
                    left: SinOsc.ar[0]
                    right: Decay.kr[0]
            -   Out.ar:
                    bus: 0.0
                    source[0]: BinaryOpUGen(MULTIPLICATION).ar[0]

    ::

        >>> str(synthdef) == str(decompiled_synthdef)
        True
    """

    ### PRIVATE METHODS ###

    @staticmethod
    def _decode_constants(value, index):
        sdd = SynthDefDecompiler
        constants = []
        constants_count, index = sdd._decode_int_32bit(value, index)
        for _ in range(constants_count):
            constant, index = sdd._decode_float(value, index)
            constants.append(constant)
        return constants, index

    @staticmethod
    def _decode_parameters(value, index):
        sdd = SynthDefDecompiler
        parameter_values = []
        parameter_count, index = sdd._decode_int_32bit(value, index)
        for _ in range(parameter_count):
            parameter_value, index = sdd._decode_float(value, index)
            parameter_values.append(parameter_value)
        parameter_count, index = sdd._decode_int_32bit(value, index)
        parameter_names = []
        parameter_indices = []
        for _ in range(parameter_count):
            parameter_name, index = sdd._decode_string(value, index)
            parameter_index, index = sdd._decode_int_32bit(value, index)
            parameter_names.append(parameter_name)
            parameter_indices.append(parameter_index)
        indexed_parameters = []
        if parameter_count:
            pairs = tuple(zip(parameter_indices, parameter_names))
            pairs = sorted(pairs, key=lambda x: x[0])
            iterator = utils.iterate_nwise(pairs)
            for (index_one, name_one), (index_two, name_two) in iterator:
                value = parameter_values[index_one:index_two]
                if len(value) == 1:
                    value = value[0]
                parameter = Parameter(name=name_one, value=value)
                indexed_parameters.append((index_one, parameter))
            index_one, name_one = pairs[-1]
            value = parameter_values[index_one:]
            if len(value) == 1:
                value = value[0]
            parameter = Parameter(name=name_one, value=value)
            indexed_parameters.append((index_one, parameter))
            indexed_parameters.sort(key=lambda x: parameter_names.index(x[1].name))
        indexed_parameters = collections.OrderedDict(indexed_parameters)
        return indexed_parameters, index

    @staticmethod
    def _decompile_synthdef(value, index):
        from .. import ugens

        sdd = SynthDefDecompiler
        synthdef = None
        name, index = sdd._decode_string(value, index)
        constants, index = sdd._decode_constants(value, index)
        indexed_parameters, index = sdd._decode_parameters(value, index)
        decompiled_ugens = []
        ugen_count, index = sdd._decode_int_32bit(value, index)
        for i in range(ugen_count):
            ugen_name, index = sdd._decode_string(value, index)
            calculation_rate, index = sdd._decode_int_8bit(value, index)
            calculation_rate = CalculationRate(calculation_rate)
            input_count, index = sdd._decode_int_32bit(value, index)
            output_count, index = sdd._decode_int_32bit(value, index)
            special_index, index = sdd._decode_int_16bit(value, index)
            inputs = []
            for _ in range(input_count):
                ugen_index, index = sdd._decode_int_32bit(value, index)
                if ugen_index == 0xFFFFFFFF:
                    constant_index, index = sdd._decode_int_32bit(value, index)
                    constant_index = int(constant_index)
                    inputs.append(constants[constant_index])
                else:
                    ugen = decompiled_ugens[ugen_index]
                    ugen_output_index, index = sdd._decode_int_32bit(value, index)
                    output_proxy = ugen[ugen_output_index]
                    inputs.append(output_proxy)
            for _ in range(output_count):
                output_rate, index = sdd._decode_int_8bit(value, index)
            ugen_class = getattr(ugens, ugen_name, None)
            ugen = UGen.__new__(ugen_class)
            if issubclass(ugen_class, Control):
                starting_control_index = special_index
                parameters = sdd._collect_parameters_for_control(
                    calculation_rate,
                    indexed_parameters,
                    inputs,
                    output_count,
                    starting_control_index,
                    ugen_class,
                )
                ugen_class.__init__(
                    ugen,
                    parameters=parameters,
                    starting_control_index=starting_control_index,
                    calculation_rate=calculation_rate,
                )
            else:
                kwargs = {}
                if not ugen._unexpanded_input_names:
                    for i, input_name in enumerate(ugen._ordered_input_names):
                        kwargs[input_name] = inputs[i]
                else:
                    for i, input_name in enumerate(ugen._ordered_input_names):
                        if input_name not in ugen._unexpanded_input_names:
                            kwargs[input_name] = inputs[i]
                        else:
                            kwargs[input_name] = tuple(inputs[i:])
                ugen._channel_count = output_count
                UGen.__init__(
                    ugen,
                    calculation_rate=calculation_rate,
                    special_index=special_index,
                    **kwargs,
                )
            decompiled_ugens.append(ugen)
        variants_count, index = sdd._decode_int_16bit(value, index)
        synthdef = SynthDef(ugens=decompiled_ugens, name=name)
        if synthdef.name == synthdef.anonymous_name:
            synthdef._name = None
        return synthdef, index

    @staticmethod
    def _decode_string(value, index):
        length = struct.unpack(">B", value[index : index + 1])[0]
        index += 1
        result = value[index : index + length]
        result = result.decode("ascii")
        index += length
        return result, index

    @staticmethod
    def _decode_float(value, index):
        result = struct.unpack(">f", value[index : index + 4])[0]
        index += 4
        return result, index

    @staticmethod
    def _decode_int_8bit(value, index):
        result = struct.unpack(">B", value[index : index + 1])[0]
        index += 1
        return result, index

    @staticmethod
    def _decode_int_16bit(value, index):
        result = struct.unpack(">H", value[index : index + 2])[0]
        index += 2
        return result, index

    @staticmethod
    def _decode_int_32bit(value, index):
        result = struct.unpack(">I", value[index : index + 4])[0]
        index += 4
        return result, index

    @staticmethod
    def _collect_parameters_for_control(
        calculation_rate,
        indexed_parameters,
        inputs,
        output_count,
        starting_control_index,
        ugen_class,
    ):
        parameter_rate = ParameterRate.CONTROL
        if issubclass(ugen_class, TrigControl):
            parameter_rate = ParameterRate.TRIGGER
        elif calculation_rate == CalculationRate.SCALAR:
            parameter_rate = ParameterRate.SCALAR
        elif calculation_rate == CalculationRate.AUDIO:
            parameter_rate = ParameterRate.AUDIO
        parameters = []
        collected_output_count = 0
        lag = 0.0
        while collected_output_count < output_count:
            if inputs:
                lag = inputs[collected_output_count]
            parameter = indexed_parameters[
                starting_control_index + collected_output_count
            ]
            parameter.parameter_rate = parameter_rate
            if lag:
                parameter.lag = lag
            parameters.append(parameter)
            collected_output_count += len(parameter)
        return parameters

    ### PUBLIC METHODS ###

    @staticmethod
    def decompile_synthdef(value):
        synthdefs = SynthDefDecompiler.decompile_synthdefs(value)
        assert len(synthdefs) == 1
        return synthdefs[0]

    @staticmethod
    def decompile_synthdefs(value):
        synthdefs = []
        sdd = SynthDefDecompiler
        index = 4
        assert value[:index] == b"SCgf"
        file_version, index = sdd._decode_int_32bit(value, index)
        synthdef_count, index = sdd._decode_int_16bit(value, index)
        for _ in range(synthdef_count):
            synthdef, index = sdd._decompile_synthdef(value, index)
            synthdefs.append(synthdef)
        return synthdefs
