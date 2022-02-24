from os import PathLike
from pathlib import Path
from typing import Dict, Optional, SupportsFloat, SupportsInt, Union

try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol  # type: ignore

from .enums import AddAction, CalculationRate, HeaderFormat, SampleFormat


class Default:
    pass


class Missing:
    pass


class SupportsRender(Protocol):
    def __render__(
        self,
        output_file_path: Optional[PathLike] = None,
        render_directory_path: Optional[PathLike] = None,
        **kwargs,
    ) -> Union[Path, "SupportsRender"]:
        ...


AddActionLike = Optional[Union[AddAction, SupportsInt, str]]
CalculationRateLike = Optional[Union[CalculationRate, SupportsInt, str]]
HeaderFormatLike = Optional[Union[HeaderFormat, SupportsInt, str]]
SampleFormatLike = Optional[Union[SampleFormat, SupportsInt, str]]
UGenInputMap = Optional[Dict[str, Union[SupportsFloat, str, None]]]
