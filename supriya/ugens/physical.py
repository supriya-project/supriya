from .bases import UGen, param, ugen


@ugen(ar=True, kr=True)
class Ball(UGen):
    """
    A bouncing ball physical model.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> ball = supriya.ugens.Ball.ar(
        ...     damping=0,
        ...     friction=0.01,
        ...     gravity=1,
        ...     source=source,
        ... )
        >>> ball
        Ball.ar()

    """

    source = param(None)
    gravity = param(1.0)
    damping = param(0.0)
    friction = param(0.01)


@ugen(ar=True)
class Pluck(UGen):
    """
    A Karplus-String UGen.

    ::

        >>> source = supriya.ugens.WhiteNoise.ar()
        >>> trigger = supriya.ugens.Dust.kr(density=2)
        >>> pluck = supriya.ugens.Pluck.ar(
        ...     coefficient=0.5,
        ...     decay_time=1,
        ...     delay_time=0.2,
        ...     maximum_delay_time=0.2,
        ...     source=source,
        ...     trigger=trigger,
        ... )
        >>> pluck
        Pluck.ar()

    """

    source = param(None)
    trigger = param(None)
    maximum_delay_time = param(0.2)
    delay_time = param(0.2)
    decay_time = param(1)
    coefficient = param(0.5)


@ugen(ar=True, kr=True)
class Spring(UGen):
    """
    A resonating spring physical model.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> spring = supriya.ugens.Spring.ar(
        ...     damping=0,
        ...     source=source,
        ...     spring=1,
        ... )
        >>> spring
        Spring.ar()

    """

    source = param(None)
    spring = param(1.0)
    damping = param(0.0)


@ugen(ar=True, kr=True)
class TBall(UGen):
    """
    A bouncing object physical model.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> tball = supriya.ugens.TBall.ar(
        ...     damping=0,
        ...     friction=0.01,
        ...     gravity=10,
        ...     source=source,
        ... )
        >>> tball
        TBall.ar()

    """

    source = param(None)
    gravity = param(10.0)
    damping = param(0.0)
    friction = param(0.01)
