from supriya import servertools
from supriya import systemtools


class Test(systemtools.TestCase):

    def setUp(self):
        super(systemtools.TestCase, self).setUp()
        self.server = servertools.Server(port=57757)

    def tearDown(self):
        self.server.quit()
        super(systemtools.TestCase, self).tearDown()

    def test_boot(self):
        for i in range(4):
            print(i)
            assert not self.server.is_running
            print('\tbooting...')
            self.server.boot()
            assert self.server.is_running
            print('\tquiting...')
            self.server.quit()
        assert not self.server.is_running

    def test_server_options(self):
        server_options = servertools.ServerOptions(
            memory_size=8192 * 32,
            load_synthdefs=False,
            )
        # Default
        self.server.boot()
        assert isinstance(self.server.server_options, type(server_options))
        assert self.server.server_options.memory_size == 8192
        assert self.server.server_options.load_synthdefs is True
        self.server.quit()
        # With ServerOptions
        self.server.boot(server_options=server_options)
        assert isinstance(self.server.server_options, type(server_options))
        assert self.server.server_options.memory_size == 8192 * 32
        assert self.server.server_options.load_synthdefs is False
        self.server.quit()
        # With **kwargs
        self.server.boot(load_synthdefs=False)
        assert isinstance(self.server.server_options, type(server_options))
        assert self.server.server_options.memory_size == 8192
        assert self.server.server_options.load_synthdefs is False
        self.server.quit()
        # With ServerOptions and **kwargs
        self.server.boot(load_synthdefs=False, server_options=server_options)
        assert isinstance(self.server.server_options, type(server_options))
        assert self.server.server_options.memory_size == 8192 * 32
        assert self.server.server_options.load_synthdefs is False
        self.server.quit()
