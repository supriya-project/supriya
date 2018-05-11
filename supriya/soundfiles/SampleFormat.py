from uqbar.enums import IntEnumeration


class SampleFormat(IntEnumeration):
    """
    An enumeration of soundfile sample formats.

    ::

        >>> import supriya.soundfiles
        >>> supriya.soundfiles.SampleFormat.INT24
        SampleFormat.INT24

    ::

        >>> supriya.soundfiles.SampleFormat.from_expr('float')
        SampleFormat.FLOAT

    ::

        >>> sample_format = supriya.soundfiles.SampleFormat.INT24
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
