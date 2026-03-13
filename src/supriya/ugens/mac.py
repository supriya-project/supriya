from ..enums import SignalRange
from .core import UGen, param, ugen


@ugen(kr=True, signal_range=SignalRange.UNIPOLAR)
class KeyState(UGen):
    keycode = param(0.0)
    minimum = param(0.0)
    maximum = param(1.0)
    lag = param(0.2)


@ugen(kr=True, signal_range=SignalRange.UNIPOLAR)
class MouseButton(UGen):
    """
    A mouse-button tracker.

    ::

        >>> supriya.ugens.MouseButton.kr()
        <MouseButton.kr()[0]>
    """

    minimum = param(0.0)
    maximum = param(1.0)
    lag = param(0.2)


@ugen(kr=True, signal_range=SignalRange.UNIPOLAR)
class MouseX(UGen):
    """
    A mouse cursor tracker.

    MouseX tracks the y-axis of the mouse cursor position.

    ::

        >>> supriya.ugens.MouseX.kr()
        <MouseX.kr()[0]>
    """

    minimum = param(0.0)
    maximum = param(1.0)
    warp = param(0.0)
    lag = param(0.2)


@ugen(kr=True, signal_range=SignalRange.UNIPOLAR)
class MouseY(UGen):
    """
    A mouse cursor tracker.

    MouseY tracks the y-axis of the mouse cursor position.

    ::

        >>> supriya.ugens.MouseY.kr()
        <MouseY.kr()[0]>
    """

    minimum = param(0.0)
    maximum = param(1.0)
    warp = param(0.0)
    lag = param(0.2)
