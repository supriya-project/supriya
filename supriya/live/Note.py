import dataclasses
from typing import Optional


@dataclasses.dataclass(frozen=True, order=True)
class Note:
    start_offset: Optional[float] = None
    stop_offset: Optional[float] = None
    pitch: float = 0.0
    velocity: float = 1.0

    def __post_init__(self):
        if self.start_offset >= self.stop_offset:
            raise ValueError

    def transpose(self, transposition):
        pass

    def translate(self, start_translation=None, stop_translation=None):
        start_offset = self.start_offset + (start_translation or 0)
        stop_offset = self.stop_offset + (stop_translation or 0)
        return dataclasses.replace(
            self, start_offset=start_offset, stop_offset=stop_offset
        )
