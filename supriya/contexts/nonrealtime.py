from typing import Dict, Iterator, List, Optional, SupportsInt, Type, Union

from ..commands import Request, RequestBundle, Requestable
from ..enums import CalculationRate
from ..osc import OscBundle
from ..scsynth import Options
from .core import Context, ContextError, ContextObject, Node


class NonrealtimeContext(Context):

    ### INITIALIZER ###

    def __init__(self, options: Optional[Options] = None, **kwargs):
        super().__init__(options=options, **kwargs)
        self._requests: Dict[float, List[Request]] = {}

    ### PRIVATE METHODS ###

    def _free_id(
        self,
        type_: Type[ContextObject],
        id_: int,
        calculation_rate: Optional[CalculationRate] = None,
    ) -> None:
        pass

    def _resolve_node(self, node: Union[Node, SupportsInt, None]) -> int:
        if node is None:
            return 0
        return int(node)

    def _validate_can_request(self) -> None:
        if self._get_moment() is None:
            raise ContextError

    def _validate_moment_timestamp(self, seconds: Optional[float]) -> None:
        if seconds is None or seconds < 0:
            raise ContextError

    ### PUBLIC METHODS ###

    def iterate_osc_bundles(self) -> Iterator[OscBundle]:
        for request_bundle in self.iterate_request_bundles():
            yield request_bundle.to_osc()

    def iterate_request_bundles(self) -> Iterator[RequestBundle]:
        for timestamp, requests in sorted(self._requests.items()):
            if not requests:
                continue
            yield RequestBundle(timestamp=timestamp, contents=requests)

    def send(self, requestable: Requestable) -> None:
        if not isinstance(requestable, RequestBundle):
            raise ContextError
        elif requestable.timestamp is None:
            raise ContextError
        self._requests.setdefault(requestable.timestamp, []).extend(
            requestable.contents
        )
