from os import PathLike
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Coroutine,
    Dict,
    Optional,
    SupportsFloat,
    SupportsInt,
    Tuple,
    Union,
    runtime_checkable,
)

try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol  # type: ignore

from .enums import AddAction, CalculationRate, HeaderFormat, SampleFormat

if TYPE_CHECKING:
    import numpy

    from .osc import OscBundle, OscMessage


class Default:
    pass


class Missing:
    pass


@runtime_checkable
class SupportsOsc(Protocol):
    def to_osc(self) -> Union["OscBundle", "OscMessage"]:
        ...


@runtime_checkable
class SupportsPlot(Protocol):
    def __plot__(self) -> "numpy.ndarray":
        ...


@runtime_checkable
class SupportsRender(Protocol):
    def __render__(
        self,
        output_file_path: Optional[PathLike] = None,
        render_directory_path: Optional[PathLike] = None,
        **kwargs,
    ) -> Coroutine[None, None, Tuple[Optional[Path], int]]:
        ...


@runtime_checkable
class SupportsRenderMemo(Protocol):
    def __render_memo__(self) -> SupportsRender:
        ...


AddActionLike = Optional[Union[AddAction, SupportsInt, str]]
CalculationRateLike = Optional[Union[CalculationRate, SupportsInt, str]]
HeaderFormatLike = Optional[Union[HeaderFormat, SupportsInt, str]]
SampleFormatLike = Optional[Union[SampleFormat, SupportsInt, str]]
UGenInputMap = Optional[Dict[str, Union[SupportsFloat, str, None]]]
