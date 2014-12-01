#! /usr/bin/env python
# -*- encoding: utf-8 -*-
from supriya.tools import servertools
from supriya.tools import webguitools


if __name__ == '__main__':
    server = servertools.Server().boot()
    server.meters.allocate()
    web_server = webguitools.WebServer(server)
    web_server.start()