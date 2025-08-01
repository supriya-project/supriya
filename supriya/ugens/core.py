import abc
import copy
import enum
import hashlib
import inspect
import math
import operator
import struct
import subprocess
import tempfile
import threading
import uuid
from enum import Enum
from itertools import zip_longest
from pathlib import Path
from types import MappingProxyType
from typing import (
    Callable,
    Iterable,
    Iterator,
    Literal,
    Mapping,
    NamedTuple,
    Optional,
    Protocol,
    Sequence,
    SupportsFloat,
    SupportsInt,
    Type,
    TypeAlias,
    Union,
    cast,
    overload,
    runtime_checkable,
)

from uqbar.graphs import Edge, Graph, Node, RecordField, RecordGroup

from .. import sclang
from ..enums import (
    BinaryOperator,
    CalculationRate,
    DoneAction,
    ParameterRate,
    SignalRange,
    UnaryOperator,
)
from ..typing import MISSING, CalculationRateLike, Default, Missing, ParameterRateLike
from ..utils import flatten, iterate_nwise


class Check(Enum):
    """
    A UGen input rate check configuration.
    """

    NONE = 0
    SAME_AS_FIRST = 1
    SAME_OR_SLOWER = 2


class Param(NamedTuple):
    """
    A UGen input configuration.
    """

    default: Default | Missing | float | None = None
    check: Check = Check.NONE
    unexpanded: bool = False


def _add_init(
    cls,
    params: dict[str, "Param"],
    is_multichannel: bool,
    channel_count: int,
    fixed_channel_count: bool,
) -> None:
    parent_class = inspect.getmro(cls)[1]
    args = ["self", "*", "calculation_rate: CalculationRateLike"]
    body = []
    if is_multichannel and not fixed_channel_count:
        args.append(f"channel_count: int = {channel_count or 1}")
        body.extend(
            [
                "if not isinstance(channel_count, int):",
                "    raise ValueError(repr(channel_count))",
                "self._channel_count = channel_count",
            ]
        )
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
        type_ = "UGenVectorInput" if param.unexpanded else "UGenScalarInput"
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
            [f"return self._inputs[{index}:]"]
            if unexpanded
            else [f"return self._inputs[{index}]"]
        ),
        decorator=property,
        globals_=_get_fn_globals(),
        override=True,
        return_type=UGenVector if unexpanded else UGenScalar,
    )


def _add_rate_fn(
    cls,
    rate: CalculationRate | None,
    params: dict[str, "Param"],
    is_multichannel: bool,
    channel_count: int,
    fixed_channel_count: bool,
) -> None:
    args = ["cls"]
    if params:
        args.append("*")
    for key, param in params.items():
        value_repr = _format_value(param.default)
        prefix = f"{key}: UGenRecursiveInput"
        args.append(
            f"{prefix} = {value_repr}"
            if not isinstance(param.default, Missing)
            else prefix
        )
    body = ["return cls._new_expanded("]
    if rate is None:
        body.append("    calculation_rate=None,")
    else:
        body.append(f"    calculation_rate=CalculationRate.{rate.name},")
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
        return_type=UGenOperable,
    )


def _create_fn(
    *,
    cls,
    name: str,
    args: list[str],
    body: list[str],
    return_type,
    globals_: dict[str, Type] | None = None,
    decorator: Callable | None = None,
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
    namespace: dict[str, Callable] = {}
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
    elif isinstance(value, enum.Enum):
        value_repr = f"{type(value).__name__}.{value.name}"
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
        "SupportsFloat": SupportsFloat,
        "UGenRecursiveInput": UGenRecursiveInput,
        "UGenScalar": UGenScalar,
        "UGenSerializable": UGenSerializable,
        "UGenVector": UGenVector,
        "UGenScalarInput": UGenScalarInput,
        "UGenVectorInput": UGenVectorInput,
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
    signal_range: int | None = None,
) -> Type["UGen"]:
    params: dict[str, Param] = {}
    unexpanded_keys = []
    valid_calculation_rates = []
    for name, value in cls.__dict__.items():
        if not isinstance(value, Param):
            continue
        params[name] = value
        if value.unexpanded:
            unexpanded_keys.append(name)
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
    cls._ordered_keys = tuple(params.keys())
    cls._unexpanded_keys = frozenset(unexpanded_keys)
    cls._valid_calculation_rates = tuple(valid_calculation_rates)
    if signal_range is not None:
        cls._signal_range = SignalRange.from_expr(signal_range)
    return cls


