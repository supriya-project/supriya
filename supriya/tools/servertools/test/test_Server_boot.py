# -*- encoding: utf-8 -*-
import os
import unittest
from supriya import servertools


@unittest.skipIf(os.environ.get('TRAVIS') == 'true', 'No Scsynth on Travis-CI')
class Test(unittest.TestCase):

    def setUp(self):
        self.server = servertools.Server(port=57757)

    def tearDown(self):
        self.server.quit()

    def test_Server_boot_01(self):
        for i in range(4):
            print(i)
            assert not self.server.is_running
            print('\tbooting...')
            self.server.boot()
            assert self.server.is_running
            print('\tquiting...')
            self.server.quit()
        assert not self.server.is_running
