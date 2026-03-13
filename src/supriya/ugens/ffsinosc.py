from typing import Sequence

from supriya import utils

from ..enums import CalculationRate
from .core import UGen, UGenOperable, UGenRecursiveInput, UGenScalarInput, param, ugen


@ugen(ar=True, kr=True)
class Blip(UGen):
    """
    A band limited impulse generator.

    ::

        >>> blip = supriya.ugens.Blip.ar(
        ...     frequency=440,
        ...     harmonic_count=200,
        ... )
        >>> blip
        <Blip.ar()[0]>
    """

    frequency = param(440.0)
    harmonic_count = param(200.0)


@ugen(ar=True, kr=True)
class FSinOsc(UGen):
    """
    Very fast sine wave generator (2 PowerPC instructions per output sample!) implemented using a ringing filter.

    ::

        >>> fsin_osc = supriya.ugens.FSinOsc.ar(
        ...     frequency=440,
        ...     initial_phase=0,
        ... )
        >>> fsin_osc
        <FSinOsc.ar()[0]>
    """

    frequency = param(440.0)
    initial_phase = param(0.0)


@ugen(ar=True)
class Klank(UGen):
    """
    A bank of resonators.

    ::

        >>> klank = supriya.ugens.Klank.ar(
        ...     amplitudes=None,
        ...     decay_scale=1,
        ...     decay_times=[1, 1, 1, 1],
        ...     frequencies=[200, 671, 1153, 1723],
        ...     frequency_offset=0,
        ...     frequency_scale=1,
        ...     source=supriya.ugens.BrownNoise.ar() * 0.001,
        ... )
        >>> klank
        <Klank.ar()[0]>
    """

    source = param()
    frequency_scale = param(1)
    frequency_offset = param(0)
    decay_scale = param(1)
    specifications = param(unexpanded=True)

    @classmethod
    def ar(
        cls,
        *,
        amplitudes: Sequence[UGenScalarInput] | None = None,
        decay_scale: UGenRecursiveInput = 1,
        decay_times: Sequence[UGenScalarInput] | None = None,
        frequencies: Sequence[UGenScalarInput],
        frequency_offset: UGenRecursiveInput = 0,
        frequency_scale: UGenRecursiveInput = 1,
        source: UGenRecursiveInput,
    ) -> UGenOperable:
        if not frequencies:
            raise ValueError(frequencies)
        if not amplitudes:
            amplitudes = [1.0] * len(frequencies)
        if not decay_times:
            decay_times = [1.0] * len(frequencies)
        specifications: Sequence[UGenScalarInput] = list(
            utils.flatten(utils.zip_cycled(frequencies, amplitudes, decay_times))
        )
        return cls._new_expanded(
            calculation_rate=CalculationRate.AUDIO,
            decay_scale=decay_scale,
            frequency_offset=frequency_offset,
            frequency_scale=frequency_scale,
            source=source,
            specifications=specifications,
        )


@ugen(ar=True, kr=True)
class Pulse(UGen):
    """
    Band limited pulse wave generator with pulse width modulation.

    ::

        >>> pulse = supriya.ugens.Pulse.ar(
        ...     frequency=440,
        ...     width=0.5,
        ... )
        >>> pulse
        <Pulse.ar()[0]>
    """

    frequency = param(440.0)
    width = param(0.5)


@ugen(ar=True, kr=True, is_pure=True)
class Saw(UGen):
    """
    A band-limited sawtooth oscillator unit generator.

    ::

        >>> supriya.ugens.Saw.ar()
        <Saw.ar()[0]>
    """

    frequency = param(440.0)
