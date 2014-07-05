# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.Enumeration import Enumeration


class HeaderFormat(Enumeration):
    r'''An enumeration of soundfile header formats.

    ::

        >>> from supriya.tools import soundfiletools
        >>> soundfiletools.HeaderFormat.AIFF
        <HeaderFormat.AIFF: 0>

    ::

        >>> soundfiletools.HeaderFormat.from_expr('wav')
        <HeaderFormat.WAV: 4>

    ::

        >>> header_format = soundfiletools.HeaderFormat.from_expr('wav')
        >>> header_format.name.lower()
        'wav'

    '''

    ### CLASS VARIABLES ###

    AIFF = 0
    IRCAM = 1
    NEXT = 2
    RAW = 3
    WAV = 4