def param(
    default: Default | Missing | float | None = MISSING,
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
    signal_range: int | None = None,
) -> Callable[[Type["UGen"]], Type["UGen"]]:
    """
    Decorate a UGen class.

    Akin to dataclasses.dataclass.

    Collects parameter descriptors and generates initializer and rate class methods.
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


def _get_method_for_rate(cls, calculation_rate: CalculationRate) -> Callable:
    if calculation_rate == CalculationRate.AUDIO:
        return cls.ar
    elif calculation_rate == CalculationRate.CONTROL:
        return cls.kr
    elif calculation_rate == CalculationRate.SCALAR:
        if hasattr(cls, "ir"):
            return cls.ir
        return cls.kr
    return cls.new


def _compute_binary_op(
    left: "UGenRecursiveInput",
    right: "UGenRecursiveInput",
    special_index: BinaryOperator,
    float_operator: Callable | None = None,
) -> "UGenOperable":
    def recurse(
        all_expanded_params: UGenRecursiveParams,
    ) -> "UGenOperable":
        if not isinstance(all_expanded_params, dict) and len(all_expanded_params) == 1:
            all_expanded_params = all_expanded_params[0]
        if isinstance(all_expanded_params, dict):
            if (
                isinstance(left, SupportsFloat)
                and isinstance(right, SupportsFloat)
                and float_operator is not None
            ):
                return ConstantProxy(float_operator(float(left), float(right)))
            return BinaryOpUGen._new_single(
                calculation_rate=max(
                    [
                        CalculationRate.from_expr(left),
                        CalculationRate.from_expr(right),
                    ]
                ),
                special_index=special_index,
                **all_expanded_params,
            )
        return UGenVector(
            *(recurse(expanded_params) for expanded_params in all_expanded_params)
        )

    return recurse(UGen._expand_params({"left": left, "right": right}))


def _compute_unary_op(
    source: "UGenRecursiveInput",
    special_index: UnaryOperator,
    float_operator: Callable | None = None,
) -> "UGenOperable":
    def recurse(
        all_expanded_params: UGenRecursiveParams,
    ) -> "UGenOperable":
        if not isinstance(all_expanded_params, dict) and len(all_expanded_params) == 1:
            all_expanded_params = all_expanded_params[0]
        if isinstance(all_expanded_params, dict):
            if isinstance(source, SupportsFloat) and float_operator is not None:
                return ConstantProxy(float_operator(float(source)))
            return UnaryOpUGen._new_single(
                calculation_rate=max(
                    [
                        CalculationRate.from_expr(source),
                    ]
                ),
                special_index=special_index,
                **all_expanded_params,
            )
        return UGenVector(
            *(recurse(expanded_params) for expanded_params in all_expanded_params)
        )

    return recurse(UGen._expand_params({"source": source}))


def _compute_ugen_map(
    source: "UGenRecursiveInput", ugen: Type["UGen"], **kwargs: "UGenRecursiveInput"
) -> "UGenOperable":
    if isinstance(source, UGenSerializable):
        source = source.serialize()
    if not isinstance(source, Sequence):
        source = UGenVector(source)
    outputs: list[UGenOperable] = []
    for input_ in source:
        calculation_rate = CalculationRate.from_expr(input_)
        method = _get_method_for_rate(ugen, calculation_rate)
        outputs.append(method(source=input_, **kwargs))
    if len(outputs) == 1:
        return outputs[0]
    return UGenVector(*outputs)


class UGenOperable:
    """
    Mixin for UGen arithmetic operations.
    """

    def __abs__(self) -> "UGenOperable":
        """
        Compute absolute value of UGen graph.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = abs(ugen_graph)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(ABSOLUTE_VALUE).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(ABSOLUTE_VALUE).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self,
            special_index=UnaryOperator.ABSOLUTE_VALUE,
            float_operator=operator.abs,
        )

    def __add__(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Add ``expr`` to UGen graph.

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph + expr
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(ADDITION).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(ADDITION).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        Supports short-circuiting:

        ::

            >>> result = ugen_graph + 0
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.ADDITION,
            float_operator=operator.add,
        )

    def __and__(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute bitwise AND of UGen graph and ``expr``.

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph & expr
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(BITWISE_AND).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(BITWISE_AND).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.BITWISE_AND,
            float_operator=operator.and_,
        )

    def __ceil__(self) -> "UGenOperable":
        """
        Calculate ceiling of ugen graph.

        ::

            >>> import math
            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = math.ceil(ugen_graph)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(CEILING).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(CEILING).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self, special_index=UnaryOperator.CEILING, float_operator=math.ceil
        )

    def __floor__(self) -> "UGenOperable":
        """
        Calculate floor of ugen graph.

        ::

            >>> import math
            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = math.floor(ugen_graph)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(FLOOR).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(FLOOR).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self, special_index=UnaryOperator.FLOOR, float_operator=math.floor
        )

    def __floordiv__(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute integer division of UGen graph by ``expr``.

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph // expr
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(INTEGER_DIVISION).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(INTEGER_DIVISION).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.INTEGER_DIVISION,
            float_operator=operator.floordiv,
        )

    def __ge__(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Test if UGen graph is greater than or equal to ``expr``.

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph >= expr
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(GREATER_THAN_OR_EQUAL).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(GREATER_THAN_OR_EQUAL).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.GREATER_THAN_OR_EQUAL,
            float_operator=operator.ge,
        )

    def __graph__(self) -> Graph:
        """
        Generate Graphviz graph of UGen graph.
        """
        return self.__synthdef__().__graph__()

    def __gt__(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Test if UGen graph is greater than ``expr``.

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph > expr
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(GREATER_THAN).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(GREATER_THAN).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.GREATER_THAN,
            float_operator=operator.gt,
        )

    def __invert__(self) -> "UGenOperable":
        """
        Compute bitwise inversion of UGen graph.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ~ugen_graph
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(BIT_NOT).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(BIT_NOT).ar/1:
                        source: SinOsc.ar/1[0]

        """

        return _compute_unary_op(
            source=self,
            special_index=UnaryOperator.BIT_NOT,
            float_operator=operator.not_,
        )

    def __iter__(self) -> Iterator["UGenOperable"]:
        raise NotImplementedError

    def __le__(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Test if UGen graph is less than or equal to ``expr``.

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph <= expr
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(LESS_THAN_OR_EQUAL).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(LESS_THAN_OR_EQUAL).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.LESS_THAN_OR_EQUAL,
            float_operator=operator.le,
        )

    def __lshift__(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Bitshift UGen graph to the left by ``expr``.

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph << expr
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(SHIFT_LEFT).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(SHIFT_LEFT).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.SHIFT_LEFT,
            float_operator=operator.lshift,
        )

    def __lt__(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Test if UGen graph is less than ``expr``.

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph < expr
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(LESS_THAN).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(LESS_THAN).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.LESS_THAN,
            float_operator=operator.lt,
        )

    def __mod__(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute modulo of UGen graph and ``expr``:

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph % expr
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(MODULO).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(MODULO).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.MODULO,
            float_operator=operator.mod,
        )

    def __mul__(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Multiply UGen graph and ``expr``.

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph * expr
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(MULTIPLICATION).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(MULTIPLICATION).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        Supports short-circuiting:

        ::

            >>> ugen_graph * 0
            <UGenVector([<0.0>, <0.0>])>

        ::

            >>> result = ugen_graph * 1
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0

        ::

            >>> result = ugen_graph * -1
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(NEGATIVE).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(NEGATIVE).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.MULTIPLICATION,
            float_operator=operator.mul,
        )

    def __neg__(self) -> "UGenOperable":
        """
        Compute negative of UGen graph.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = -ugen_graph
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(NEGATIVE).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(NEGATIVE).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self,
            special_index=UnaryOperator.NEGATIVE,
            float_operator=operator.neg,
        )

    def __or__(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute bitwise OR of UGen graph and ``expr``.

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph | expr
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(BITWISE_OR).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(BITWISE_OR).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.BITWISE_OR,
            float_operator=operator.or_,
        )

    def __pow__(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Raise UGen graph to the power of ``expr``.

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph ** expr
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(POWER).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(POWER).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.POWER,
            float_operator=operator.pow,
        )

    def __radd__(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Add UGen graph to ``expr`` (reflected).

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = [1, 2, 3]
            >>> result = expr + ugen_graph
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   BinaryOpUGen(ADDITION).ar/0:
                        left: 1.0
                        right: SinOsc.ar/0[0]
                -   BinaryOpUGen(ADDITION).ar/1:
                        left: 3.0
                        right: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(ADDITION).ar/2:
                        left: 2.0
                        right: SinOsc.ar/1[0]

        """
        return _compute_binary_op(
            left=expr,
            right=self,
            special_index=BinaryOperator.ADDITION,
            float_operator=operator.add,
        )

    def __rand__(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute reflected bitwise AND of ``expr`` and UGen graph (reflected).

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = [1, 2, 3]
            >>> result = expr & ugen_graph
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   BinaryOpUGen(BITWISE_AND).ar/0:
                        left: 1.0
                        right: SinOsc.ar/0[0]
                -   BinaryOpUGen(BITWISE_AND).ar/1:
                        left: 3.0
                        right: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(BITWISE_AND).ar/2:
                        left: 2.0
                        right: SinOsc.ar/1[0]

        """
        return _compute_binary_op(
            left=expr,
            right=self,
            special_index=BinaryOperator.BITWISE_AND,
            float_operator=operator.and_,
        )

    def __rfloordiv__(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute integer division of ``expr`` by UGen graph (reflected).

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = [1, 2, 3]
            >>> result = expr // ugen_graph
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   BinaryOpUGen(INTEGER_DIVISION).ar/0:
                        left: 1.0
                        right: SinOsc.ar/0[0]
                -   BinaryOpUGen(INTEGER_DIVISION).ar/1:
                        left: 3.0
                        right: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(INTEGER_DIVISION).ar/2:
                        left: 2.0
                        right: SinOsc.ar/1[0]

        """
        return _compute_binary_op(
            left=expr,
            right=self,
            special_index=BinaryOperator.INTEGER_DIVISION,
            float_operator=operator.floordiv,
        )

    def __rmod__(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute reflected modulo of ``expr`` and UGen graph (reflected).

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = [1, 2, 3]
            >>> result = expr % ugen_graph
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   BinaryOpUGen(MODULO).ar/0:
                        left: 1.0
                        right: SinOsc.ar/0[0]
                -   BinaryOpUGen(MODULO).ar/1:
                        left: 3.0
                        right: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(MODULO).ar/2:
                        left: 2.0
                        right: SinOsc.ar/1[0]

        """
        return _compute_binary_op(
            left=expr,
            right=self,
            special_index=BinaryOperator.MODULO,
            float_operator=operator.mod,
        )

    def __rmul__(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Multiple ``expr`` by UGen graph (reflected).

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = [1, 2, 3]
            >>> result = expr - ugen_graph
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   BinaryOpUGen(SUBTRACTION).ar/0:
                        left: 1.0
                        right: SinOsc.ar/0[0]
                -   BinaryOpUGen(SUBTRACTION).ar/1:
                        left: 3.0
                        right: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(SUBTRACTION).ar/2:
                        left: 2.0
                        right: SinOsc.ar/1[0]

        Supports short-circuiting:

        ::

            >>> result = 0 - ugen_graph
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(NEGATIVE).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(NEGATIVE).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_binary_op(
            left=expr,
            right=self,
            special_index=BinaryOperator.MULTIPLICATION,
            float_operator=operator.mul,
        )

    def __ror__(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute bitwise OR of ``expr`` and UGen graph (reflected).

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = [1, 2, 3]
            >>> result = expr | ugen_graph
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   BinaryOpUGen(BITWISE_OR).ar/0:
                        left: 1.0
                        right: SinOsc.ar/0[0]
                -   BinaryOpUGen(BITWISE_OR).ar/1:
                        left: 3.0
                        right: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(BITWISE_OR).ar/2:
                        left: 2.0
                        right: SinOsc.ar/1[0]

        """
        return _compute_binary_op(
            left=expr,
            right=self,
            special_index=BinaryOperator.BITWISE_OR,
            float_operator=operator.or_,
        )

    def __rpow__(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Raise ``expr`` to the power of UGen graph (reflected).

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = [1, 2, 3]
            >>> result = expr ** ugen_graph
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   BinaryOpUGen(POWER).ar/0:
                        left: 1.0
                        right: SinOsc.ar/0[0]
                -   BinaryOpUGen(POWER).ar/1:
                        left: 3.0
                        right: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(POWER).ar/2:
                        left: 2.0
                        right: SinOsc.ar/1[0]

        """
        return _compute_binary_op(
            left=expr,
            right=self,
            special_index=BinaryOperator.POWER,
            float_operator=operator.pow,
        )

    def __rlshift__(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Bitshift ``expr`` to the left by UGen graph (reflected).

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = [1, 2, 3]
            >>> result = expr << ugen_graph
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   BinaryOpUGen(SHIFT_LEFT).ar/0:
                        left: 1.0
                        right: SinOsc.ar/0[0]
                -   BinaryOpUGen(SHIFT_LEFT).ar/1:
                        left: 3.0
                        right: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(SHIFT_LEFT).ar/2:
                        left: 2.0
                        right: SinOsc.ar/1[0]

        """
        return _compute_binary_op(
            left=expr,
            right=self,
            special_index=BinaryOperator.SHIFT_LEFT,
            float_operator=operator.lshift,
        )

    def __rrshift__(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Bitshift ``expr`` to the right by UGen graph (reflected).

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = [1, 2, 3]
            >>> result = expr >> ugen_graph
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   BinaryOpUGen(SHIFT_RIGHT).ar/0:
                        left: 1.0
                        right: SinOsc.ar/0[0]
                -   BinaryOpUGen(SHIFT_RIGHT).ar/1:
                        left: 3.0
                        right: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(SHIFT_RIGHT).ar/2:
                        left: 2.0
                        right: SinOsc.ar/1[0]

        """
        return _compute_binary_op(
            left=expr,
            right=self,
            special_index=BinaryOperator.SHIFT_RIGHT,
            float_operator=operator.rshift,
        )

    def __rshift__(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Bitshift UGen graph to the right by ``expr``.

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph >> expr
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(SHIFT_RIGHT).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(SHIFT_RIGHT).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.SHIFT_RIGHT,
            float_operator=operator.rshift,
        )

    def __rsub__(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Subtract UGen graph from ``expr`` (reflected).

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = [1, 2, 3]
            >>> result = expr - ugen_graph
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   BinaryOpUGen(SUBTRACTION).ar/0:
                        left: 1.0
                        right: SinOsc.ar/0[0]
                -   BinaryOpUGen(SUBTRACTION).ar/1:
                        left: 3.0
                        right: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(SUBTRACTION).ar/2:
                        left: 2.0
                        right: SinOsc.ar/1[0]

        Supports short-circuiting:

        ::

            >>> result = 0 - ugen_graph
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(NEGATIVE).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(NEGATIVE).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_binary_op(
            left=expr,
            right=self,
            special_index=BinaryOperator.SUBTRACTION,
            float_operator=operator.sub,
        )

    def __rtruediv__(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute true division of ``expr`` by UGen graph (reflected).

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = [1, 2, 3]
            >>> result = expr / ugen_graph
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   BinaryOpUGen(FLOAT_DIVISION).ar/0:
                        left: 1.0
                        right: SinOsc.ar/0[0]
                -   BinaryOpUGen(FLOAT_DIVISION).ar/1:
                        left: 3.0
                        right: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(FLOAT_DIVISION).ar/2:
                        left: 2.0
                        right: SinOsc.ar/1[0]

        """
        return _compute_binary_op(
            left=expr,
            right=self,
            special_index=BinaryOperator.FLOAT_DIVISION,
            float_operator=operator.truediv,
        )

    def __rxor__(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute bitwise XOR of ``expr`` and UGen graph (reflected).

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = [1, 2, 3]
            >>> result = expr ^ ugen_graph
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   BinaryOpUGen(BITWISE_XOR).ar/0:
                        left: 1.0
                        right: SinOsc.ar/0[0]
                -   BinaryOpUGen(BITWISE_XOR).ar/1:
                        left: 3.0
                        right: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(BITWISE_XOR).ar/2:
                        left: 2.0
                        right: SinOsc.ar/1[0]

        """
        return _compute_binary_op(
            left=expr,
            right=self,
            special_index=BinaryOperator.BITWISE_XOR,
            float_operator=operator.xor,
        )

    def __str__(self) -> str:
        return str(self.__synthdef__())

    def __sub__(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Subtract ``expr`` from UGen graph.

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph - expr
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(SUBTRACTION).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(SUBTRACTION).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        Supports short-circuiting:

        ::

            >>> result = ugen_graph - 0
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.SUBTRACTION,
            float_operator=operator.sub,
        )

    def __synthdef__(self) -> "SynthDef":
        """
        Generate a SynthDef from UGen graph.

        Typically used for rendering debug information about the UGen graph, or
        for generating Graphviz graphs.
        """

        def recurse(operable) -> None:
            if isinstance(operable, UGenVector):
                for x in operable:
                    recurse(x)
            elif isinstance(operable, OutputProxy):
                recurse(operable.ugen)
            elif isinstance(operable, UGen):
                if operable in ugens:
                    return
                ugens.append(operable)
                for input_ in operable.inputs:
                    recurse(input_)

        builder = SynthDefBuilder()
        ugens: list[UGen] = []
        recurse(copy.deepcopy(self))
        for ugen in ugens:
            ugen._uuid = builder._uuid
            builder._add_ugen(ugen)
        return builder.build(name="...", optimize=False)

    def __truediv__(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute true division of UGen graph by ``expr``.

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph / expr
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(FLOAT_DIVISION).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(FLOAT_DIVISION).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        Supports short-circuiting:

        ::

            >>> result = ugen_graph / 1
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.FLOAT_DIVISION,
            float_operator=operator.truediv,
        )

    def __xor__(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute bitwise XOR of UGen graph and ``expr``.

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph ^ expr
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(BITWISE_XOR).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(BITWISE_XOR).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.BITWISE_XOR,
            float_operator=operator.xor,
        )

    def absdiff(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute absolute difference between UGen graph and ``expr``.

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph.absdiff(expr)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(ABSOLUTE_DIFFERENCE).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(ABSOLUTE_DIFFERENCE).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.ABSOLUTE_DIFFERENCE,
            float_operator=lambda a, b: abs(a - b),
        )

    def am_clip(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute two quadrant multiplication between UGen graph and ``expr``.

        - 0 when b <= 0
        - a * b when b > 0

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph.am_clip(expr)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(AMCLIP).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(AMCLIP).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.AMCLIP,
        )

    def amplitude_to_db(self) -> "UGenOperable":
        """
        Convert UGen graph from amplitude to decibels.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.amplitude_to_db()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(AMPLITUDE_TO_DB).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(AMPLITUDE_TO_DB).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self, special_index=UnaryOperator.AMPLITUDE_TO_DB
        )

    def acos(self) -> "UGenOperable":
        """
        Compute the arccosine of UGen graph.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.acos()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(ARCCOS).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(ARCCOS).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self,
            special_index=UnaryOperator.ARCCOS,
            float_operator=math.acos,
        )

    def asin(self) -> "UGenOperable":
        """
        Compute the arcsine of UGen graph.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.asin()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(ARCSIN).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(ARCSIN).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self,
            special_index=UnaryOperator.ARCSIN,
            float_operator=math.asin,
        )

    def atan(self) -> "UGenOperable":
        """
        Compute the arctangent of UGen graph.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.atan()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(ARCTAN).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(ARCTAN).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self,
            special_index=UnaryOperator.ARCTAN,
            float_operator=math.atan,
        )

    def atan2(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute the arctangen of UGen graph divided by ``expr``.

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph.atan2(expr)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(ATAN2).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(ATAN2).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.ATAN2,
            float_operator=math.atan2,
        )

    def bi_lin_rand(self) -> "UGenOperable":
        """
        Compute a bilateral linearly distributed random number from - UGen graph to + UGen graph.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.bi_lin_rand()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(BILINRAND).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(BILINRAND).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self,
            special_index=UnaryOperator.BILINRAND,
        )

    def bi_rand(self) -> "UGenOperable":
        """
        Compute a random number between - UGen graph and + UGen graph.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.bi_rand()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(RAND2).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(RAND2).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self,
            special_index=UnaryOperator.RAND2,
        )

    def clip(
        self,
        minimum: "UGenRecursiveInput",
        maximum: "UGenRecursiveInput",
    ) -> "UGenOperable":
        """
        Clip UGen graph between ``maximum`` and ``minimum``.

        ::

            >>> from supriya.ugens import LFNoise1, SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.clip(
            ...     maximum=LFNoise1.kr(),
            ...     minimum=LFNoise1.kr(),
            ... )
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   LFNoise1.kr/0:
                        frequency: 500.0
                -   LFNoise1.kr/1:
                        frequency: 500.0
                -   Clip.ar/0:
                        source: SinOsc.ar/0[0]
                        minimum: LFNoise1.kr/0[0]
                        maximum: LFNoise1.kr/1[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   Clip.ar/1:
                        source: SinOsc.ar/1[0]
                        minimum: LFNoise1.kr/0[0]
                        maximum: LFNoise1.kr/1[0]

        """
        from . import Clip

        return _compute_ugen_map(
            self, cast(Type[UGen], Clip), minimum=minimum, maximum=maximum
        )

    def clip2(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute bilateral clipping of UGen graph by ``expr``.

        - clip a to +/- b

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph.clip2(expr)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(CLIP2).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(CLIP2).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.CLIP2,
        )

    def cos(self) -> "UGenOperable":
        """
        Compute cosine of UGen graph.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.cos()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(COS).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(COS).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self,
            special_index=UnaryOperator.COS,
            float_operator=math.cos,
        )

    def cosh(self) -> "UGenOperable":
        """
        Compute the hyperbolic cosine of UGen graph.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.cosh()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(COSH).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(COSH).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self,
            special_index=UnaryOperator.COSH,
            float_operator=math.cosh,
        )

    def cubed(self) -> "UGenOperable":
        """
        Compute the cube of UGen graph.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.cubed()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(CUBED).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(CUBED).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self,
            special_index=UnaryOperator.CUBED,
            float_operator=lambda x: x**3,
        )

    def db_to_amplitude(self) -> "UGenOperable":
        """
        Convert UGen graph from decibels to amplitude.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.db_to_amplitude()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(DB_TO_AMPLITUDE).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(DB_TO_AMPLITUDE).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self, special_index=UnaryOperator.DB_TO_AMPLITUDE
        )

    def difference_of_squares(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute the difference of squares of UGen graph and ``expr``.

        - (a * a) - (b * b)

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph.difference_of_squares(expr)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(DIFFERENCE_OF_SQUARES).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(DIFFERENCE_OF_SQUARES).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.DIFFERENCE_OF_SQUARES,
            float_operator=lambda a, b: (a * a) - (b * b),
        )

    def digit_value(self) -> "UGenOperable":
        """
        Compute the digit value of UGen graph.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.digit_value()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(AS_INT).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(AS_INT).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self,
            special_index=UnaryOperator.AS_INT,
            float_operator=lambda x: divmod(x, 1.0)[0],
        )

    def distort(self) -> "UGenOperable":
        """
        Compute non-linear distortion of UGen graph.

        - x / (1 + abs(x))

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.softclip()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(SOFTCLIP).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(SOFTCLIP).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self,
            special_index=UnaryOperator.DISTORT,
            float_operator=lambda x: x / (1 + abs(x)),
        )

    def exceeds(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Threshold UGen graph by ``expr``.

        - 0 when a < b, otherwise a

        Equivalent to sclang's ``threshold`` method, but renamed due to name
        conflicts with many UGen parameters.

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph.exceeds(expr)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(THRESHOLD).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(THRESHOLD).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.THRESHOLD,
            float_operator=lambda a, b: 0.0 if a < b else a,
        )

    def exponential_rand_range(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute an exponentially-distributed random number in the interval of UGen graph to ``expr``.

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph.exponential_rand_range(expr)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(EXPRANDRANGE).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(EXPRANDRANGE).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.EXPRANDRANGE,
        )

    def excess(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute the residual of clipping UGen graph by ``expr``

        - a - clip2(a,b))

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph.excess(expr)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(EXCESS).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(EXCESS).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.EXCESS,
        )

    def exponential(self) -> "UGenOperable":
        """
        Compute the exponential of UGen graph.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.exponential()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(EXPONENTIAL).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(EXPONENTIAL).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(source=self, special_index=UnaryOperator.EXPONENTIAL)

    def fill(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.FILL,
        )

    def fold2(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute bilateral folding of UGen graph by ``expr``.

        - fold a to +/- b

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph.fold2(expr)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(FOLD2).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(FOLD2).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.FOLD2,
        )

    def fractional_part(self) -> "UGenOperable":
        """
        Compute the fractional part of UGen graph.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.fractional_part()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(FRACTIONAL_PART).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(FRACTIONAL_PART).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self,
            special_index=UnaryOperator.FRACTIONAL_PART,
            float_operator=lambda x: divmod(x, 1.0)[1],
        )

    def gcd(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute the greatest common divisor of UGen graph and ``expr``.

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph.gcd(expr)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(GREATEST_COMMON_DIVISOR).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(GREATEST_COMMON_DIVISOR).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.GREATEST_COMMON_DIVISOR,
            float_operator=lambda a, b: math.gcd(a, b),
        )

    def hanning_window(self) -> "UGenOperable":
        """
        Compute Hanning window from UGen graph.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.hanning_window()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(HANNING_WINDOW).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(HANNING_WINDOW).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self, special_index=UnaryOperator.HANNING_WINDOW
        )

    def hypot(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute the hypotenuse of UGen graph and ``expr``.

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph.hypot(expr)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(HYPOT).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(HYPOT).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.HYPOT,
            float_operator=math.hypot,
        )

    def hypotx(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute the hypotenuse approximation of UGen graph and ``expr``.

        - abs(x) + abs(y) - ((sqrt(2) - 1) * min(abs(x), abs(y)))

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph.hypotx(expr)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(HYPOTX).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(HYPOTX).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.HYPOTX,
        )

    def hz_to_midi(self) -> "UGenOperable":
        """
        Convert UGen graph from Hertz to MIDI note number.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.hz_to_midi()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(HZ_TO_MIDI).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(HZ_TO_MIDI).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(source=self, special_index=UnaryOperator.HZ_TO_MIDI)

    def hz_to_octave(self) -> "UGenOperable":
        """
        Convert UGen graph from Hertz to octave number.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.hz_to_octave()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(HZ_TO_OCTAVE).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(HZ_TO_OCTAVE).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(source=self, special_index=UnaryOperator.HZ_TO_OCTAVE)

    def is_equal_to(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute equality of UGen graph and ``expr``.

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph.is_equal_to(expr)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(EQUAL).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(EQUAL).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.EQUAL,
            float_operator=lambda a, b: float(a == b),
        )

    def is_not_equal_to(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute inequality of UGen graph and ``expr``.

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph.is_not_equal_to(expr)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(NOT_EQUAL).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(NOT_EQUAL).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.NOT_EQUAL,
            float_operator=lambda a, b: float(a != b),
        )

    def lagged(
        self,
        lag_time_up: "UGenRecursiveInput" = 0.5,
        lag_time_down: Optional["UGenRecursiveInput"] = None,
        factor: Literal[1, 2, 3] = 1,
    ) -> "UGenOperable":
        """
        Lag UGen graph.

        If ``lag_time_down`` is non-null, use an "up/down" variant.

        If ``factor`` is 2 or 3, use the Lag2 or Lag3 variant.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.lagged(0.25)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   Lag.ar/0:
                        source: SinOsc.ar/0[0]
                        lag_time: 0.25
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   Lag.ar/1:
                        source: SinOsc.ar/1[0]
                        lag_time: 0.25

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.lagged(lag_time_up=0.25, lag_time_down=1.5, factor=3)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   Lag3UD.ar/0:
                        source: SinOsc.ar/0[0]
                        lag_time_up: 0.25
                        lag_time_down: 1.5
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   Lag3UD.ar/1:
                        source: SinOsc.ar/1[0]
                        lag_time_up: 0.25
                        lag_time_down: 1.5

        """
        from . import Lag, Lag2, Lag2UD, Lag3, Lag3UD, LagUD

        if factor not in [1, 2, 3]:
            raise ValueError(factor)

        if lag_time_down is None:
            ugen: Type[UGen] = [Lag, Lag2, Lag3][factor - 1]
            return _compute_ugen_map(self, cast(Type[UGen], ugen), lag_time=lag_time_up)
        ugen = [LagUD, Lag2UD, Lag3UD][factor - 1]
        return _compute_ugen_map(
            self,
            cast(Type[UGen], ugen),
            lag_time_up=lag_time_up,
            lag_time_down=lag_time_down,
        )

    def lin_rand(self) -> "UGenOperable":
        """
        Compute a linearly-distributed random number between 0 and UGen graph.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.lin_rand()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(LINRAND).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(LINRAND).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self,
            special_index=UnaryOperator.LINRAND,
        )

    def lcm(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute the least common multiple of UGen graph and ``expr``.

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph.lcm(expr)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(LEAST_COMMON_MULTIPLE).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(LEAST_COMMON_MULTIPLE).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.LEAST_COMMON_MULTIPLE,
            float_operator=lambda a, b: math.lcm(a, b),
        )

    def log(self) -> "UGenOperable":
        """
        Compute the logarithm of UGen graph.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.log()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(LOG).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(LOG).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self, special_index=UnaryOperator.LOG, float_operator=math.log
        )

    def log2(self) -> "UGenOperable":
        """
        Compute the base 2 logarithm of UGen graph.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.log2()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(LOG2).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(LOG2).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self, special_index=UnaryOperator.LOG2, float_operator=math.log2
        )

    def log10(self) -> "UGenOperable":
        """
        Compute the base 10 logarithm of UGen graph.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.log10()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(LOG10).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(LOG10).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self, special_index=UnaryOperator.LOG10, float_operator=math.log10
        )

    def max(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute the maximum of UGen graph and ``expr``.

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph.max(expr)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(MAXIMUM).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(MAXIMUM).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.MAXIMUM,
            float_operator=lambda a, b: max((a, b)),
        )

    def midi_to_hz(self) -> "UGenOperable":
        """
        Convert UGen graph from MIDI note number to Hertz.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.midi_to_hz()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(MIDI_TO_HZ).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(MIDI_TO_HZ).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(source=self, special_index=UnaryOperator.MIDI_TO_HZ)

    def min(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute the minimum of UGen graph and ``expr``.

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph.min(expr)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(MINIMUM).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(MINIMUM).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.MINIMUM,
            float_operator=lambda a, b: min((a, b)),
        )

    def octave_to_hz(self) -> "UGenOperable":
        """
        Convert UGen graph from octave number to Hertz.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.octave_to_hz()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(OCTAVE_TO_HZ).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(OCTAVE_TO_HZ).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(source=self, special_index=UnaryOperator.OCTAVE_TO_HZ)

    def rand_range(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute a random number in the interval of UGen graph to ``expr``.

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph.rand_range(expr)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(RANDRANGE).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(RANDRANGE).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.RANDRANGE,
        )

    def rand(self) -> "UGenOperable":
        """
        Compute a random number between 0 and UGen graph, exclusive.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.rand()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(RAND).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(RAND).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self,
            special_index=UnaryOperator.RAND,
        )

    def ratio_to_semitones(self) -> "UGenOperable":
        """
        Converts UGen graph from frequency ratio to semitone distance.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.ratio_to_semitones()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(RATIO_TO_SEMITONES).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(RATIO_TO_SEMITONES).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self, special_index=UnaryOperator.RATIO_TO_SEMITONES
        )

    def rectangle_window(self) -> "UGenOperable":
        """
        Compute rectangle window from UGen graph.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.rectangle_window()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(RECTANGLE_WINDOW).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(RECTANGLE_WINDOW).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self, special_index=UnaryOperator.RECTANGLE_WINDOW
        )

    def reciprocal(self) -> "UGenOperable":
        """
        Compute the reciprocal of UGen graph.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.reciprocal()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(RECIPROCAL).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(RECIPROCAL).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self,
            special_index=UnaryOperator.RECIPROCAL,
            float_operator=lambda x: 1 / x,
        )

    def ring1(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute ring modulation of UGen graph and ``expr`` plus UGen graph.

        - (a * b) + a

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph.ring1(expr)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(RING1).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(RING1).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.RING1,
            float_operator=lambda a, b: ((a * b) + a),
        )

    def ring2(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute ring modulation of UGen graph and ``expr`` plus both sources.

        - (a * b) + a + b

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph.ring2(expr)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(RING2).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(RING2).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.RING2,
            float_operator=lambda a, b: (a * b) + a + b,
        )

    def ring3(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute ring modulation of UGen graph and ``expr`` multiplied by UGen graph.

        - a * b * a

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph.ring3(expr)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(RING3).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(RING3).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.RING3,
            float_operator=lambda a, b: a * a * b,
        )

    def ring4(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute ring modulation variant of UGen graph and ``expr``.

        - (a * a * b) - (a * b * b)

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph.ring4(expr)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(RING4).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(RING4).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.RING4,
            float_operator=lambda a, b: (a * a * b) - (a * b * b),
        )

    def round(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Round UGen graph by ``expr``.

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph.round(expr)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(ROUND).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(ROUND).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.ROUND,
        )

    def round_up(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Round UGen graph _up_ by ``expr``.

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph.round_up(expr)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(ROUND_UP).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(ROUND_UP).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.ROUND_UP,
        )

    def s_curve(self) -> "UGenOperable":
        """
        Compute the S-curve of UGen graph.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.s_curve()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(S_CURVE).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(S_CURVE).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(source=self, special_index=UnaryOperator.S_CURVE)

    def scale(
        self,
        input_minimum: "UGenRecursiveInput",
        input_maximum: "UGenRecursiveInput",
        output_minimum: "UGenRecursiveInput",
        output_maximum: "UGenRecursiveInput",
        exponential: bool = False,
    ) -> "UGenOperable":
        """
        Scale UGen graph.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.scale(-1.0, 1.0, 0.5, 0.75)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   MulAdd.ar/0:
                        source: SinOsc.ar/0[0]
                        multiplier: 0.125
                        addend: 0.625
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   MulAdd.ar/1:
                        source: SinOsc.ar/1[0]
                        multiplier: 0.125
                        addend: 0.625

        """
        from . import LinExp, LinLin

        return _compute_ugen_map(
            self,
            cast(Type[UGen], LinExp if exponential else LinLin),
            input_minimum=input_minimum,
            input_maximum=input_maximum,
            output_minimum=output_minimum,
            output_maximum=output_maximum,
        )

    def scale_negative(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Scale negative portion of UGen graph by ``expr``.

        - a * b when a < 0
        - otherwise a

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph.scale_negative(expr)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(SCALE_NEG).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(SCALE_NEG).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.SCALE_NEG,
        )

    def semitones_to_ratio(self) -> "UGenOperable":
        """
        Converts UGen graph from semitone distance to frequency ratio.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.semitones_to_ratio()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(SEMITONES_TO_RATIO).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(SEMITONES_TO_RATIO).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self, special_index=UnaryOperator.SEMITONES_TO_RATIO
        )

    def sign(self) -> "UGenOperable":
        """
        Compute the sign of UGen graph.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.sign()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(SIGN).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(SIGN).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(source=self, special_index=UnaryOperator.SIGN)

    def silence(self) -> "UGenOperable":
        """
        Silence (zero-out) UGen graph.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.silence()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(SILENCE).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(SILENCE).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self,
            special_index=UnaryOperator.SILENCE,
            float_operator=lambda x: 0.0,
        )

    def sin(self) -> "UGenOperable":
        """
        Compute the sine of UGen graph.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.sin()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(SIN).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(SIN).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self,
            special_index=UnaryOperator.SIN,
            float_operator=math.sin,
        )

    def sinh(self) -> "UGenOperable":
        """
        Compute the hyperbolic sine of UGen graph.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.sinh()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(SINH).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(SINH).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self,
            special_index=UnaryOperator.SINH,
            float_operator=math.sinh,
        )

    def softclip(self) -> "UGenOperable":
        """
        Compute non-linear distortion of UGen graph.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.softclip()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(SOFTCLIP).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(SOFTCLIP).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(source=self, special_index=UnaryOperator.SOFTCLIP)

    def sqrt(self) -> "UGenOperable":
        """
        Compute the square root of UGen graph.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.sqrt()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(SQUARE_ROOT).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(SQUARE_ROOT).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self,
            special_index=UnaryOperator.SQUARE_ROOT,
            float_operator=math.sqrt,
        )

    def squared(self) -> "UGenOperable":
        """
        Compute the square of UGen graph.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.squared()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(SQUARED).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(SQUARED).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self,
            special_index=UnaryOperator.SQUARED,
            float_operator=lambda x: x**2,
        )

    def square_of_difference(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute the square of difference between UGen graph and ``expr``.

        - (a - b) ** 2

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph.square_of_difference(expr)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(SQUARE_OF_DIFFERENCE).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(SQUARE_OF_DIFFERENCE).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.SQUARE_OF_DIFFERENCE,
            float_operator=lambda a, b: (a - b) ** 2,
        )

    def square_of_sum(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute square of sum of UGen graph and ``expr``.

        - (a + b) ** 2

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph.square_of_sum(expr)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(SQUARE_OF_SUM).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(SQUARE_OF_SUM).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.SQUARE_OF_SUM,
            float_operator=lambda a, b: (a + b) ** 2,
        )

    def sum3_rand(self) -> "UGenOperable":
        """
        Compute a random number in the interval of - UGen graph to + UGen graph, calculated by averaging three such numbers.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.sum3_rand()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(SUM3RAND).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(SUM3RAND).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self,
            special_index=UnaryOperator.SUM3RAND,
        )

    def sum_of_squares(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute sum of squares of UGen graph and ``expr``.

        - (a * a) + (b * b)

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph.sum_of_squares(expr)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(SUM_OF_SQUARES).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(SUM_OF_SQUARES).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.SUM_OF_SQUARES,
            float_operator=lambda a, b: (a * a) + (b * b),
        )

    def tan(self) -> "UGenOperable":
        """
        Compute the tangent of UGen graph.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.tan()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(TAN).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(TAN).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self,
            special_index=UnaryOperator.TAN,
            float_operator=math.tan,
        )

    def tanh(self) -> "UGenOperable":
        """
        Compute the hyperbolic tangent of UGen graph.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.tanh()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(TANH).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(TANH).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self,
            special_index=UnaryOperator.TANH,
            float_operator=math.tanh,
        )

    def through(self) -> "UGenOperable":
        """
        Pass through UGen graph.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.through()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(THRU).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(THRU).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self,
            special_index=UnaryOperator.THRU,
            float_operator=lambda x: x,
        )

    def transpose(self, semitones: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute transposition of UGen graph by ``expr`` in semitones.

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph.transpose(expr)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(HZ_TO_MIDI).ar/0:
                        source: SinOsc.ar/0[0]
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(ADDITION).ar/0:
                        left: UnaryOpUGen(HZ_TO_MIDI).ar/0[0]
                        right: WhiteNoise.kr[0]
                -   UnaryOpUGen(MIDI_TO_HZ).ar/0:
                        source: BinaryOpUGen(ADDITION).ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(HZ_TO_MIDI).ar/1:
                        source: SinOsc.ar/1[0]
                -   BinaryOpUGen(ADDITION).ar/1:
                        left: UnaryOpUGen(HZ_TO_MIDI).ar/1[0]
                        right: WhiteNoise.kr[0]
                -   UnaryOpUGen(MIDI_TO_HZ).ar/1:
                        source: BinaryOpUGen(ADDITION).ar/1[0]

        """
        return (self.hz_to_midi() + semitones).midi_to_hz()

    def triangle_window(self) -> "UGenOperable":
        """
        Compute triangle window from UGen graph.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.triangle_window()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(TRIANGLE_WINDOW).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(TRIANGLE_WINDOW).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(
            source=self, special_index=UnaryOperator.TRIANGLE_WINDOW
        )

    def truncate(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Truncate UGen graph by ``expr``.

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph.truncate(expr)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(TRUNCATION).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(TRUNCATION).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.TRUNCATION,
        )

    def unsigned_shift(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute unsigned right shift of UGen graph by ``expr``.

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph.unsigned_shift(expr)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(UNSIGNED_SHIFT).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(UNSIGNED_SHIFT).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.UNSIGNED_SHIFT,
        )

    def welch_window(self) -> "UGenOperable":
        """
        Compute Welch window from UGen graph.

        ::

            >>> from supriya.ugens import SinOsc
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> result = ugen_graph.welch_window()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(WELCH_WINDOW).ar/0:
                        source: SinOsc.ar/0[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   UnaryOpUGen(WELCH_WINDOW).ar/1:
                        source: SinOsc.ar/1[0]

        """
        return _compute_unary_op(source=self, special_index=UnaryOperator.WELCH_WINDOW)

    def wrap2(self, expr: "UGenRecursiveInput") -> "UGenOperable":
        """
        Compute bilateral wrapping of UGen graph by ``expr``.

        - wrap a to +/- b

        ::

            >>> from supriya.ugens import SinOsc, WhiteNoise
            >>> ugen_graph = SinOsc.ar(frequency=[440, 443])
            >>> expr = WhiteNoise.kr()
            >>> result = ugen_graph.wrap2(expr)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   WhiteNoise.kr: null
                -   BinaryOpUGen(WRAP2).ar/0:
                        left: SinOsc.ar/0[0]
                        right: WhiteNoise.kr[0]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(WRAP2).ar/1:
                        left: SinOsc.ar/1[0]
                        right: WhiteNoise.kr[0]

        """
        return _compute_binary_op(
            left=self,
            right=expr,
            special_index=BinaryOperator.WRAP2,
        )


class UGenScalar(UGenOperable):
    """
    A UGen scalar.
    """

    def __iter__(self) -> Iterator["UGenOperable"]:
        yield self


class OutputProxy(UGenScalar):
    """
    A UGen output proxy.

    Encodes a reference to a specific output of a UGen, as a scalar.
    """

    def __init__(self, ugen: "UGen", index: int) -> None:
        self.ugen = ugen
        self.index = index

    def __eq__(self, expr) -> bool:
        return (
            isinstance(expr, type(self))
            and self.ugen is expr.ugen
            and self.index == expr.index
        )

    def __hash__(self) -> int:
        return hash((type(self), self.ugen, self.index))

    def __repr__(self) -> str:
        return repr(self.ugen).replace(">", f"[{self.index}]>")

    def __str__(self) -> str:
        return str(self.ugen)

    @property
    def calculation_rate(self) -> CalculationRate:
        return self.ugen.calculation_rate


class ConstantProxy(UGenScalar):
    """
    A floating point constant proxy.

    Wraps a float and exposes all UGenOperable methods against it.
    """

    def __init__(self, value: SupportsFloat) -> None:
        self.value = float(value)

    def __eq__(self, expr) -> bool:
        if isinstance(expr, SupportsFloat):
            return float(self) == float(expr)
        return False

    def __float__(self) -> float:
        return self.value

    def __repr__(self) -> str:
        return f"<{self.value}>"

    def __str__(self) -> str:
        return str(self.value)


class UGenVector(UGenOperable, Sequence[UGenOperable]):
    """
    A sequence of UGenOperables.
    """

    def __init__(self, *values: SupportsFloat | UGenOperable) -> None:
        values_: list[UGen | UGenScalar | UGenVector] = []
        for x in values:
            if isinstance(x, (UGen, UGenScalar, UGenVector)):
                values_.append(x)
            elif isinstance(x, UGenSerializable):
                values_.append(UGenVector(*x.serialize()))
            elif isinstance(x, SupportsFloat):
                values_.append(ConstantProxy(float(x)))
            else:
                raise ValueError(x)
        self._values = tuple(values_)

    @overload
    def __getitem__(self, i: int) -> UGenOperable:
        pass

    @overload
    def __getitem__(self, i: slice) -> "UGenVector":
        pass

    def __getitem__(self, i):
        if isinstance(i, int):
            return self._values[i]
        return UGenVector(*self._values[i])

    def __iter__(self) -> Iterator["UGenOperable"]:
        yield from self._values

    def __len__(self) -> int:
        return len(self._values)

    def __repr__(self) -> str:
        return f"<{type(self).__name__}([{', '.join(repr(x) for x in self)}])>"

    def flatten(self) -> UGenOperable:
        """
        Flatten UGen vector.

        ::

            >>> from supriya.ugens import Pan2, SinOsc
            >>> vector = Pan2.ar(source=Pan2.ar(source=SinOsc.ar(frequency=[440, 443])))
            >>> supriya.graph(vector)  # doctest: +SKIP
            >>> print(repr(vector))
            <UGenVector([<UGenVector([<Pan2.ar()>, <Pan2.ar()>])>, <UGenVector([<Pan2.ar()>, <Pan2.ar()>])>])>

        ::

            >>> result = vector.flatten()
            >>> print(repr(result))
            <UGenVector([<Pan2.ar()[0]>, <Pan2.ar()[1]>, <Pan2.ar()[0]>, <Pan2.ar()[1]>, <Pan2.ar()[0]>, <Pan2.ar()[1]>, <Pan2.ar()[0]>, <Pan2.ar()[1]>])>

        """
        if len(vector := UGenVector(*flatten(self, terminal_types=UGenScalar))) == 1:
            return vector[0]
        return vector

    def mix(self, channel_count: int = 1) -> UGenOperable:
        """
        Mix UGen vector down to ``channel_count`` outputs.

        ::

            >>> from supriya.ugens import Pan2, SinOsc
            >>> vector = Pan2.ar(source=Pan2.ar(source=SinOsc.ar(frequency=[440, 443])))
            >>> supriya.graph(vector)  # doctest: +SKIP
            >>> print(vector)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   Pan2.ar/0:
                        source: SinOsc.ar/0[0]
                        position: 0.0
                        level: 1.0
                -   Pan2.ar/1:
                        source: Pan2.ar/0[0]
                        position: 0.0
                        level: 1.0
                -   Pan2.ar/2:
                        source: Pan2.ar/0[1]
                        position: 0.0
                        level: 1.0
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   Pan2.ar/3:
                        source: SinOsc.ar/1[0]
                        position: 0.0
                        level: 1.0
                -   Pan2.ar/4:
                        source: Pan2.ar/3[0]
                        position: 0.0
                        level: 1.0
                -   Pan2.ar/5:
                        source: Pan2.ar/3[1]
                        position: 0.0
                        level: 1.0

        ::

            >>> result = vector.mix(2)
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   Pan2.ar/0:
                        source: SinOsc.ar/0[0]
                        position: 0.0
                        level: 1.0
                -   Pan2.ar/1:
                        source: Pan2.ar/0[0]
                        position: 0.0
                        level: 1.0
                -   Pan2.ar/2:
                        source: Pan2.ar/0[1]
                        position: 0.0
                        level: 1.0
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   Pan2.ar/3:
                        source: SinOsc.ar/1[0]
                        position: 0.0
                        level: 1.0
                -   Pan2.ar/4:
                        source: Pan2.ar/3[0]
                        position: 0.0
                        level: 1.0
                -   Pan2.ar/5:
                        source: Pan2.ar/3[1]
                        position: 0.0
                        level: 1.0
                -   Sum4.ar/0:
                        input_one: Pan2.ar/1[0]
                        input_two: Pan2.ar/2[0]
                        input_three: Pan2.ar/4[0]
                        input_four: Pan2.ar/5[0]
                -   Sum4.ar/1:
                        input_one: Pan2.ar/1[1]
                        input_two: Pan2.ar/2[1]
                        input_three: Pan2.ar/4[1]
                        input_four: Pan2.ar/5[1]

        """
        from . import Mix

        return Mix.multichannel(self, channel_count=channel_count)

    def sum(self) -> UGenOperable:
        """
        Sum UGen vector down to a single output.

        ::

            >>> from supriya.ugens import Pan2, SinOsc
            >>> vector = Pan2.ar(source=Pan2.ar(source=SinOsc.ar(frequency=[440, 443])))
            >>> supriya.graph(vector)  # doctest: +SKIP
            >>> print(vector)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   Pan2.ar/0:
                        source: SinOsc.ar/0[0]
                        position: 0.0
                        level: 1.0
                -   Pan2.ar/1:
                        source: Pan2.ar/0[0]
                        position: 0.0
                        level: 1.0
                -   Pan2.ar/2:
                        source: Pan2.ar/0[1]
                        position: 0.0
                        level: 1.0
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   Pan2.ar/3:
                        source: SinOsc.ar/1[0]
                        position: 0.0
                        level: 1.0
                -   Pan2.ar/4:
                        source: Pan2.ar/3[0]
                        position: 0.0
                        level: 1.0
                -   Pan2.ar/5:
                        source: Pan2.ar/3[1]
                        position: 0.0
                        level: 1.0

        ::

            >>> result = vector.sum()
            >>> supriya.graph(result)  # doctest: +SKIP
            >>> print(result)
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   Pan2.ar/0:
                        source: SinOsc.ar/0[0]
                        position: 0.0
                        level: 1.0
                -   Pan2.ar/1:
                        source: Pan2.ar/0[0]
                        position: 0.0
                        level: 1.0
                -   Pan2.ar/2:
                        source: Pan2.ar/0[1]
                        position: 0.0
                        level: 1.0
                -   Sum4.ar/0:
                        input_one: Pan2.ar/1[0]
                        input_two: Pan2.ar/1[1]
                        input_three: Pan2.ar/2[0]
                        input_four: Pan2.ar/2[1]
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   Pan2.ar/3:
                        source: SinOsc.ar/1[0]
                        position: 0.0
                        level: 1.0
                -   Pan2.ar/4:
                        source: Pan2.ar/3[0]
                        position: 0.0
                        level: 1.0
                -   Pan2.ar/5:
                        source: Pan2.ar/3[1]
                        position: 0.0
                        level: 1.0
                -   Sum4.ar/1:
                        input_one: Pan2.ar/4[0]
                        input_two: Pan2.ar/4[1]
                        input_three: Pan2.ar/5[0]
                        input_four: Pan2.ar/5[1]
                -   BinaryOpUGen(ADDITION).ar:
                        left: Sum4.ar/0[0]
                        right: Sum4.ar/1[0]

        """
        from . import Mix

        return Mix.new(self)


@runtime_checkable
class UGenSerializable(Protocol):
    """
    Protocol for classes serializable as UGenVectors.
    """

    def serialize(self, **kwargs) -> UGenVector:
        raise NotImplementedError


class UGen(UGenOperable, Sequence):
    """
    A UGen: a "unit generator".
    """

    _channel_count = 1
    _has_done_flag = False
    _has_settable_channel_count = False
    _is_input = False
    _is_output = False
    _is_pure = False
    _is_width_first = False
    _ordered_keys: tuple[str, ...] = ()
    _signal_range: SignalRange = SignalRange.BIPOLAR
    _unexpanded_keys: frozenset[str] = frozenset()
    _valid_calculation_rates: tuple[CalculationRate, ...] = ()

    def __init__(
        self,
        *,
        calculation_rate: CalculationRate = CalculationRate.SCALAR,
        special_index: SupportsInt = 0,
        **kwargs: Union["UGenScalarInput", "UGenVectorInput"],
    ) -> None:
        if (
            self._valid_calculation_rates
            and calculation_rate not in self._valid_calculation_rates
        ):
            raise ValueError(
                f"{calculation_rate} not in {self._valid_calculation_rates}"
            )
        calculation_rate, kwargs = self._postprocess_kwargs(
            calculation_rate=calculation_rate, **kwargs
        )
        self._calculation_rate = calculation_rate
        self._special_index = int(special_index)
        input_keys: list[str | tuple[str, int]] = []
        inputs: list[OutputProxy | float] = []
        for key in self._ordered_keys:
            if (value := kwargs.pop(key)) is None:
                raise ValueError(key)
            if isinstance(value, UGenSerializable):
                serialized = value.serialize()
                if any(isinstance(x, UGenVector) for x in serialized):
                    raise ValueError(key, serialized)
                value = cast(Sequence[SupportsFloat | UGenScalar], serialized)
            if isinstance(value, Sequence):
                if key not in self._unexpanded_keys:
                    raise ValueError(key, value)
                iterator: Iterable[tuple[int | None, SupportsFloat | UGenScalar]] = (
                    (i, v) for i, v in enumerate(value)
                )
            else:
                iterator = ((None, v) for v in [value])
            i: int | None
            for i, x in iterator:
                if isinstance(x, SupportsFloat):
                    inputs.append(float(x))
                elif isinstance(x, ConstantProxy):
                    inputs.append(float(x.value))
                elif isinstance(x, OutputProxy):
                    inputs.append(x)
                else:
                    raise ValueError(key, x)
                input_keys.append((key, i) if i is not None else key)
        if kwargs:
            raise ValueError(type(self).__name__, kwargs)
        self._inputs = tuple(inputs)
        self._input_keys = tuple(input_keys)
        self._uuid: uuid.UUID | None = None
        if SynthDefBuilder._active_builders:
            builder = SynthDefBuilder._active_builders[-1]
            self._uuid = builder._uuid
            builder._add_ugen(self)
        for input_ in self._inputs:
            if isinstance(input_, OutputProxy) and input_.ugen._uuid != self._uuid:
                raise SynthDefError("UGen input in different scope")
        self._values = tuple(
            OutputProxy(ugen=self, index=i)
            for i in range(getattr(self, "_channel_count", 1))
        )

    @overload
    def __getitem__(self, i: int) -> OutputProxy:
        pass

    @overload
    def __getitem__(self, i: slice) -> UGenVector:
        pass

    def __getitem__(self, i):
        if isinstance(i, int):
            return self._values[i]
        return UGenVector(*self._values[i])

    def __iter__(self) -> Iterator["UGenOperable"]:
        yield from self._values

    def __len__(self) -> int:
        return self._channel_count

    def __repr__(self):
        return f"<{type(self).__name__}.{self.calculation_rate.token}()>"

    def _eliminate(
        self, sort_bundles: dict["UGen", "SynthDefBuilder.SortBundle"]
    ) -> None:
        if not (sort_bundle := sort_bundles.get(self)) or sort_bundle.descendants:
            return
        del sort_bundles[self]
        for antecedent in tuple(sort_bundle.antecedents):
            if not (antecedent_bundle := sort_bundles.get(antecedent)):
                continue
            antecedent_bundle.descendants.remove(self)
            antecedent._optimize(sort_bundles)

    @classmethod
    def _expand_params(
        cls,
        params: dict[str, "UGenRecursiveInput"],
        unexpanded_keys: Iterable[str] | None = None,
    ) -> "UGenRecursiveParams":
        unexpanded_keys_ = set(unexpanded_keys or ())
        size = 0
        for key, value in params.items():
            if isinstance(value, UGenSerializable):
                params[key] = value = value.serialize()
            # Scalars
            if isinstance(value, (SupportsFloat, UGenScalar)):
                continue
            elif isinstance(value, Sequence):
                # Unexpanded, but need to reach bottom layer
                if key in unexpanded_keys_:
                    if isinstance(value, Sequence) and any(
                        (
                            isinstance(x, Sequence)
                            and not isinstance(x, (SupportsFloat, UGenScalar))
                        )
                        for x in value
                    ):
                        size = max(size, len(value))
                    else:
                        # Reached the bottom layer
                        continue
                # Expanded
                else:
                    size = max(size, len(value))
        if not size:
            return cast(dict[str, UGenScalarInput | UGenVectorInput], params)
        results = []
        for i in range(size):
            new_params: dict[str, UGenRecursiveInput] = {}
            for key, value in params.items():
                # Redundant but satiates MyPy
                if isinstance(value, UGenSerializable):
                    value = value.serialize()
                if isinstance(value, (SupportsFloat, UGenScalar)):
                    new_params[key] = value
                elif isinstance(value, Sequence):
                    if key in unexpanded_keys_:
                        if isinstance(value, Sequence) and all(
                            isinstance(x, (SupportsFloat, UGenScalar)) for x in value
                        ):
                            new_params[key] = value
                        else:
                            new_params[key] = value[i % len(value)]
                    else:
                        new_params[key] = value[i % len(value)]
            results.append(
                cls._expand_params(new_params, unexpanded_keys=unexpanded_keys)
            )
        return results

    @classmethod
    def _new_expanded(
        cls,
        *,
        calculation_rate: CalculationRateLike,
        special_index: int = 0,
        **kwargs: "UGenRecursiveInput",
    ) -> UGenOperable:
        """
        (
            var a, b, c, d;
            a = SinOsc.ar([1, 2, 3]);
            b = Pan2.ar(a);
            c = Pan2.ar(b);
            d = (Pan2.ar(c) * 2);
            a.postln;
            b.postln;
            c.postln;
            d.postln;
        )
        [ a SinOsc, a SinOsc, a SinOsc ]
        [ [ an OutputProxy, an OutputProxy ], [ an OutputProxy, an OutputProxy ], [ an OutputProxy, an OutputProxy ] ]
        [ [ [ an OutputProxy, an OutputProxy ], [ an OutputProxy, an OutputProxy ] ], [ [ an OutputProxy, an OutputProxy ], [ an OutputProxy, an OutputProxy ] ], [ [ an OutputProxy, an OutputProxy ], [ an OutputProxy, an OutputProxy ] ] ]
        [ [ [ [ a BinaryOpUGen, a BinaryOpUGen ], [ a BinaryOpUGen, a BinaryOpUGen ] ], [ [ a BinaryOpUGen, a BinaryOpUGen ], [ a BinaryOpUGen, a BinaryOpUGen ] ] ], [ [ [ a BinaryOpUGen, a BinaryOpUGen ], [ a BinaryOpUGen, a BinaryOpUGen ] ], [ [ a BinaryOpUGen, a BinaryOpUGen ], [ a BinaryOpUGen, a BinaryOpUGen ] ] ], [ [ [ a BinaryOpUGen, a BinaryOpUGen ], [ a BinaryOpUGen, a BinaryOpUGen ] ], [ [ a BinaryOpUGen, a BinaryOpUGen ], [ a BinaryOpUGen, a BinaryOpUGen ] ] ] ]
        """

        def recurse(
            all_expanded_params: UGenRecursiveParams,
        ) -> UGenOperable:
            if (
                not isinstance(all_expanded_params, dict)
                and len(all_expanded_params) == 1
            ):
                all_expanded_params = all_expanded_params[0]
            if isinstance(all_expanded_params, dict):
                return cls._new_single(
                    calculation_rate=calculation_rate,
                    special_index=special_index,
                    **all_expanded_params,
                )
            return UGenVector(
                *(recurse(expanded_params) for expanded_params in all_expanded_params)
            )

        return recurse(cls._expand_params(kwargs, unexpanded_keys=cls._unexpanded_keys))

    @classmethod
    def _new_single(
        cls,
        *,
        calculation_rate: CalculationRateLike = None,
        special_index: SupportsInt = 0,
        **kwargs: Union["UGenScalarInput", "UGenVectorInput"],
    ) -> UGenOperable:
        if (
            len(
                ugen := cls(
                    calculation_rate=CalculationRate.from_expr(calculation_rate),
                    special_index=special_index,
                    **kwargs,
                )
            )
            == 1
        ):
            return ugen[0]
        return ugen

    def _optimize(
        self, sort_bundles: dict["UGen", "SynthDefBuilder.SortBundle"]
    ) -> None:
        if not self._is_pure:
            return
        self._eliminate(sort_bundles)

    def _postprocess_kwargs(
        self,
        *,
        calculation_rate: CalculationRate,
        **kwargs: Union["UGenScalarInput", "UGenVectorInput"],
    ) -> tuple[CalculationRate, dict[str, Union["UGenScalarInput", "UGenVectorInput"]]]:
        return calculation_rate, kwargs

    @property
    def calculation_rate(self) -> CalculationRate:
        return self._calculation_rate

    @property
    def has_done_flag(self) -> bool:
        return self._has_done_flag

    @property
    def inputs(self) -> tuple[OutputProxy | float, ...]:
        return tuple(self._inputs)

    @property
    def is_input_ugen(self) -> bool:
        return self._is_input

    @property
    def is_output_ugen(self) -> bool:
        return self._is_output

    @property
    def signal_range(self) -> SignalRange:
        return self._signal_range

    @property
    def special_index(self) -> int:
        return self._special_index


UGenScalarInput: TypeAlias = SupportsFloat | UGenScalar
UGenVectorInput: TypeAlias = UGenSerializable | Sequence[UGenScalarInput]

UGenRecursiveInput: TypeAlias = (
    SupportsFloat | UGenOperable | UGenSerializable | Sequence["UGenRecursiveInput"]
)

UGenParams: TypeAlias = dict[str, UGenScalarInput | UGenVectorInput]
UGenRecursiveParams: TypeAlias = UGenParams | list["UGenRecursiveParams"]


@ugen(is_pure=True)
class UnaryOpUGen(UGen):
    source = param()

    def __init__(
        self,
        *,
        calculation_rate: CalculationRate,
        source: UGenScalarInput,
        special_index: SupportsInt = 0,
    ) -> None:
        super().__init__(
            calculation_rate=calculation_rate,
            source=source,
            special_index=special_index,
        )

    def __repr__(self) -> str:
        return f"<{type(self).__name__}.{self.calculation_rate.token}({self.operator.name})>"

    @property
    def operator(self) -> UnaryOperator:
        return UnaryOperator(self.special_index)


@ugen(is_pure=True)
class BinaryOpUGen(UGen):
    left = param()
    right = param()

    def __init__(
        self,
        *,
        calculation_rate: CalculationRate,
        left: UGenScalarInput,
        right: UGenScalarInput,
        special_index: SupportsInt = 0,
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
        cls,
        *,
        calculation_rate: CalculationRateLike = None,
        special_index: SupportsInt = 0,
        **kwargs: UGenScalarInput | UGenVectorInput,
    ) -> UGenOperable:
        def process(
            left: UGenScalar | float,
            right: UGenScalar | float,
        ) -> UGenOperable | float:
            if special_index == BinaryOperator.MULTIPLICATION:
                if left == 0 or right == 0:
                    return ConstantProxy(0)
                if left == 1:
                    return right
                if left == -1:
                    return -right
                if right == 1:
                    return left
                if right == -1:
                    return -left
            if special_index == BinaryOperator.ADDITION:
                if left == 0:
                    return right
                if right == 0:
                    return left
            if special_index == BinaryOperator.SUBTRACTION:
                if left == 0:
                    return -right
                if right == 0:
                    return left
            if special_index == BinaryOperator.FLOAT_DIVISION:
                if right == 1:
                    return left
                if right == -1:
                    return -left
            return cls(
                calculation_rate=max(
                    [
                        CalculationRate.from_expr(left),
                        CalculationRate.from_expr(right),
                    ]
                ),
                special_index=special_index,
                left=left,
                right=right,
            )[0]

        left = kwargs["left"]
        right = kwargs["right"]
        if not isinstance(left, (SupportsFloat, UGenScalar)):
            raise ValueError(left)
        if not isinstance(right, (SupportsFloat, UGenScalar)):
            raise ValueError(right)
        if isinstance(
            result := process(
                float(left) if isinstance(left, SupportsFloat) else left,
                float(right) if isinstance(right, SupportsFloat) else right,
            ),
            SupportsFloat,
        ):
            return ConstantProxy(result)
        return result

    @property
    def operator(self) -> BinaryOperator:
        return BinaryOperator(self.special_index)


class PseudoUGen:
    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError


class Parameter(UGen):
    def __init__(
        self,
        *,
        name: str | None = None,
        value: float | Sequence[float],
        rate: ParameterRateLike = ParameterRate.CONTROL,
        lag: float | None = None,
    ) -> None:
        if isinstance(value, SupportsFloat):
            self.value: tuple[float, ...] = (float(value),)
        else:
            self.value = tuple(float(x) for x in value)
        self.name = name
        self.lag = lag
        self.rate = ParameterRate.from_expr(rate)
        self._channel_count = len(self.value)
        super().__init__(calculation_rate=CalculationRate.from_expr(self.rate))

    def __eq__(self, other) -> bool:
        return (type(self), self.name, self.value, self.rate, self.lag) == (
            type(other),
            other.name,
            other.value,
            other.rate,
            other.lag,
        )

    def __hash__(self) -> int:
        return hash((type(self), self.name, self.value, self.rate, self.lag))

    def __repr__(self) -> str:
        return f"<{type(self).__name__}.{self.calculation_rate.token}({self.name})>"


class Control(UGen):
    def __init__(
        self,
        *,
        parameters: Sequence[Parameter],
        calculation_rate: CalculationRate,
        special_index: int = 0,
    ) -> None:
        self._parameters = tuple(parameters)
        self._channel_count = sum(len(parameter) for parameter in self._parameters)
        super().__init__(
            calculation_rate=calculation_rate,
            special_index=special_index,
        )

    @property
    def parameters(self) -> Sequence[Parameter]:
        return self._parameters


class AudioControl(Control):
    pass


class LagControl(Control):
    _ordered_keys = ("lags",)
    _unexpanded_keys = frozenset(["lags"])

    def __init__(
        self,
        *,
        parameters: Sequence[Parameter],
        calculation_rate: CalculationRate,
        special_index: int = 0,
    ) -> None:
        self._parameters = tuple(parameters)
        self._channel_count = sum(len(parameter) for parameter in self._parameters)
        lags = []
        for parameter in parameters:
            lags.extend([parameter.lag or 0.0] * len(parameter))
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            lags=lags,
            special_index=special_index,
        )


class TrigControl(Control):
    pass


class SynthDefError(Exception):
    pass


class SynthDef:
    def __init__(self, ugens: Sequence[UGen], name: str | None = None) -> None:
        if not ugens:
            raise SynthDefError("No UGens provided")
        self._ugens = tuple(ugens)
        self._name = name
        constants: list[float] = []
        for ugen in ugens:
            for input_ in ugen.inputs:
                if isinstance(input_, float) and input_ not in constants:
                    constants.append(input_)
        self._constants = tuple(constants)
        self._controls: tuple[Control, ...] = tuple(
            ugen for ugen in ugens if isinstance(ugen, Control)
        )
        self._parameters: dict[str, tuple[Parameter, int]] = (
            self._collect_indexed_parameters(self._controls)
        )
        self._compiled_graph = _compile_ugen_graph(self)

    def __graph__(self) -> Graph:
        r"""
        Graph a SynthDef.

        ::

            >>> from supriya.ugens import Out, SinOsc, SynthDefBuilder
            >>> with SynthDefBuilder(amplitude=1.0, bus=0, frequency=[440, 443]) as builder:
            ...     source = SinOsc.ar(frequency=builder["frequency"])
            ...     out = Out.ar(bus=builder["bus"], source=source * builder["amplitude"])
            ...

        ::

            >>> synthdef = builder.build()

        ::

            >>> graph = synthdef.__graph__()
            >>> print(format(graph, "graphviz"))
            digraph synthdef_4e5d18af62c02b10252a62def13fb402 {
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
                    label="<f_0> Control\n(control) | { { <f_1_0_0> amplitude:\n1.0 | <f_1_0_1> bus:\n0.0 | <f_1_0_2> frequency[0]:\n440.0 | <f_1_0_3> frequency[1]:\n443.0 } }"];
                ugen_1 [fillcolor=lightsteelblue2,
                    label="<f_0> SinOsc\n(audio) | { { <f_1_0_0> frequency | <f_1_0_1> phase:\n0.0 } | { <f_1_1_0> 0 } }"];
                ugen_2 [fillcolor=lightsteelblue2,
                    label="<f_0> BinaryOpUGen\n[MULTIPLICATION]\n(audio) | { { <f_1_0_0> left | <f_1_0_1> right } | { <f_1_1_0> 0 } }"];
                ugen_3 [fillcolor=lightsteelblue2,
                    label="<f_0> SinOsc\n(audio) | { { <f_1_0_0> frequency | <f_1_0_1> phase:\n0.0 } | { <f_1_1_0> 0 } }"];
                ugen_4 [fillcolor=lightsteelblue2,
                    label="<f_0> BinaryOpUGen\n[MULTIPLICATION]\n(audio) | { { <f_1_0_0> left | <f_1_0_1> right } | { <f_1_1_0> 0 } }"];
                ugen_5 [fillcolor=lightsteelblue2,
                    label="<f_0> Out\n(audio) | { { <f_1_0_0> bus | <f_1_0_1> source[0] | <f_1_0_2> source[1] } }"];
                ugen_0:f_1_0_0:e -> ugen_2:f_1_0_1:w [color=goldenrod];
                ugen_0:f_1_0_0:e -> ugen_4:f_1_0_1:w [color=goldenrod];
                ugen_0:f_1_0_1:e -> ugen_5:f_1_0_0:w [color=goldenrod];
                ugen_0:f_1_0_2:e -> ugen_1:f_1_0_0:w [color=goldenrod];
                ugen_0:f_1_0_3:e -> ugen_3:f_1_0_0:w [color=goldenrod];
                ugen_1:f_1_1_0:e -> ugen_2:f_1_0_0:w [color=steelblue];
                ugen_2:f_1_1_0:e -> ugen_5:f_1_0_1:w [color=steelblue];
                ugen_3:f_1_1_0:e -> ugen_4:f_1_0_0:w [color=steelblue];
                ugen_4:f_1_1_0:e -> ugen_5:f_1_0_2:w [color=steelblue];
            }

        """

        def connect_nodes(ugen_node_mapping: dict[UGen, Node]) -> None:
            for ugen, tail_node in ugen_node_mapping.items():
                # Don't graph synthetic inputs (e.g. MaxLocalBufs -> LocalBuf)
                # because these inputs don't actually exist.
                # Use the shortest length of input keys vs inputs.
                for i, (_, input_) in enumerate(zip(ugen._input_keys, ugen._inputs)):
                    if not isinstance(input_, OutputProxy):
                        continue
                    tail_field = tail_node["inputs"][i]
                    head_node = ugen_node_mapping[input_.ugen]
                    head_field = head_node["outputs"][input_.index]
                    edge = Edge(head_port_position="w", tail_port_position="e")
                    edge.attach(head_field, tail_field)
                    if input_.calculation_rate == CalculationRate.CONTROL:
                        edge.attributes["color"] = "goldenrod"
                    elif input_.calculation_rate == CalculationRate.AUDIO:
                        edge.attributes["color"] = "steelblue"
                    else:
                        edge.attributes["color"] = "salmon"

        def create_ugen_input_group(ugen: UGen, ugen_index: int) -> RecordGroup | None:
            if not ugen.inputs:
                return None
            input_group = RecordGroup(name="inputs")
            for i, (input_key, input_) in enumerate(
                zip_longest(ugen._input_keys, ugen._inputs)
            ):
                if input_ is None:
                    raise ValueError
                elif input_key is None:
                    continue
                if isinstance(input_key, str):
                    input_name = input_key
                elif isinstance(input_key, tuple):
                    input_name = f"{input_key[0]}[{input_key[1]}]"
                if isinstance(input_, float):
                    label = f"{input_name}:\\n{input_}"
                else:
                    label = input_name
                input_group.append(
                    RecordField(label=label, name=f"ugen_{ugen_index}_input_{i}")
                )
            return input_group

        def create_ugen_node_mapping() -> dict[UGen, Node]:
            mapping = {}
            for i, ugen in enumerate(self.ugens):
                node = Node(name=f"ugen_{i}")
                if ugen.calculation_rate == CalculationRate.CONTROL:
                    node.attributes["fillcolor"] = "lightgoldenrod2"
                elif ugen.calculation_rate == CalculationRate.AUDIO:
                    node.attributes["fillcolor"] = "lightsteelblue2"
                else:
                    node.attributes["fillcolor"] = "lightsalmon2"
                node.append(create_ugen_title_field(ugen))
                group = RecordGroup()
                if (input_group := create_ugen_input_group(ugen, i)) is not None:
                    group.append(input_group)
                if (output_group := create_ugen_output_group(ugen, i)) is not None:
                    group.append(output_group)
                node.append(group)
                mapping[ugen] = node
            return mapping

        def create_ugen_output_group(ugen: UGen, ugen_index: int) -> RecordGroup | None:
            if not len(ugen):
                return None
            output_group = RecordGroup(name="outputs")
            if isinstance(ugen, Control):
                i = 0
                for parameter in ugen.parameters:
                    for j, value in enumerate(parameter.value):
                        if len(parameter.value) == 1:
                            label = f"{parameter.name}:\\n{value}"
                        else:
                            label = f"{parameter.name}[{j}]:\\n{value}"
                        output_group.append(
                            RecordField(
                                label=label, name=f"ugen_{ugen_index}_output_{i}"
                            )
                        )
                        i += 1
            else:
                for i, output in enumerate(ugen):
                    output_group.append(
                        RecordField(label=str(i), name=f"ugen_{ugen_index}_output_{i}")
                    )
            return output_group

        def create_ugen_title_field(ugen: UGen) -> RecordField:
            name = type(ugen).__name__
            calculation_rate = ugen.calculation_rate.name.lower()
            if isinstance(ugen, BinaryOpUGen):
                label = f"{name}\\n[{BinaryOperator(ugen.special_index).name}]\\n({calculation_rate})"
            elif isinstance(ugen, UnaryOpUGen):
                label = f"{name}\\n[{UnaryOperator(ugen.special_index).name}]\\n({calculation_rate})"
            else:
                label = f"{name}\\n({calculation_rate})"
            return RecordField(label=label)

        def style_graph(graph: Graph) -> None:
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

        graph = Graph(name=f"synthdef_{self.effective_name}")
        for node in (ugen_node_mapping := create_ugen_node_mapping()).values():
            graph.append(node)
        connect_nodes(ugen_node_mapping)
        style_graph(graph)
        return graph

    def __hash__(self) -> int:
        return hash((type(self), self._name, self._compiled_graph))

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return (self._name, self._compiled_graph) == (
            other._name,
            other._compiled_graph,
        )

    def __repr__(self) -> str:
        return "<{}: {}>".format(type(self).__name__, self.effective_name)

    def __str__(self) -> str:
        result = [
            "synthdef:",
            f"    name: {self.effective_name}",
            "    ugens:",
        ]
        grouped_ugens: dict[tuple[Type[UGen], CalculationRate, int], list[UGen]] = {}
        for ugen in self.ugens:
            key = (type(ugen), ugen.calculation_rate, ugen.special_index)
            grouped_ugens.setdefault(key, []).append(ugen)
        ugen_names: dict[UGen, str] = {}
        for ugen in self.ugens:
            name = type(ugen).__name__
            if isinstance(ugen, BinaryOpUGen):
                name += f"({BinaryOperator.from_expr(ugen.special_index).name})"
            elif isinstance(ugen, UnaryOpUGen):
                name += f"({UnaryOperator.from_expr(ugen.special_index).name})"
            name += f".{ugen.calculation_rate.token}"
            key = (type(ugen), ugen.calculation_rate, ugen.special_index)
            if len(related_ugens := grouped_ugens[key]) > 1:
                name += f"/{related_ugens.index(ugen)}"
            ugen_names[ugen] = name
        for ugen in self.ugens:
            inputs: dict[str, str] = {}
            if "channel_count" in inspect.signature(type(ugen)).parameters:
                inputs["channel_count"] = str(len(ugen))
            if isinstance(ugen, Control):
                for parameter in ugen.parameters:
                    if parameter.name is None:
                        raise ValueError(parameter)
                    if len(parameter.value) == 1:
                        inputs[parameter.name] = str(parameter.value[0])
                    else:
                        for i, value in enumerate(parameter.value):
                            inputs[f"{parameter.name}[{i}]"] = str(value)
            # Don't graph synthetic inputs (e.g. MaxLocalBufs -> LocalBuf)
            # because these inputs don't actually exist.
            # Use the shortest length of input keys vs inputs.
            for input_key, input_ in zip(ugen._input_keys, ugen._inputs):
                if isinstance(input_key, str):
                    input_name = input_key
                    if input_key in ugen._unexpanded_keys:
                        input_name += "[0]"
                elif isinstance(input_key, tuple):
                    input_name = f"{input_key[0]}[{input_key[1]}]"
                else:
                    raise ValueError(input_key)
                if isinstance(input_, float):
                    input_value = str(input_)
                else:
                    input_value = ugen_names[input_.ugen]
                    input_value += "["
                    input_value += str(input_.index)
                    if isinstance(input_.ugen, Control):
                        value_index = 0
                        for parameter in input_.ugen.parameters:
                            if input_.index < value_index + len(parameter):
                                break
                            else:
                                value_index += len(parameter)
                        input_value += f":{parameter.name}"
                        if len(parameter) > 1:
                            input_value += f"[{input_.index - value_index}]"
                    input_value += "]"
                inputs[input_name] = input_value
            if inputs:
                result.append(f"    -   {ugen_names[ugen]}:")
                for input_name, input_value in inputs.items():
                    result.append(f"            {input_name}: {input_value}")
            else:
                result.append(f"    -   {ugen_names[ugen]}: null")
        return "\n".join(result)

    def _collect_indexed_parameters(
        self, controls: Sequence[Control]
    ) -> dict[str, tuple[Parameter, int]]:
        mapping: dict[str, tuple[Parameter, int]] = {}
        for control in controls:
            index = control.special_index
            for parameter in control.parameters:
                if parameter.name is None:
                    raise ValueError(parameter)
                mapping[parameter.name] = (parameter, index)
                index += len(parameter)
        return mapping

    def compile(self, use_anonymous_name: bool = False) -> bytes:
        return compile_synthdefs(self, use_anonymous_names=use_anonymous_name)

    @property
    def anonymous_name(self) -> str:
        return hashlib.md5(self._compiled_graph).hexdigest()

    @property
    def constants(self) -> Sequence[float]:
        return self._constants

    @property
    def controls(self) -> Sequence[Control]:
        return self._controls

    @property
    def effective_name(self) -> str:
        return self.name or self.anonymous_name

    @property
    def has_gate(self) -> bool:
        return "gate" in self.parameters

    @property
    def indexed_parameters(self) -> Sequence[tuple[int, Parameter]]:
        return sorted((value[1], value[0]) for value in self.parameters.values())

    @property
    def name(self) -> str | None:
        return self._name

    @property
    def parameters(self) -> Mapping[str, tuple[Parameter, int]]:
        return MappingProxyType(self._parameters)

    @property
    def ugens(self) -> Sequence[UGen]:
        return self._ugens


# TODO: Convert to ContextVar instead
_local = threading.local()
_local._active_builders = []


class SynthDefBuilder:
    class SortBundle(NamedTuple):
        ugen: UGen
        width_first_antecedents: tuple[UGen, ...]
        antecedents: list[UGen]
        descendants: list[UGen]

    _active_builders: list["SynthDefBuilder"] = _local._active_builders

    def __init__(self, **kwargs: Parameter | Sequence[float] | float) -> None:
        self._building = False
        self._parameters: dict[str, Parameter] = {}
        self._ugens: list[UGen] = []
        self._uuid = uuid.uuid4()
        for key, value in kwargs.items():
            if isinstance(value, Parameter):
                self.add_parameter(
                    lag=value.lag, name=key, value=value.value, rate=value.rate
                )
            else:
                self.add_parameter(name=key, value=value)

    def __enter__(self) -> "SynthDefBuilder":
        self._active_builders.append(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._active_builders.pop()

    def __getitem__(self, item: str) -> OutputProxy | Parameter:
        parameter = self._parameters[item]
        if len(parameter) == 1:
            return parameter[0]
        return parameter

    def _add_ugen(self, ugen: UGen):
        if ugen._uuid != self._uuid:
            raise SynthDefError("UGen input in different scope")
        if not self._building:
            self._ugens.append(ugen)

    def _build_control_mapping(
        self, parameters: Sequence[Parameter]
    ) -> tuple[
        list[Control],
        dict[OutputProxy, OutputProxy],
    ]:
        parameter_mapping: dict[ParameterRate, list[Parameter]] = {}
        for parameter in parameters:
            parameter_mapping.setdefault(parameter.rate, []).append(parameter)
        for filtered_parameters in parameter_mapping.values():
            filtered_parameters.sort(key=lambda x: x.name or "")
        controls: list[Control] = []
        control_mapping: dict[OutputProxy, OutputProxy] = {}
        starting_control_index = 0
        for parameter_rate in sorted(ParameterRate):
            if not (filtered_parameters := parameter_mapping.get(parameter_rate, [])):
                continue
            if parameter_rate == ParameterRate.SCALAR:
                control = Control(
                    calculation_rate=CalculationRate.SCALAR,
                    parameters=filtered_parameters,
                    special_index=starting_control_index,
                )
            elif parameter_rate == ParameterRate.TRIGGER:
                control = TrigControl(
                    calculation_rate=CalculationRate.CONTROL,
                    parameters=filtered_parameters,
                    special_index=starting_control_index,
                )
            elif parameter_rate == ParameterRate.AUDIO:
                control = AudioControl(
                    calculation_rate=CalculationRate.AUDIO,
                    parameters=filtered_parameters,
                    special_index=starting_control_index,
                )
            elif any(parameter.lag for parameter in filtered_parameters):
                control = LagControl(
                    calculation_rate=CalculationRate.CONTROL,
                    parameters=filtered_parameters,
                    special_index=starting_control_index,
                )
            else:
                control = Control(
                    calculation_rate=CalculationRate.CONTROL,
                    parameters=filtered_parameters,
                    special_index=starting_control_index,
                )
            controls.append(control)
            output_index = 0
            for parameter in filtered_parameters:
                for output in parameter:
                    control_mapping[cast(OutputProxy, output)] = cast(
                        OutputProxy, control[output_index]
                    )
                    output_index += 1
                    starting_control_index += 1
        return controls, control_mapping

    def _cleanup_local_bufs(self, ugens: list[UGen]) -> list[UGen]:
        from . import LocalBuf, MaxLocalBufs

        filtered_ugens: list[UGen] = []
        local_bufs: list[UGen] = []
        for ugen in ugens:
            if isinstance(ugen, MaxLocalBufs):
                continue  # purging MaxLocalBufs from the graph so we can rebuild
            if isinstance(ugen, LocalBuf):
                local_bufs.append(ugen)
            filtered_ugens.append(ugen)
        if local_bufs:
            max_local_bufs = cast(OutputProxy, MaxLocalBufs.ir(maximum=len(local_bufs)))
            for local_buf in local_bufs:
                inputs: list[OutputProxy | float] = list(local_buf.inputs[:2])
                inputs.append(max_local_bufs)
                local_buf._inputs = tuple(inputs)
            # Insert the MaxLocalBufs just before the first LocalBuf
            index = filtered_ugens.index(local_bufs[0])
            filtered_ugens[index:index] = [max_local_bufs.ugen]
        return filtered_ugens

    def _cleanup_pv_chains(self, ugens: list[UGen]) -> list[UGen]:
        from . import LocalBuf, PV_ChainUGen, PV_Copy

        mapping: dict[UGen, list[tuple[UGen, int]]] = {}
        for ugen in ugens:
            if isinstance(ugen, PV_Copy) or not isinstance(ugen, PV_ChainUGen):
                continue
            for i, input_ in enumerate(ugen.inputs):
                if not isinstance(input_, OutputProxy) or not isinstance(
                    input_.ugen, PV_ChainUGen
                ):
                    continue
                mapping.setdefault(input_.ugen, []).append((ugen, i))

        for antecedent, descendant_pairs in mapping.items():
            if len(descendant_pairs) < 2:
                continue
            for descendant, input_index in descendant_pairs[:-1]:
                fft_size = getattr(antecedent, "fft_size")
                # Create a new LocalBuf and PV_Copy
                new_buffer = cast(OutputProxy, LocalBuf.ir(frame_count=fft_size))
                pv_copy = cast(
                    OutputProxy,
                    PV_Copy.kr(pv_chain_a=antecedent, pv_chain_b=new_buffer),
                )
                # Patch the PV_Copy into the descendant's inputs
                inputs = list(descendant.inputs)
                inputs[input_index] = pv_copy
                descendant._inputs = tuple(inputs)
                # Insert the new Localbuf and PV_Copy into the graph
                index = ugens.index(descendant)
                replacement = []
                if isinstance(fft_size, OutputProxy):
                    replacement.append(fft_size.ugen)
                replacement.extend([new_buffer.ugen, pv_copy.ugen])
                ugens[index:index] = replacement
        return ugens

    def _initiate_topological_sort(self, ugens: list[UGen]) -> dict[UGen, SortBundle]:
        sort_bundles: dict[UGen, SynthDefBuilder.SortBundle] = {}
        width_first_antecedents: list[UGen] = []
        # The UGens are in the order they were added to the SynthDef and that
        # order already mostly places inputs before outputs.  In sclang, the
        # per-UGen width-first antecedents list is updated at the moment the
        # UGen is added to the SynthDef.  Because we don't store that state
        # directly on UGens in Supriya, we'll do it here.
        for ugen in ugens:
            sort_bundles[ugen] = self.SortBundle(
                antecedents=[],
                descendants=[],
                ugen=ugen,
                width_first_antecedents=tuple(width_first_antecedents),
            )
            if ugen._is_width_first:
                width_first_antecedents.append(ugen)
        for ugen, sort_bundle in sort_bundles.items():
            for input_ in ugen.inputs:
                if not isinstance(input_, OutputProxy):
                    continue
                if input_.ugen not in sort_bundle.antecedents:
                    sort_bundle.antecedents.append(input_.ugen)
                if (
                    ugen
                    not in (input_sort_bundle := sort_bundles[input_.ugen]).descendants
                ):
                    input_sort_bundle.descendants.append(ugen)
            for antecedent in sort_bundle.width_first_antecedents:
                if antecedent not in sort_bundle.antecedents:
                    sort_bundle.antecedents.append(antecedent)
                if (
                    ugen
                    not in (input_sort_bundle := sort_bundles[antecedent]).descendants
                ):
                    input_sort_bundle.descendants.append(ugen)
            sort_bundle.descendants[:] = sorted(
                sort_bundles[ugen].descendants, key=lambda x: ugens.index(ugen)
            )
        return sort_bundles

    def _optimize(self, ugens: list[UGen]) -> list[UGen]:
        sort_bundles = self._initiate_topological_sort(ugens)
        for ugen in ugens:
            ugen._optimize(sort_bundles)
        return list(sort_bundles)

    def _remap_controls(
        self, ugens: list[UGen], control_mapping: dict[OutputProxy, OutputProxy]
    ) -> list[UGen]:
        for ugen in ugens:
            ugen._inputs = tuple(
                (
                    control_mapping.get(input_, input_)
                    if isinstance(input_, OutputProxy)
                    else input_
                )
                for input_ in ugen._inputs
            )
        return ugens

    def _sort_topologically(self, ugens: list[UGen]) -> list[UGen]:
        sort_bundles = self._initiate_topological_sort(ugens)
        available_ugens: list[UGen] = []
        output_stack: list[UGen] = []
        for ugen in reversed(ugens):
            if not sort_bundles[ugen].antecedents and ugen not in available_ugens:
                available_ugens.append(ugen)
        while available_ugens:
            available_ugen = available_ugens.pop()
            for descendant in reversed(sort_bundles[available_ugen].descendants):
                (descendant_sort_bundle := sort_bundles[descendant]).antecedents.remove(
                    available_ugen
                )
                if (
                    not descendant_sort_bundle.antecedents
                    and descendant_sort_bundle.ugen not in available_ugens
                ):
                    available_ugens.append(descendant_sort_bundle.ugen)
            output_stack.append(available_ugen)
        return output_stack

    def add_parameter(
        self,
        *,
        name: str,
        value: float | Sequence[float],
        rate: ParameterRateLike | None = ParameterRate.CONTROL,
        lag: float | None = None,
    ) -> OutputProxy | Parameter:
        if name in self._parameters:
            raise ValueError(name, value)
        with self:
            parameter = Parameter(
                lag=lag, name=name, rate=ParameterRate.from_expr(rate), value=value
            )
        self._parameters[name] = parameter
        if len(parameter) == 1:
            return parameter[0]
        return parameter

    def build(self, name: str | None = None, optimize: bool = True) -> SynthDef:
        """
        Build.

        ::

            >>> from supriya.ugens import Out, SinOsc, SynthDefBuilder
            >>> with SynthDefBuilder(amplitude=1.0, bus=0, frequency=[440, 443]) as builder:
            ...     source = SinOsc.ar(frequency=builder["frequency"])
            ...     source *= builder["amplitude"]
            ...     _ = Out.ar(bus=builder["bus"], source=source)
            ...

        ::

            >>> synthdef = builder.build()
            >>> print(synthdef)
            synthdef:
                name: 4e5d18af62c02b10252a62def13fb402
                ugens:
                -   Control.kr:
                        amplitude: 1.0
                        bus: 0.0
                        frequency[0]: 440.0
                        frequency[1]: 443.0
                -   SinOsc.ar/0:
                        frequency: Control.kr[2:frequency[0]]
                        phase: 0.0
                -   BinaryOpUGen(MULTIPLICATION).ar/0:
                        left: SinOsc.ar/0[0]
                        right: Control.kr[0:amplitude]
                -   SinOsc.ar/1:
                        frequency: Control.kr[3:frequency[1]]
                        phase: 0.0
                -   BinaryOpUGen(MULTIPLICATION).ar/1:
                        left: SinOsc.ar/1[0]
                        right: Control.kr[0:amplitude]
                -   Out.ar:
                        bus: Control.kr[1:bus]
                        source[0]: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                        source[1]: BinaryOpUGen(MULTIPLICATION).ar/1[0]

        """
        try:
            self._building = True
            with self:
                ugens: list[UGen] = copy.deepcopy(self._ugens)
                parameters: list[Parameter] = sorted(
                    [x for x in ugens if isinstance(x, Parameter)],
                    key=lambda x: x.name or "",
                )
                ugens = [x for x in ugens if not isinstance(x, Parameter)]
                controls, control_mapping = self._build_control_mapping(parameters)
                ugens = controls + ugens
                ugens = self._remap_controls(ugens, control_mapping)
                ugens = self._cleanup_pv_chains(ugens)
                ugens = self._cleanup_local_bufs(ugens)
                ugens = self._sort_topologically(ugens)
                if optimize:
                    ugens = self._optimize(ugens)
        finally:
            self._building = False
        return SynthDef(ugens, name=name)


def synthdef(*args: str | tuple[str, float]) -> Callable[[Callable], SynthDef]:
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
            -   Control.kr:
                    amp: 0.1
                    freq: 440.0
                    gate: 1.0
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
            -   AudioControl.ar:
                    freq: 440.0
            -   SinOsc.ar:
                    frequency: AudioControl.ar[0:freq]
                    phase: 0.0
            -   LagControl.kr:
                    amp: 0.1
                    gate: 1.0
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
            kwargs[name] = builder.add_parameter(
                name=name, lag=lag, rate=rate, value=value
            )
        with builder:
            func(**kwargs)
        return builder.build(name=func.__name__)

    return inner


def _compile_constants(synthdef: SynthDef) -> bytes:
    return b"".join(
        [
            _encode_unsigned_int_32bit(len(synthdef.constants)),
            *(_encode_float(constant) for constant in synthdef.constants),
        ]
    )


def _compile_parameters(synthdef: SynthDef) -> bytes:
    result = [
        _encode_unsigned_int_32bit(sum(len(control) for control in synthdef.controls))
    ]
    for control in synthdef.controls:
        for parameter in control.parameters:
            for value in parameter.value:
                result.append(_encode_float(value))
    result.append(_encode_unsigned_int_32bit(len(synthdef.parameters)))
    for name, (_, index) in synthdef.parameters.items():
        result.append(_encode_string(name) + _encode_unsigned_int_32bit(index))
    return b"".join(result)


def _compile_synthdef(synthdef: SynthDef, name: str) -> bytes:
    return b"".join(
        [
            _encode_string(name),
            _compile_ugen_graph(synthdef),
        ]
    )


def _compile_ugen(ugen: UGen, synthdef: SynthDef) -> bytes:
    return b"".join(
        [
            _encode_string(type(ugen).__name__),
            _encode_unsigned_int_8bit(ugen.calculation_rate),
            _encode_unsigned_int_32bit(len(ugen.inputs)),
            _encode_unsigned_int_32bit(len(ugen)),
            _encode_unsigned_int_16bit(int(ugen.special_index)),
            *(_compile_ugen_input_spec(input_, synthdef) for input_ in ugen.inputs),
            *(
                _encode_unsigned_int_8bit(ugen.calculation_rate)
                for _ in range(len(ugen))
            ),
        ]
    )


def _compile_ugens(synthdef: SynthDef) -> bytes:
    return b"".join(
        [
            _encode_unsigned_int_32bit(len(synthdef.ugens)),
            *(_compile_ugen(ugen, synthdef) for ugen in synthdef.ugens),
        ]
    )


def _compile_ugen_graph(synthdef):
    return b"".join(
        [
            _compile_constants(synthdef),
            _compile_parameters(synthdef),
            _compile_ugens(synthdef),
            _encode_unsigned_int_16bit(0),  # no variants, please
        ]
    )


def _compile_ugen_input_spec(input_: OutputProxy | float, synthdef: SynthDef) -> bytes:
    if isinstance(input_, float):
        return _encode_unsigned_int_32bit(0xFFFFFFFF) + _encode_unsigned_int_32bit(
            synthdef._constants.index(input_)
        )
    else:
        return _encode_unsigned_int_32bit(
            synthdef._ugens.index(input_.ugen)
        ) + _encode_unsigned_int_32bit(input_.index)


def _encode_string(value: str) -> bytes:
    return struct.pack(">B", len(value)) + value.encode("ascii")


def _encode_float(value: float) -> bytes:
    return struct.pack(">f", value)


def _encode_unsigned_int_8bit(value: int) -> bytes:
    return struct.pack(">B", value)


def _encode_unsigned_int_16bit(value: int) -> bytes:
    return struct.pack(">H", value)


def _encode_unsigned_int_32bit(value: int) -> bytes:
    return struct.pack(">I", value)


def compile_synthdefs(
    synthdef: SynthDef, *synthdefs: SynthDef, use_anonymous_names: bool = False
) -> bytes:
    synthdefs_ = (synthdef,) + synthdefs
    return b"".join(
        [
            b"SCgf",
            _encode_unsigned_int_32bit(2),
            _encode_unsigned_int_16bit(len(synthdefs_)),
            *(
                _compile_synthdef(
                    synthdef,
                    (
                        synthdef.anonymous_name
                        if not synthdef.name or use_anonymous_names
                        else synthdef.name
                    ),
                )
                for synthdef in synthdefs_
            ),
        ]
    )


def _decode_string(value: bytes, index: int) -> tuple[str, int]:
    length, index = struct.unpack(">B", value[index : index + 1])[0], index + 1
    return value[index : index + length].decode("ascii"), index + length


def _decode_float(value: bytes, index: int) -> tuple[float, int]:
    return struct.unpack(">f", value[index : index + 4])[0], index + 4


def _decode_int_8bit(value: bytes, index: int) -> tuple[int, int]:
    return struct.unpack(">B", value[index : index + 1])[0], index + 1


def _decode_int_16bit(value: bytes, index: int) -> tuple[int, int]:
    return struct.unpack(">H", value[index : index + 2])[0], index + 2


def _decode_int_32bit(value: bytes, index: int) -> tuple[int, int]:
    return struct.unpack(">I", value[index : index + 4])[0], index + 4


def _decode_constants(value: bytes, index: int) -> tuple[Sequence[float], int]:
    constants = []
    constants_count, index = _decode_int_32bit(value, index)
    for _ in range(constants_count):
        constant, index = _decode_float(value, index)
        constants.append(constant)
    return constants, index


def _decode_parameters(value: bytes, index: int) -> tuple[dict[int, Parameter], int]:
    parameter_values = []
    parameter_count, index = _decode_int_32bit(value, index)
    for _ in range(parameter_count):
        parameter_value, index = _decode_float(value, index)
        parameter_values.append(parameter_value)
    parameter_count, index = _decode_int_32bit(value, index)
    parameter_names = []
    parameter_indices = []
    for _ in range(parameter_count):
        parameter_name, index = _decode_string(value, index)
        parameter_index, index = _decode_int_32bit(value, index)
        parameter_names.append(parameter_name)
        parameter_indices.append(parameter_index)
    indexed_parameters = []
    if parameter_count:
        for (index_one, name_one), (index_two, name_two) in iterate_nwise(
            sorted(
                zip(parameter_indices, parameter_names),
                key=lambda x: x[0],
            )
            + [(len(parameter_values), "")]
        ):
            indexed_parameters.append(
                (
                    index_one,
                    Parameter(
                        name=name_one, value=parameter_values[index_one:index_two]
                    ),
                )
            )
        indexed_parameters.sort(key=lambda x: parameter_names.index(x[1].name or ""))
    return dict(indexed_parameters), index


def _decompile_control_parameters(
    calculation_rate: CalculationRate,
    indexed_parameters: dict[int, Parameter],
    inputs: Sequence[OutputProxy | float],
    output_count: int,
    special_index: int,
    ugen_class: Type[UGen],
) -> Sequence[Parameter]:
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
            lag = cast(float, inputs[collected_output_count])
        parameter = indexed_parameters[special_index + collected_output_count]
        parameter.rate = parameter_rate
        if lag:
            parameter.lag = lag
        parameters.append(parameter)
        collected_output_count += len(parameter)
    return parameters


def _decompile_synthdef(value: bytes, index: int) -> tuple[SynthDef, int]:
    from supriya import ugens

    name, index = _decode_string(value, index)
    constants, index = _decode_constants(value, index)
    indexed_parameters, index = _decode_parameters(value, index)
    decompiled_ugens: list[UGen] = []
    ugen_count, index = _decode_int_32bit(value, index)
    for i in range(ugen_count):
        ugen_name, index = _decode_string(value, index)
        calculation_rate, index = _decode_int_8bit(value, index)
        calculation_rate = CalculationRate(calculation_rate)
        input_count, index = _decode_int_32bit(value, index)
        output_count, index = _decode_int_32bit(value, index)
        special_index, index = _decode_int_16bit(value, index)
        inputs: list[OutputProxy | float] = []
        for _ in range(input_count):
            ugen_index, index = _decode_int_32bit(value, index)
            if ugen_index == 0xFFFFFFFF:
                constant_index, index = _decode_int_32bit(value, index)
                inputs.append(constants[constant_index])
            else:
                ugen = decompiled_ugens[ugen_index]
                ugen_output_index, index = _decode_int_32bit(value, index)
                output_proxy = ugen[ugen_output_index]
                inputs.append(output_proxy)
        for _ in range(output_count):
            output_rate, index = _decode_int_8bit(value, index)
        ugen_class = cast(Type[UGen], getattr(ugens, ugen_name, None))
        ugen = UGen.__new__(ugen_class)
        if issubclass(ugen_class, Control):
            parameters = _decompile_control_parameters(
                calculation_rate,
                indexed_parameters,
                inputs,
                output_count,
                special_index,
                ugen_class,
            )
            ugen_class.__init__(
                cast(Control, ugen),
                parameters=parameters,
                special_index=special_index,
                calculation_rate=calculation_rate,
            )
        else:
            kwargs: UGenParams = {}
            if not ugen._unexpanded_keys:
                for i, input_name in enumerate(ugen._ordered_keys):
                    kwargs[input_name] = inputs[i]
            else:
                for i, input_name in enumerate(ugen._ordered_keys):
                    if input_name not in ugen._unexpanded_keys:
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
    variants_count, index = _decode_int_16bit(value, index)
    synthdef = SynthDef(ugens=decompiled_ugens, name=name)
    if synthdef.name == synthdef.anonymous_name:
        synthdef._name = None
    return synthdef, index


def decompile_synthdef(value: bytes) -> SynthDef:
    if len(synthdefs := decompile_synthdefs(value)) != 1:
        raise ValueError(bytes)
    return synthdefs[0]


def decompile_synthdefs(value: bytes) -> list[SynthDef]:
    synthdefs: list[SynthDef] = []
    index = 4
    if value[:index] != b"SCgf":
        raise ValueError(value)
    file_version, index = _decode_int_32bit(value, index)
    synthdef_count, index = _decode_int_16bit(value, index)
    for _ in range(synthdef_count):
        synthdef, index = _decompile_synthdef(value, index)
        synthdefs.append(synthdef)
    return synthdefs


class SuperColliderSynthDef:
    def __init__(self, name: str, body: str, rates: str | None = None):
        self.name = name
        self.body = body
        self.rates = rates

    def _build_sc_input(self, directory_path: Path) -> str:
        input_ = [
            "a = SynthDef(",
            "    \\{}, {{".format(self.name),
        ]
        for line in self.body.splitlines():
            input_.append("    " + line)
        if self.rates:
            input_.append("}}, {});".format(self.rates))
        else:
            input_.append("});")
        input_.extend(
            [
                '"Defined SynthDef".postln;',
                'a.writeDefFile("{}");'.format(directory_path),
                '"Wrote SynthDef".postln;',
                "0.exit;",
            ]
        )
        text = "\n".join(input_)
        print(text)
        return text

    def compile(self) -> bytes:
        sclang_path = sclang.find()
        with tempfile.TemporaryDirectory() as directory:
            directory_path = Path(directory)
            sc_input = self._build_sc_input(directory_path)
            sc_file_path = directory_path / f"{self.name}.sc"
            sc_file_path.write_text(sc_input)
            command = [str(sclang_path), "-D", str(sc_file_path)]
            subprocess.run(command, timeout=10)
            result = (directory_path / f"{self.name}.scsyndef").read_bytes()
        return bytes(result)
