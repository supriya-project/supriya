from supriya.system.Enumeration import Enumeration


class HeaderFormat(Enumeration):
    """
    An enumeration of soundfile header formats.

    ::

        >>> import supriya.soundfiles
        >>> supriya.soundfiles.HeaderFormat.AIFF
        HeaderFormat.AIFF

    ::

        >>> supriya.soundfiles.HeaderFormat.from_expr('wav')
        HeaderFormat.WAV

    ::

        >>> header_format = supriya.soundfiles.HeaderFormat.from_expr('wav')
        >>> header_format.name.lower()
        'wav'

    """

    ### CLASS VARIABLES ###

    AIFF = 0
    IRCAM = 1
    NEXT = 2
    RAW = 3
    WAV = 4
