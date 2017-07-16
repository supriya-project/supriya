from supriya.tools.systemtools.Enumeration import Enumeration


class SampleFormat(Enumeration):
    """
    An enumeration of soundfile sample formats.

    ::

        >>> from supriya.tools import soundfiletools
        >>> soundfiletools.SampleFormat.INT24
        SampleFormat.INT24

    ::

        >>> soundfiletools.SampleFormat.from_expr('float')
        SampleFormat.FLOAT

    ::

        >>> sample_format = soundfiletools.SampleFormat.INT24
        >>> sample_format.name.lower()
        'int24'

    """

    ### CLASS VARIABLES ###

    INT24 = 0
    ALAW = 1
    DOUBLE = 2
    FLOAT = 3
    INT8 = 4
    INT16 = 5
    INT32 = 6
    MULAW = 7
