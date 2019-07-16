from supriya.time.Interval import Interval


class Block(Interval):

    ### CLASS VARIABLES ###

    __documentation_section__ = "Server Internals"

    __slots__ = ("_used",)

    ### INITIALIZER ###

    def __init__(
        self, start_offset: float = float("-inf"), stop_offset: float = float("inf"), used: bool = False
    ):
        Interval.__init__(self, start_offset=start_offset, stop_offset=stop_offset)
        self._used = bool(used)

    ### PUBLIC PROPERTIES ###

    @property
    def used(self) -> bool:
        return self._used
