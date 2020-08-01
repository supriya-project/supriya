import itertools
from queue import PriorityQueue

from uqbar.objects import new

import supriya.commands
import supriya.realtime
import supriya.system
from supriya.clock import TempoClock


class EventPlayer:

    ### INITIALIZER ###

    def __init__(self, pattern, server=None, event_template=None, clock=None):
        import supriya.patterns
        clock = clock or TempoClock.default()
        if event_template is None:
            event_template = supriya.patterns.NoteEvent()
        elif issubclass(event_template, supriya.patterns.Event):
            event_template = event_template()
        self._clock = clock
        self._cumulative_time = 0
        self._event_template = event_template
        self._iterator = None
        self._pattern = pattern
        self._server = server or supriya.realtime.Server.default()
        self._uuids = {}
        self._event_id = None

    ### SPECIAL METHODS ###

    def __call__(self, current_moment, desired_moment, *args, communicate=True):
        if self._iterator is None:
            self._iterator = self._iterate_outer(
                pattern=self._pattern,
                server=self._server,
                timestamp=desired_moment.seconds,
                uuids=self._uuids,
            )
        event_products, delta = next(self._iterator)
        node_free_ids, requests = set(), []
        for event_product in event_products:
            if not event_product.event:
                continue
            for request in event_product.requests:
                if isinstance(request, supriya.commands.NodeFreeRequest):
                    node_free_ids.update(request.node_ids)
                else:
                    requests.append(request)
            if event_product.is_stop:
                proxies = self._uuids[event_product.uuid]
                for proxy_id, proxy in proxies.items():
                    if isinstance(
                        proxy, (supriya.realtime.Bus, supriya.realtime.BusGroup)
                    ):
                        allocator = supriya.realtime.Bus._get_allocator(
                            calculation_rate=proxy.calculation_rate, server=self._server
                        )
                        allocator.free(proxy_id)
                self._uuids.pop(event_product.uuid)
        if node_free_ids:
            node_free_ids = sorted(node_free_ids)
            request = supriya.commands.NodeFreeRequest(node_ids=node_free_ids)
            requests.append(request)
        consolidated_bundle = supriya.commands.RequestBundle(
            timestamp=desired_moment.seconds, contents=requests
        )
        if communicate:
            osc_bundle = consolidated_bundle.to_osc()
            osc_bundle = new(
                osc_bundle, timestamp=osc_bundle.timestamp + self._server.latency
            )
            self._server.send(osc_bundle)
            return delta
        return consolidated_bundle, delta

    ### PRIVATE METHODS ###

    def _collect_stop_requests(self):
        import supriya.nonrealtime

        requests = []
        gated_node_ids = []
        freed_node_ids = []
        for _, proxy_ids in self._uuids.items():
            for proxy_id, proxy in proxy_ids.items():
                if not isinstance(proxy, supriya.realtime.Node):
                    continue
                if (
                    isinstance(proxy, supriya.nonrealtime.Synth)
                    and proxy.synthdef.has_gate
                ):
                    gated_node_ids.append(proxy_id)
                else:
                    freed_node_ids.append(proxy_id)
        if freed_node_ids:
            request = supriya.commands.NodeFreeRequest(node_ids=sorted(freed_node_ids))
            requests.append(request)
        for node_id in sorted(gated_node_ids):
            request = supriya.commands.NodeSetRequest(node_id=node_id, gate=0)
            requests.append(request)
        if not requests:
            return
        return supriya.commands.RequestBundle(contents=requests)

    @staticmethod
    def _iterate_inner(pattern, server, timestamp, uuids):
        queue = PriorityQueue()
        for index, event in enumerate(pattern):
            for event_product in event._perform_realtime(
                index=(index, 0), server=server, timestamp=timestamp, uuids=uuids
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
        iterator = EventPlayer._iterate_inner(pattern, server, timestamp, uuids)
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

    def notify(self, topic, event):
        if topic == "server-quitting":
            self.stop()

    def start(self):
        if not self._server.is_running:
            return
        self._uuids.clear()
        self._event_id = self._clock.cue(self.__call__)
        if not self._clock.is_running:
            self._clock.start()

    def stop(self):
        self._clock.cancel(self._event_id)
        self._iterator = None
        bundle = self._collect_stop_requests()
        if bundle and self._server.is_running:
            self._server.send(bundle.to_osc())

    ### PUBLIC PROPERTIES ###

    @property
    def event_template(self):
        return self._event_template

    @property
    def pattern(self):
        return self._pattern
