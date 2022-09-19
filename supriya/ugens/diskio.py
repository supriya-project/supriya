from .bases import UGen, param, ugen


@ugen(ar=True, is_multichannel=True, has_done_flag=True)
class DiskIn(UGen):
    """
    Streams in audio from a file.

    ::

        >>> buffer_id = 23
        >>> disk_in = supriya.ugens.DiskIn.ar(
        ...     buffer_id=buffer_id,
        ...     channel_count=2,
        ...     loop=0,
        ... )
        >>> disk_in
        UGenArray({2})

    """

    buffer_id = param(None)
    loop = param(0)


@ugen(ar=True)
class DiskOut(UGen):
    """
    Records to a soundfile to disk.

    ::

        >>> buffer_id = 0
        >>> source = supriya.ugens.SinOsc.ar(frequency=[440, 442])
        >>> disk_out = supriya.ugens.DiskOut.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ... )
        >>> disk_out
        DiskOut.ar()

    """

    buffer_id = param(None)
    source = param(None, unexpanded=True)


@ugen(ar=True, is_multichannel=True, has_done_flag=True)
class VDiskIn(UGen):
    """
    Streams in audio from a file, with variable rate.

    ::

        >>> buffer_id = 23
        >>> vdisk_in = supriya.ugens.VDiskIn.ar(
        ...     buffer_id=buffer_id,
        ...     channel_count=2,
        ...     loop=0,
        ...     rate=1,
        ...     send_id=0,
        ... )
        >>> vdisk_in
        UGenArray({2})

    """

    buffer_id = param(None)
    rate = param(1.0)
    loop = param(0)
    send_id = param(0)
