from types import FunctionType
from typing import NamedTuple, Optional

from ..enums import CalculationRate
from .bases import UGen


def _create_fn(cls, name, args, body):
    globals_ = {"CalculationRate": CalculationRate}
    locals_ = {"_return_type": cls}
    args = ", ".join(args)
    body = "\n".join(f"        {line}" for line in body)
    text = f"    def {name}({args}) -> _return_type:\n{body}"
    local_vars = ", ".join(locals_.keys())
    text = f"def __create_fn__({local_vars}):\n{text}\n    return {name}"
    namespace = {}
    exec(text, globals_, namespace)
    return namespace["__create_fn__"](**locals_)


def _set_qualname(cls, value):
    if isinstance(value, FunctionType):
        value.__qualname__ = f"{cls.__qualname__}.{value.__name__}"
    return value


def _set_new_attribute(cls, name, value):
    if name in cls.__dict__:
        return True
    _set_qualname(cls, value)
    setattr(cls, name, value)
    return False


def _rate_fn(cls, rate, params):
    args = ["cls"] + [f"{name}={value}" for name, value in params.items()]
    body = [
        "return cls(",
        f"    calculation_rate={rate!r},",
        *[f"    {name}={name}," for name in params],
        ")",
    ]
    return classmethod(_create_fn(cls, rate.token, args=args, body=body))


class Parameter(NamedTuple):
    default: Optional[float] = None
    unexpanded: bool = False


def _process_class(cls, ar, done, input_, ir, kr, output, pure, width_first):
    if not any([ar, ir, kr]):
        raise ValueError
    params = {}
    unexpanded_input_names = []
    for name, value in cls.__dict__.items():
        if not isinstance(value, Parameter):
            continue
        params[name] = value.default
        if value.unexpanded:
            unexpanded_input_names.append(name)
    if ar:
        _set_new_attribute(cls, "ar", _rate_fn(cls, CalculationRate.AUDIO, params))
    if ir:
        _set_new_attribute(cls, "ir", _rate_fn(cls, CalculationRate.SCALAR, params))
    if kr:
        _set_new_attribute(cls, "kr", _rate_fn(cls, CalculationRate.CONTROL, params))
    cls._has_done_flag = bool(done)
    cls._is_input = bool(input_)
    cls._is_output = bool(output)
    cls._is_pure = bool(pure)
    cls._is_width_first = bool(width_first)
    cls._ordered_input_names = params
    cls._unexpanded_input_names = tuple(unexpanded_input_names)
    return cls


def param(default=None, unexpanded=False):
    return Parameter(default, unexpanded)


def ugen(
    cls=None,
    /,
    *,
    ar: bool = False,
    done: bool = False,
    input_: bool = False,
    ir: bool = False,
    kr: bool = False,
    output: bool = False,
    pure: bool = False,
    width_first: bool = False,
):
    def wrap(cls):
        return _process_class(cls, ar, done, input_, ir, kr, output, pure, width_first)

    if cls is None:
        return wrap
    return wrap(cls)


@ugen(ar=True, kr=True, pure=True, width_first=True)
class Foo(UGen):
    source = param(None, unexpanded=True)
    windows_size = param(0.2)
    pitch_ratio = param(1.0)
    pitch_dispersion = param(0.0)
    time_dispersion = param(0.0)
