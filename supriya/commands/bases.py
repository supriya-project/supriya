import abc
import asyncio
import logging
import threading
import time
from collections import deque

from uqbar.objects import new

from supriya.exceptions import ServerOffline
from supriya.osc.messages import BUNDLE_PREFIX, OscBundle
from supriya.system import SupriyaValueObject

logger = logging.getLogger("supriya.osc")


class Requestable(SupriyaValueObject):

    ### INITIALIZER ###

    def __init__(self):
        self._condition = threading.Condition()
        self._response = None

    ### PRIVATE METHODS ###

    def _get_response_patterns_and_requestable(self, server):
        raise NotImplementedError

    def _handle_async(self, sync, server):
        raise NotImplementedError

    def _linearize(self):
        raise NotImplementedError

    def _sanitize_node_id(self, node_id, with_placeholders):
        if not isinstance(node_id, int) and with_placeholders:
            return -1
        return int(node_id)

    def _set_response(self, message):
        from supriya.commands import Response

        with self.condition:
            self._response = Response.from_osc_message(message)
            self.condition.notify()

    def _set_response_async(self, message):
        from supriya.commands import Response

        self._response = Response.from_osc_message(message)
        self._response_future.set_result(True)

    ### PUBLIC METHODS ###

    def communicate(self, server, sync=True, timeout=1.0, apply_local=True):
        import supriya.realtime

        if not isinstance(server, supriya.realtime.servers.BaseServer):
            raise ValueError(server)
        if not server.is_running:
            raise ServerOffline
        if apply_local:
            with server._lock:
                for request in self._linearize():
                    request._apply_local(server)
        # handle non-sync
        if self._handle_async(sync, server):
            return
        (
            success_pattern,
            failure_pattern,
            requestable,
        ) = self._get_response_patterns_and_requestable(server)
        start_time = time.time()
        timed_out = False
        with self.condition:
            try:
                server.osc_protocol.register(
                    pattern=success_pattern,
                    failure_pattern=failure_pattern,
                    procedure=self._set_response,
                    once=True,
                )
            except Exception:
                print(self)
                raise
            server.send(requestable.to_osc())
            while self.response is None:
                self.condition.wait(timeout)
                current_time = time.time()
                delta_time = current_time - start_time
                if timeout <= delta_time:
                    timed_out = True
                    break
        if timed_out:
            logger.warning("Timed out: {!r}".format(self))
            return None
        return self._response

    async def communicate_async(self, server, sync=True, timeout=1.0):
        (
            success_pattern,
            failure_pattern,
            requestable,
        ) = self._get_response_patterns_and_requestable(server)
        if self._handle_async(sync, server):
            return
        loop = asyncio.get_running_loop()
        self._response_future = loop.create_future()
        server.osc_protocol.register(
            pattern=success_pattern,
            failure_pattern=failure_pattern,
            procedure=self._set_response_async,
            once=True,
        )
        server.send(requestable.to_osc())
        await asyncio.wait_for(self._response_future, timeout=timeout)
        return self._response

    def to_datagram(self, *, with_placeholders=False):
        return self.to_osc(with_placeholders=with_placeholders).to_datagram()

    def to_list(self, *, with_placeholders=False):
        return self.to_osc(with_placeholders=with_placeholders).to_list()

    ### PUBLIC PROPERTIES ###

    @property
    def condition(self):
        return self._condition

    @property
    def response(self):
        return self._response


class Request(Requestable):

    ### PRIVATE METHODS ###

    def _apply_local(self, server):
        pass

    def _get_response_patterns_and_requestable(self, server):
        success_pattern, failure_pattern = self.response_patterns
        return success_pattern, failure_pattern, self

    def _handle_async(self, sync, server):
        if not sync or self.response_patterns[0] is None:
            message = self.to_osc()
            server.send(message)
            return True

    def _linearize(self):
        if hasattr(self, "callback") and self.callback:
            yield new(self, callback=None)
            yield from self.callback._linearize()
        else:
            yield self

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def to_osc(self, *, with_placeholders=False):
        raise NotImplementedError

    ### PUBLIC PROPERTIES ###

    @property
    def request_name(self):
        return self.request_id.request_name

    @property
    def response_patterns(self):
        return None, None

    @property
    @abc.abstractmethod
    def request_id(self):
        return NotImplementedError


