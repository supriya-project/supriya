import inspect
from enum import Enum
from typing import NamedTuple, Optional

from ..enums import CalculationRate, SignalRange


def _create_fn(cls, name, args, body, globals_=None, decorator=None, override=False):
    if name in cls.__dict__ and not override:
        return
    globals_ = globals_ or {}
    locals_ = {"_return_type": cls}
    args = ", ".join(args)
    body = "\n".join(f"        {line}" for line in body)
    text = f"    def {name}({args}) -> _return_type:\n{body}"
    local_vars = ", ".join(locals_.keys())
    text = f"def __create_fn__({local_vars}):\n{text}\n    return {name}"
    namespace = {}
    exec(text, globals_, namespace)
    value = namespace["__create_fn__"](**locals_)
    value.__qualname__ = f"{cls.__qualname__}.{value.__name__}"
    if decorator:
        value = decorator(value)
    setattr(cls, name, value)


def _add_init(cls, params, is_multichannel, fixed_channel_count):
    parent_class = inspect.getmro(cls)[1]
    name = "__init__"
    args = ["self", "calculation_rate=None"]
    body = []
    if is_multichannel:
        if fixed_channel_count:
            body.append(f"self._channel_count = {fixed_channel_count}")
        else:
            args.append("channel_count=1")
            body.append("self._channel_count = channel_count")
    body.extend(
        [
            f"return {parent_class.__name__}.__init__(",
            "    self,",
            "    calculation_rate=CalculationRate.from_expr(calculation_rate),",
        ]
    )
    for key, value in params.items():
        args.append(f"{key}={value}")
        body.append(f"    {key}={key},")
    args.append("**kwargs")
    body.append("    **kwargs,")
    body.append(")")
    globals_ = {"CalculationRate": CalculationRate, parent_class.__name__: parent_class}
    return _create_fn(cls=cls, name=name, args=args, body=body, globals_=globals_)


def _add_rate_fn(cls, rate, params):
    name = rate.token if rate is not None else "new"
    args = ["cls"] + [f"{name}={value}" for name, value in params.items()]
    body = ["return cls._new_expanded("]
    if rate is not None:
        body.append(f"    calculation_rate={rate!r},")
    body.extend(f"    {name}={name}," for name in params)
    body.append(")")
    globals_ = {"CalculationRate": CalculationRate}
    return _create_fn(
        cls, name, args=args, body=body, decorator=classmethod, globals_=globals_
    )


def _add_param_fn(cls, name, index, unexpanded):
    args = ["self"]
    if unexpanded:
        body = [f"return self._inputs[{index}:]"]
    else:
        body = [f"return self._inputs[{index}]"]
    return _create_fn(
        cls, name, args=args, body=body, decorator=property, override=True
    )


class Check(Enum):
    NONE = 0
    SAME_AS_FIRST = 1
    SAME_OR_SLOWER = 2


class Parameter(NamedTuple):
    default: Optional[float] = None
    check: Check = Check.NONE
    unexpanded: bool = False


def _process_class(
    cls,
    *,
    ar,
    ir,
    kr,
    new,
    has_done_flag,
    is_input,
    is_multichannel,
    is_output,
    is_pure,
    is_width_first,
    fixed_channel_count,
    signal_range,
):
    params = {}
    unexpanded_input_names = []
    valid_calculation_rates = []
    for name, value in cls.__dict__.items():
        if not isinstance(value, Parameter):
            continue
        params[name] = value.default
        if value.unexpanded:
            unexpanded_input_names.append(name)
        _add_param_fn(cls, name, len(params) - 1, value.unexpanded)
    _add_init(cls, params, is_multichannel, fixed_channel_count)
    for should_add, rate in [
        (ar, CalculationRate.AUDIO),
        (kr, CalculationRate.CONTROL),
        (ir, CalculationRate.SCALAR),
        (new, None),
    ]:
        if not should_add:
            continue
        _add_rate_fn(cls, rate, params)
        if rate is not None:
            valid_calculation_rates.append(rate)
    cls._has_done_flag = bool(has_done_flag)
    cls._is_input = bool(is_input)
    cls._is_output = bool(is_output)
    cls._is_pure = bool(is_pure)
    cls._is_width_first = bool(is_width_first)
    cls._ordered_input_names = params
    cls._unexpanded_input_names = tuple(unexpanded_input_names)
    cls._valid_calculation_rates = tuple(valid_calculation_rates)
    if signal_range is not None:
        cls._signal_range = SignalRange.from_expr(signal_range)
    return cls


def param(
    default: Optional[float] = None,
    /,
    *,
    check: Check = Check.NONE,
    unexpanded: bool = False,
):
    """
    Define a UGen parameter.

    Akin to dataclasses.field.
    """
    return Parameter(default, check, unexpanded)


def ugen(
    cls=None,
    /,
    *,
    ar: bool = False,
    kr: bool = False,
    ir: bool = False,
    new: bool = False,
    has_done_flag: bool = False,
    is_input: bool = False,
    is_multichannel: bool = False,
    is_output: bool = False,
    is_pure: bool = False,
    is_width_first: bool = False,
    fixed_channel_count: Optional[int] = None,
    signal_range: Optional[SignalRange] = None,
):
    """
    Decorate a UGen class.

    Akin to dataclasses.dataclass.
    """

    def wrap(cls):
        return _process_class(
            cls,
            ar=ar,
            kr=kr,
            ir=ir,
            new=new,
            has_done_flag=has_done_flag,
            is_input=is_input,
            is_multichannel=is_multichannel,
            is_output=is_output,
            is_pure=is_pure,
            is_width_first=is_width_first,
            fixed_channel_count=fixed_channel_count,
            signal_range=signal_range,
        )

    if cls is None:
        return wrap
    return wrap(cls)
