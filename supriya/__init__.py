# -*- encoding: utf -*-

import sys
if sys.version_info[0] == 3:
    from supriya.tools import *
    from supriya.tools.servertools import AddAction
    from supriya.tools.servertools import Buffer
    from supriya.tools.servertools import BufferGroup
    from supriya.tools.servertools import Bus
    from supriya.tools.servertools import BusGroup
    from supriya.tools.servertools import Group
    from supriya.tools.servertools import Server
    from supriya.tools.servertools import Synth
    from supriya.tools.synthdeftools import Op
    from supriya.tools.synthdeftools import Rate
    from supriya.tools.synthdeftools import SynthDef
    from supriya.tools.synthdeftools import SynthDefBuilder
    from supriya import synthdefs
else:
    from .tools import *
    from .tools.servertools import AddAction
    from .tools.servertools import Buffer
    from .tools.servertools import BufferGroup
    from .tools.servertools import Bus
    from .tools.servertools import BusGroup
    from .tools.servertools import Group
    from .tools.servertools import Server
    from .tools.servertools import Synth
    from .tools.synthdeftools import Op
    from .tools.synthdeftools import Rate
    from .tools.synthdeftools import SynthDef
    from .tools.synthdeftools import SynthDefBuilder
    from . import synthdefs
del(sys)