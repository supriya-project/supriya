import types
import supriya.assets.synthdefs
import supriya.patterns
import supriya.realtime
import supriya.system


class TestCase(supriya.system.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
        self.pseudo_server = types.SimpleNamespace(
            audio_bus_allocator=supriya.realtime.BlockAllocator(),
            control_bus_allocator=supriya.realtime.BlockAllocator(),
            node_id_allocator=supriya.realtime.NodeIdAllocator(),
            )
        self.server = supriya.realtime.Server.get_default_server().boot()
        supriya.assets.synthdefs.default.allocate(self.server)
        self.server.debug_osc = True
        self.server.latency = 0.0

    def build_d_recv_commands(self, synthdefs):
        d_recv_commands = []
        synthdefs = sorted(synthdefs, key=lambda x: x.anonymous_name)
        for synthdef in synthdefs:
            compiled_synthdef = synthdef.compile(use_anonymous_name=True)
            compiled_synthdef = bytearray(compiled_synthdef)
            d_recv_commands.append(['/d_recv', compiled_synthdef])
        return d_recv_commands

    def tearDown(self):
        self.server.debug_osc = False
        self.server.quit()
        super(TestCase, self).tearDown()

    def manual_incommunicado(self, pattern, timestamp=10):
        player = supriya.patterns.RealtimeEventPlayer(
            pattern,
            server=self.pseudo_server,
            )
        lists, deltas, delta = [], [], True
        while delta is not None:
            bundle, delta = player(timestamp, timestamp, communicate=False)
            if delta is not None:
                timestamp += delta
            lists.append(bundle.to_list(True))
            deltas.append(delta)
        return lists, deltas

    def setup_send(self, pattern, iterations):
        events, iterator = [], iter(pattern)
        for i in range(iterations):
            event = next(iterator)
            events.append(event)
        try:
            event = iterator.send(True)
            events.append(event)
            events.extend(iterator)
        except StopIteration:
            pass
        return events
