import supriya.assets.synthdefs
import supriya.patterns
import supriya.realtime
import supriya.system


class TestCase(supriya.system.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
        self.server = supriya.realtime.Server.get_default_server().boot()
        supriya.assets.synthdefs.default.allocate(self.server)
        self.server.debug_osc = True
        self.server.latency = 0.0

    def tearDown(self):
        self.server.debug_osc = False
        self.server.quit()
        super(TestCase, self).tearDown()
