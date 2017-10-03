import supriya


class TestCase(supriya.systemtools.TestCase):

    def setUp(self):
        super(supriya.systemtools.TestCase, self).setUp()
        self.server = supriya.Server.get_default_server()

    def tearDown(self):
        self.server.quit()
        super(supriya.systemtools.TestCase, self).tearDown()

    def test_01(self):
        supriya.livetools.ServerTUI(self.server)
