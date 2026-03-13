from .core import UGen, param, ugen


@ugen(ar=True)
class FreeVerb(UGen):
    """
    A FreeVerb reverb unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.FreeVerb.ar(
        ...     source=source,
        ... )
        <FreeVerb.ar()[0]>
    """

    source = param()
    mix = param(0.33)
    room_size = param(0.5)
    damping = param(0.5)
