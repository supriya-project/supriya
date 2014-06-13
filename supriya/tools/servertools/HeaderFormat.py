# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.Enumeration import Enumeration


class HeaderFormat(Enumeration):
    r'''An enumeration of soundfile header formats.

    ::

        >>> from supriya.tools import servertools
        >>> servertools.HeaderFormat.AIFF
        <HeaderFormat.AIFF: 0>

    ::

        >>> servertools.HeaderFormat.from_expr('wav')
        <HeaderFormat.WAV: 4>

    ::

        >>> header_format = servertools.HeaderFormat.from_expr('wav')
        >>> header_format.name.lower()
        'wav'

    '''

    ### CLASS VARIABLES ###

    AIFF = 0
    IRCAM = 1
    NEXT = 2
    RAW = 3
    WAV = 4
