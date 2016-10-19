# -*- encoding: utf-8 -*-
import os
import unittest
from supriya import servertools


@unittest.skipIf(os.environ.get('TRAVIS') == 'true', 'No Scsynth on Travis-CI')
class Test(unittest.TestCase):

    def setUp(self):
        self.server = servertools.Server().boot()

    def tearDown(self):
        self.server.quit()

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