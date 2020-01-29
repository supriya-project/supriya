import threading
from collections import deque

from supriya.commands.Requestable import Requestable
from supriya.commands.SyncRequest import SyncRequest
from supriya.osc import OscBundle, BUNDLE_PREFIX


class RequestBundle(Requestable):
    """
    A Request bundle.

    ::

        >>> request_one = supriya.commands.BufferAllocateRequest(
        ...     buffer_id=23,
        ...     frame_count=512,
        ...     channel_count=1,
        ...     )
        >>> request_two = supriya.commands.BufferAllocateRequest(
        ...     buffer_id=24,
        ...     frame_count=512,
        ...     channel_count=1,
        ...     )
        >>> request_bundle = supriya.commands.RequestBundle(
        ...     timestamp=10.5,
        ...     contents=[request_one, request_two],
        ...     )

    ::

        >>> request_bundle.to_osc(with_request_name=True)
        OscBundle(
            contents=(
                OscMessage('/b_alloc', 23, 512, 1),
                OscMessage('/b_alloc', 24, 512, 1),
                ),
            timestamp=10.5,
            )

    ::

        >>> request_bundle.to_list(with_request_name=True)
        [10.5, [['/b_alloc', 23, 512, 1], ['/b_alloc', 24, 512, 1]]]

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_contents", "_timestamp")

    ### INITIALIZER ###

    def __init__(self, timestamp=None, contents=None):
        import supriya.commands

        self._condition = threading.Condition()
        self._timestamp = timestamp
        if contents is not None:
            prototype = (supriya.commands.Request, type(self))
            assert all(isinstance(x, prototype) for x in contents)
            contents = tuple(contents)
        else:
            contents = ()
        self._contents = contents
        self._response = None

    ### PRIVATE METHODS ###

    def _get_response_patterns_and_requestable(self, server):
        sync_id = server.next_sync_id
        contents = list(self.contents)
        contents.append(SyncRequest(sync_id=sync_id))
        request_bundle = type(self)(contents=contents)
        response_pattern = ["/synced", sync_id]
        return response_pattern, None, request_bundle

    def _handle_async(self, sync, server):
        if not sync:
            server.send_message(self)
            return True

    def _linearize(self):
        for x in self.contents:
            yield from x._linearize()

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False, with_request_name=False):
        contents = []
        for x in self.contents:
            if isinstance(x, type(self)):
                contents.append(
                    x.to_osc(
                        with_placeholders=with_placeholders,
                        with_request_name=with_request_name,
                    )
                )
            else:
                contents.append(
                    x.to_osc(
                        with_placeholders=with_placeholders,
                        with_request_name=with_request_name,
                    )
                )
        bundle = OscBundle(timestamp=self.timestamp, contents=contents)
        return bundle

    @classmethod
    def partition(cls, requests, timestamp=None):
        bundles = []
        contents = []
        requests = deque(requests)
        remaining = maximum = 8192 - len(BUNDLE_PREFIX) - 4
        while requests:
            request = requests.popleft()
            datagram = request.to_datagram()
            remaining -= len(datagram) + 4
            if remaining > 0:
                contents.append(request)
            else:
                bundles.append(cls(timestamp=timestamp, contents=contents))
                contents = [request]
                remaining = maximum
        if contents:
            bundles.append(cls(timestamp=timestamp, contents=contents))
        return bundles

    ### PUBLIC PROPERTIES ###

    @property
    def condition(self):
        return self._condition

    @property
    def contents(self):
        return self._contents

    @property
    def timestamp(self):
        return self._timestamp
