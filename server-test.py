#! /usr/bin/env python
import time
from supriya import Server, synthdefs
server = Server()
server.debug_subprocess = True
server.boot()
time.sleep(5)
server.debug_osc = True
server.debug_udp = True
synthdefs.default.allocate()
time.sleep(5)
server.quit()
