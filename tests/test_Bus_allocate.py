import supriya.realtime
from supriya import synthdeftools
from supriya import systemtools


class Test(systemtools.TestCase):

    def setUp(self):
        super(systemtools.TestCase, self).setUp()
        self.server = supriya.realtime.Server().boot()

    def tearDown(self):
        self.server.quit()
        super(systemtools.TestCase, self).tearDown()

    def test_01(self):

        control_bus = supriya.realtime.Bus.control()

        assert control_bus.bus_group is None
        assert control_bus.bus_id is None
        assert control_bus.calculation_rate == synthdeftools.CalculationRate.CONTROL
        assert control_bus.server is None
        assert not control_bus.is_allocated

        control_bus.allocate()

        assert control_bus.bus_group is None
        assert control_bus.bus_id == 0
        assert control_bus.calculation_rate == synthdeftools.CalculationRate.CONTROL
        assert control_bus.server is self.server
        assert control_bus.is_allocated
        assert control_bus.map_symbol == 'c0'

        control_bus.free()

        assert control_bus.bus_group is None
        assert control_bus.bus_id is None
        assert control_bus.calculation_rate == synthdeftools.CalculationRate.CONTROL
        assert control_bus.server is None
        assert not control_bus.is_allocated

    def test_02(self):

        audio_bus = supriya.realtime.Bus.audio()

        assert audio_bus.bus_group is None
        assert audio_bus.bus_id is None
        assert audio_bus.calculation_rate == synthdeftools.CalculationRate.AUDIO
        assert audio_bus.server is None
        assert not audio_bus.is_allocated

        audio_bus.allocate()

        assert audio_bus.bus_group is None
        assert audio_bus.bus_id == 16
        assert audio_bus.calculation_rate == synthdeftools.CalculationRate.AUDIO
        assert audio_bus.server is self.server
        assert audio_bus.is_allocated
        assert audio_bus.map_symbol == 'a16'

        audio_bus.free()

        assert audio_bus.bus_group is None
        assert audio_bus.bus_id is None
        assert audio_bus.calculation_rate == synthdeftools.CalculationRate.AUDIO
        assert audio_bus.server is None
        assert not audio_bus.is_allocated

    def test_03(self):

        bus = supriya.realtime.Bus(
            bus_group_or_index=23,
            calculation_rate=synthdeftools.CalculationRate.CONTROL,
            )

        assert bus.bus_id == 23
        assert bus.bus_group is None
        assert not bus.is_allocated
        assert bus.server is None

        bus.allocate()
        self.server.sync()

        assert bus.bus_id == 23
        assert bus.bus_group is None
        assert bus.is_allocated
        assert bus.server is self.server

        bus.free()
        self.server.sync()

        assert bus.bus_id is None
        assert bus.bus_group is None
        assert not bus.is_allocated
        assert bus.server is None

    def test_04(self):

        bus_a = supriya.realtime.Bus.control()
        bus_b = supriya.realtime.Bus.control()
        bus_c = supriya.realtime.Bus.control()
        bus_d = supriya.realtime.Bus.control()

        assert bus_a.bus_id is None
        assert bus_b.bus_id is None
        assert bus_c.bus_id is None
        assert bus_d.bus_id is None
        assert bus_a.server is None
        assert bus_b.server is None
        assert bus_c.server is None
        assert bus_d.server is None

        bus_a.allocate()
        bus_b.allocate()
        bus_c.allocate()
        self.server.sync()

        assert bus_a.bus_id == 0
        assert bus_b.bus_id == 1
        assert bus_c.bus_id == 2
        assert bus_d.bus_id is None
        assert bus_a.server is self.server
        assert bus_b.server is self.server
        assert bus_c.server is self.server
        assert bus_d.server is None

        bus_c.free()
        bus_a.free()
        bus_d.allocate()
        self.server.sync()

        assert bus_a.bus_id is None
        assert bus_b.bus_id == 1
        assert bus_c.bus_id is None
        assert bus_d.bus_id == 0
        assert bus_a.server is None
        assert bus_b.server is self.server
        assert bus_c.server is None
        assert bus_d.server is self.server
