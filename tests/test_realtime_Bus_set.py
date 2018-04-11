import supriya.realtime
import supriya.system


class Test(supriya.system.TestCase):

    def setUp(self):
        super(supriya.system.TestCase, self).setUp()
        self.server = supriya.realtime.Server().boot()

    def tearDown(self):
        self.server.quit()
        super(supriya.system.TestCase, self).tearDown()

    def test_01(self):

        control_bus = supriya.realtime.Bus.control()
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