class RequestBundle(Requestable):
    """
    A Request bundle.

    ::

        >>> request_one = supriya.commands.BufferAllocateRequest(
        ...     buffer_id=23,
        ...     frame_count=512,
        ...     channel_count=1,
        ... )
        >>> request_two = supriya.commands.BufferAllocateRequest(
        ...     buffer_id=24,
        ...     frame_count=512,
        ...     channel_count=1,
        ... )
        >>> request_bundle = supriya.commands.RequestBundle(
        ...     timestamp=10.5,
        ...     contents=[request_one, request_two],
        ... )

    ::

        >>> request_bundle.to_osc()
        OscBundle(
            contents=(
                OscMessage('/b_alloc', 23, 512, 1),
                OscMessage('/b_alloc', 24, 512, 1),
            ),
            timestamp=10.5,
        )

    ::

        >>> request_bundle.to_list()
        [10.5, [['/b_alloc', 23, 512, 1], ['/b_alloc', 24, 512, 1]]]

    """

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
        from supriya.commands import SyncRequest

        sync_id = server.next_sync_id
        contents = list(self.contents)
        contents.append(SyncRequest(sync_id=sync_id))
        request_bundle = type(self)(contents=contents)
        response_pattern = ["/synced", sync_id]
        return response_pattern, None, request_bundle

    def _handle_async(self, sync, server):
        if not sync:
            message = self.to_osc()
            server.send(message)
            return True

    def _linearize(self):
        for x in self.contents:
            yield from x._linearize()

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        contents = []
        for x in self.contents:
            if isinstance(x, type(self)):
                contents.append(x.to_osc(with_placeholders=with_placeholders))
            else:
                contents.append(x.to_osc(with_placeholders=with_placeholders))
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


class Response(SupriyaValueObject):

    ### PRIVATE METHODS ###

    @staticmethod
    def _group_items(items, length):
        iterators = [iter(items)] * length
        iterator = zip(*iterators)
        return iterator

    ### PUBLIC METHODS ###

    @classmethod
    def from_osc_message(cls, message):
        import supriya.commands

        return {
            "/b_info": supriya.commands.BufferInfoResponse,
            "/b_set": supriya.commands.BufferSetResponse,
            "/b_setn": supriya.commands.BufferSetContiguousResponse,
            "/c_set": supriya.commands.ControlBusSetResponse,
            "/c_setn": supriya.commands.ControlBusSetContiguousResponse,
            "/d_removed": supriya.commands.SynthDefRemovedResponse,
            "/done": supriya.commands.DoneResponse,
            "/fail": supriya.commands.FailResponse,
            "/g_queryTree.reply": supriya.commands.QueryTreeResponse,
            "/n_end": supriya.commands.NodeInfoResponse,
            "/n_go": supriya.commands.NodeInfoResponse,
            "/n_info": supriya.commands.NodeInfoResponse,
            "/n_move": supriya.commands.NodeInfoResponse,
            "/n_off": supriya.commands.NodeInfoResponse,
            "/n_on": supriya.commands.NodeInfoResponse,
            "/n_set": supriya.commands.NodeSetResponse,
            "/n_setn": supriya.commands.NodeSetContiguousResponse,
            "/status.reply": supriya.commands.StatusResponse,
            "/synced": supriya.commands.SyncedResponse,
            "/tr": supriya.commands.TriggerResponse,
        }[message.address].from_osc_message(message)

    def to_dict(self):
        result = {}
        for key, value in self.__getstate__().items():
            key = key[1:]
            if key == "osc_message":
                continue
            result[key] = value
        return result
