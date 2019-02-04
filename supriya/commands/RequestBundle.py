import threading

import supriya.osc
from supriya.commands.Requestable import Requestable


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

        >>> request_bundle.to_osc(True)
        OscBundle(
            contents=(
                OscMessage('/b_alloc', 23, 512, 1),
                OscMessage('/b_alloc', 24, 512, 1),
                ),
            timestamp=10.5,
            )

    ::

        >>> request_bundle.to_list(True)
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

    def _get_response_pattern_and_requestable(self, server):
        sync_id = server.next_sync_id
        contents = list(self.contents)
        contents.append(supriya.commands.SyncRequest(sync_id=sync_id))
        request_bundle = type(self)(contents=contents)
        response_pattern = ["/synced", sync_id]
        return response_pattern, request_bundle

    def _handle_async(self, sync, server):
        if not sync:
            server.send_message(self)
            return True

    def _linearize(self):
        for x in self.contents:
            yield from x._linearize()

    ### PUBLIC METHODS ###

    def to_datagram(self):
        return self.to_osc().to_datagram()

    def to_list(self, with_request_name=False):
        return self.to_osc(with_request_name).to_list()

    def to_osc(self, with_request_name=False):
        contents = []
        for x in self.contents:
            if isinstance(x, type(self)):
                contents.append(x.to_osc(with_request_name))
            else:
                contents.append(x.to_osc(with_request_name))
        bundle = supriya.osc.OscBundle(timestamp=self.timestamp, contents=contents)
        return bundle

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
