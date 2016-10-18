# -*- encoding: utf-8 -*-
from abjad import new
import itertools
import time
try:
    from queue import PriorityQueue
except ImportError:
    from Queue import PriorityQueue
from supriya.tools import requesttools
from supriya.tools import servertools
from supriya.tools.patterntools.EventPlayer import EventPlayer


class RealtimeEventPlayer(EventPlayer):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_clock',
        '_iterator',
        '_pattern',
        '_server',
        '_uuids',
        '_call_count',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pattern,
        server=None,
        event_template=None,
        clock=None,
        ):
        from supriya.tools import patterntools
        EventPlayer.__init__(
            self,
            pattern,
            event_template,
            )
        clock = clock or patterntools.Clock.get_default_clock()
        assert isinstance(clock, patterntools.Clock)
        self._server = server or servertools.Server.get_default_server()
        self._clock = clock
        self._iterator = None
        self._uuids = {}
        self._call_count = 0

    ### SPECIAL METHODS ###

    def __call__(self, execution_time, scheduled_time, communicate=True):
        if self._iterator is None:
            self._iterator = self._iterate_outer(
                pattern=self._pattern,
                server=self._server,
                timestamp=scheduled_time,
                uuids=self._uuids,
                )
        event_products, delta = next(self._iterator)
        node_free_ids, requests = set(), []
        for event_product in event_products:
            if not event_product.event:
                continue
            for request in event_product.requests:
                if isinstance(request, requesttools.NodeFreeRequest):
                    node_free_ids.update(request.node_ids)
                else:
                    requests.append(request)
            if event_product.is_stop:
                proxies = self._uuids[event_product.uuid]
                for proxy_id, proxy in proxies.items():
                    if isinstance(proxy, (
                        servertools.Bus,
                        servertools.BusGroup,
                        )):
                        allocator = servertools.Bus._get_allocator(
                            calculation_rate=proxy.calculation_rate,
                            server=self._server,
                            )
                        allocator.free(proxy_id)
                self._uuids.pop(event_product.uuid)
        if node_free_ids:
            node_free_ids = sorted(node_free_ids)
            request = requesttools.NodeFreeRequest(node_ids=node_free_ids)
            requests.append(request)
        consolidated_bundle = requesttools.RequestBundle(
            timestamp=scheduled_time,
            contents=requests,
            )
        if communicate:
            osc_bundle = consolidated_bundle.to_osc_bundle()
            osc_bundle = new(
                osc_bundle,
                timestamp=osc_bundle.timestamp + self._server.latency,
                )
            self._server.send_message(osc_bundle)
            return delta
        return consolidated_bundle, delta

    ### PRIVATE METHODS ###

    def _collect_stop_requests(self):
        requests = []
        gated_node_ids = []
        freed_node_ids = []
        for _, node_ids in self._uuids.items():
            for node_id, synth in node_ids.items():
                if synth.synthdef.has_gate:
                    gated_node_ids.append(node_id)
                else:
                    freed_node_ids.append(node_id)
        if freed_node_ids:
            request = requesttools.NodeFreeRequest(node_ids=sorted(node_ids))
            requests.append(request)
        for node_id in sorted(gated_node_ids):
            request = requesttools.NodeSetRequest(
                node_id=node_id,
                gate=0,
                )
            requests.append(request)
        if not requests:
            return
        return requesttools.RequestBundle(contents=requests)

    @staticmethod
    def _iterate_inner(pattern, server, timestamp, uuids):
        queue = PriorityQueue()
        for index, event in enumerate(pattern):
            for event_product in event._perform_realtime(
                index=index,
                server=server,
                timestamp=timestamp,
                uuids=uuids,
                ):
                queue.put(event_product)
            while not queue.empty():
                event_product = queue.get()
                if event_product.timestamp < (timestamp + event.delta):
                    yield event_product
                else:
                    queue.put(event_product)
                    break
            timestamp += event.delta
        while not queue.empty():
            event_product = queue.get()
            yield event_product
        assert queue.empty()

    @staticmethod
    def _iterate_outer(pattern, server, timestamp, uuids):
        iterator = RealtimeEventPlayer._iterate_inner(
            pattern, server, timestamp, uuids)
        iterator = itertools.groupby(iterator, lambda x: x.timestamp)
        pairs = []
        try:
            timestamp_one, grouper = next(iterator)
        except StopIteration:
            return
        pairs.append((timestamp_one, tuple(grouper)))
        for timestamp_two, grouper in iterator:
            pairs.append((timestamp_two, tuple(grouper)))
            timestamp_one, event_products = pairs.pop(0)
            delta = timestamp_two - timestamp_one
            yield event_products, delta
        _, event_products = pairs.pop()
        yield event_products, None

    ### PUBLIC METHODS ###

    def start(self):
        timestamp = time.time()
        self._uuids.clear()
        self._iterator = self._iterate_outer(
            pattern=self._pattern,
            server=self._server,
            timestamp=timestamp,
            uuids=self._uuids,
            )
        self._clock.schedule(
            self,
            scheduled_time=timestamp,
            absolute=True,
            )

    def stop(self):
        self._clock.cancel(self)
        self._iterator = None
        bundle = self._collect_stop_requests()
        self._uuids.clear()
        if bundle:
            self._server.send_message(bundle.to_osc_bundle())
