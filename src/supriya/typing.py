import asyncio
import concurrent.futures
from os import PathLike
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Coroutine,
    Protocol,
    SupportsFloat,
    SupportsInt,
    TypeAlias,
    TypeVar,
    Union,
    runtime_checkable,
)
from uuid import UUID

from .enums import (
    AddAction,
    CalculationRate,
    DoneAction,
    EnvelopeShape,
    HeaderFormat,
    ParameterRate,
    SampleFormat,
    ServerLifecycleEvent,
)

if TYPE_CHECKING:
    import numpy

    from .osc import OscBundle, OscMessage


class Default:
    pass


class Inherit:
    pass


class Missing:
    pass


DEFAULT = Default()
INHERIT = Inherit()
MISSING = Missing()


@runtime_checkable
class SupportsOsc(Protocol):
    def to_osc(self) -> Union["OscBundle", "OscMessage"]:
        pass


@runtime_checkable
class SupportsPlot(Protocol):
    def __plot__(self) -> tuple["numpy.ndarray", float]:
        pass


@runtime_checkable
class SupportsRender(Protocol):
    def __render__(
        self,
        output_file_path: PathLike | None = None,
        render_directory_path: PathLike | None = None,
        **kwargs,
    ) -> Coroutine[None, None, tuple[Path | None, int]]:
        pass


@runtime_checkable
class SupportsRenderMemo(Protocol):
    def __render_memo__(self) -> SupportsRender:
        pass


E = TypeVar("E")

_EnumLike = Union[E, SupportsInt, str] | None

AddActionLike: TypeAlias = _EnumLike[AddAction]
DoneActionLike: TypeAlias = _EnumLike[DoneAction]
CalculationRateLike: TypeAlias = _EnumLike[CalculationRate]
FutureLike: TypeAlias = concurrent.futures.Future[E] | asyncio.Future[E]
ParameterRateLike: TypeAlias = _EnumLike[ParameterRate]
RateLike: TypeAlias = _EnumLike[CalculationRate]
EnvelopeShapeLike: TypeAlias = _EnumLike[EnvelopeShape]
HeaderFormatLike: TypeAlias = _EnumLike[HeaderFormat]
SampleFormatLike: TypeAlias = _EnumLike[SampleFormat]
ServerLifecycleEventLike: TypeAlias = _EnumLike[ServerLifecycleEvent]
UGenInputMap: TypeAlias = dict[str, SupportsFloat | str | None] | None

UUIDDict: TypeAlias = dict[str, UUID]
