# -*- encoding: utf-8 -*-
import unittest
from supriya import servertools


class Test(unittest.TestCase):

    def setUp(self):
        self.server = servertools.Server(port=57757)

    def tearDown(self):
        self.server.quit()

    def test_Server_boot_01(self):
        for i in range(4):
            assert not self.server.is_running
            self.server.boot()
            assert self.server.is_running
            self.server.quit()
        assert not self.server.is_running