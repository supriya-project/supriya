from supriya import servertools


def test_Server_boot():

    server = servertools.Server(port=57757)
    for i in range(10):
        assert not server.is_running
        server.boot()
        assert server.is_running
        server.quit()
    assert not server.is_running
