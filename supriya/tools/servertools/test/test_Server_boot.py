from supriya import *


def test_Server_boot():

    server = servertools.Server(port=57757)
    server.boot()
    server.quit()
