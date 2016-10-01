# -*- encoding: utf-8 -*-
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

    ### SPECIAL METHODS ###

    def __call__(self, execution_time, scheduled_time, communicate=True):
        if self._iterator is None:
            self._iterator = self._iterate_bundles(
                uuids=self._uuids,
                server=self._server,
                timestamp=time.time(),
                )
        group, delta = next(self._iterator)
        node_free_ids, requests = set(), []
        for event_product in group:
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

    def _iterate_grouped_events(self):
        events = []
        for event in self._pattern:
            events.append(event)
            if event.delta:
                yield tuple(events), event.delta
                events[:] = []
        if events:
            yield tuple(events), 0

    def _iterate_bundles(
        self,
        server,
        timestamp,
        uuids,
        ):
        #now = timestamp
        queue = PriorityQueue()
        index = 0
        group, group_delta = None, None
        for event in self._pattern:
            #print('EVENT?', event)
            if group:
                # If we previously had a null delta, check for a next event.
                group_delta = timestamp - group[0].timestamp
                #print('    Catching up...')
                yield group, group_delta
                group, group_delta = None, None
            for event_product in event._perform_realtime(
                index=index,
                server=server,
                timestamp=timestamp,
                uuids=uuids,
                ):
                queue.put(event_product)
            index += 1
            timestamp += event.delta
            if not event.delta:
                continue
            for group, group_delta in self._iterate_queue(queue, timestamp):
                #print('    TS?', group[0].timestamp - now)
                if group_delta:
                    yield group, group_delta
                    group, group_delta = None, None
                #else:
                    #print('    Continuing...')
                # Otherwise store and attempt to pull another event.
        if group:
            #print('    TS?', group[0].timestamp - now)
            yield group, group_delta
        for group, group_delta in self._iterate_queue(queue):
            #print('    TS?', group[0].timestamp - now)
            yield group, group_delta
        assert queue.empty()

    def _iterate_queue(self, queue, until=None):
        group = []
        while not queue.empty():
            event_product = queue.get()
            if until is not None and until <= event_product.timestamp:
                queue.put(event_product)
                break
            if group and event_product.timestamp != group[0].timestamp:
                delta = event_product.timestamp - group[0].timestamp
                yield group, delta
                group.clear()
            group.append(event_product)
        if group:
            delta = None
            if not queue.empty():
                event_product = queue.get()
                delta = event_product.timestamp - group[0].timestamp
                queue.put(event_product)
            yield group, delta

    ### PUBLIC METHODS ###

    def pause(self):
        pass

    def start(self):
        self._uuids.clear()
        self._iterator = self._iterate_bundles(
            uuids=self._uuids,
            server=self._server,
            timestamp=time.time(),
            )
        self._clock.schedule(self)

    def stop(self):
        self._clock.cancel(self)
        self._iterator = None
        bundle = self._collect_stop_requests()
        self._uuids.clear()
        if bundle:
            self._server.send_message(bundle.to_osc_bundle())

    def unpause(self):
        pass
