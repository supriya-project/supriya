from typing import Callable, NamedTuple, Optional, Tuple, Union


class OscCallback(NamedTuple):
    pattern: Tuple[Union[str, int, float], ...]
    procedure: Callable
    failure_pattern: Optional[Tuple[Union[str, int, float], ...]] = None
    once: bool = False
