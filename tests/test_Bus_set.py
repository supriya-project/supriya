from supriya import servertools
from supriya import systemtools


class Test(systemtools.TestCase):

    def setUp(self):
        super(systemtools.TestCase, self).setUp()
        self.server = servertools.Server().boot()

    def tearDown(self):
        self.server.quit()
        super(systemtools.TestCase, self).tearDown()

    def test_01(self):

        control_bus = servertools.Bus.control()
        control_bus.allocate()

        result = control_bus.get()
        assert result == 0.0
        assert control_bus.value == result

        control_bus.set(0.5)
        result = control_bus.get()
        assert result == 0.5
        assert control_bus.value == result

        control_bus.set(0.25)
        result = control_bus.get()
        assert result == 0.25
        assert control_bus.value == result
