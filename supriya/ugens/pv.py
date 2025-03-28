from typing import Any

from ..enums import CalculationRate
from ..typing import Default
from .bufio import LocalBuf
from .core import OutputProxy, UGen, UGenOperable, param, ugen
from .info import BufFrames


@ugen(is_width_first=True)
class PV_ChainUGen(UGen):
    """
    Abstract base class for all phase-vocoder-chain unit generators.
    """

    @property
    def fft_size(self) -> UGenOperable:
        """
        Gets FFT size as UGen input.

        Returns ugen input.
        """
        input_ = self.inputs[0]
        if not isinstance(input_, OutputProxy):
            raise ValueError(input_)
        if not isinstance(input_.ugen, PV_ChainUGen):
            raise ValueError(input_.ugen)
        return input_.ugen.fft_size


@ugen(kr=True, is_width_first=True)
class FFT(PV_ChainUGen):
    """
    A fast Fourier transform.

    ::

        >>> buffer_id = supriya.ugens.LocalBuf.ir(frame_count=2048)
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> fft = supriya.ugens.FFT.kr(
        ...     active=1,
        ...     buffer_id=buffer_id,
        ...     hop=0.5,
        ...     source=source,
        ...     window_size=0,
        ...     window_type=0,
        ... )
        >>> fft
        <FFT.kr()[0]>
    """

    ### CLASS VARIABLES ###

    buffer_id = param(Default())
    source = param()
    hop = param(0.5)
    window_type = param(0)
    active = param(1)
    window_size = param(0)

    ### PRIVATE METHODS ###

    def _postprocess_kwargs(
        self, calculation_rate: CalculationRate, **kwargs
    ) -> tuple[CalculationRate, dict[str, Any]]:
        if isinstance(kwargs["buffer_id"], Default):
            kwargs["buffer_id"] = LocalBuf.ir(frame_count=kwargs["window_size"] or 2048)
        return calculation_rate, kwargs

    ### PUBLIC PROPERTIES ###

    @property
    def fft_size(self) -> UGenOperable:
        """
        Gets FFT size as UGen input.

        Returns ugen input.
        """
        return BufFrames.ir(buffer_id=self.buffer_id)


@ugen(ar=True, kr=True, is_width_first=True)
class IFFT(UGen):
    """
    An inverse fast Fourier transform.

    ::

        >>> pv_chain = supriya.ugens.LocalBuf.ir(frame_count=2048)
        >>> ifft = supriya.ugens.IFFT.ar(
        ...     pv_chain=pv_chain,
        ...     window_size=0,
        ...     window_type=0,
        ... )
        >>> ifft
        <IFFT.ar()[0]>
    """

    pv_chain = param()
    window_type = param(0)
    window_size = param(0)


@ugen(kr=True, is_width_first=True)
class PV_Add(PV_ChainUGen):
    """
    Complex addition.

    ::

        >>> pv_chain_a = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_chain_b = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.LFSaw.ar(),
        ... )
        >>> pv_add = supriya.ugens.PV_Add.kr(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ... )
        >>> pv_add
        <PV_Add.kr()[0]>
    """

    pv_chain_a = param()
    pv_chain_b = param()


@ugen(kr=True, is_width_first=True)
class PV_BinScramble(PV_ChainUGen):
    """
    Scrambles bins.

    ::

        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_bin_scramble = supriya.ugens.PV_BinScramble.kr(
        ...     pv_chain=pv_chain,
        ...     trigger=0,
        ...     width=0.2,
        ...     wipe=0,
        ... )
        >>> pv_bin_scramble
        <PV_BinScramble.kr()[0]>
    """

    pv_chain = param()
    wipe = param(0)
    width = param(0.2)
    trigger = param(0)


@ugen(kr=True, is_width_first=True)
class PV_BinShift(PV_ChainUGen):
    """
    Shifts and stretches bin positions.

    ::

        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_bin_shift = supriya.ugens.PV_BinShift.kr(
        ...     pv_chain=pv_chain,
        ...     interpolate=0,
        ...     shift=0,
        ...     stretch=1,
        ... )
        >>> pv_bin_shift
        <PV_BinShift.kr()[0]>
    """

    pv_chain = param()
    stretch = param(1.0)
    shift = param(0.0)
    interpolate = param(0)


@ugen(kr=True, is_width_first=True)
class PV_BinWipe(PV_ChainUGen):
    """
    Copies low bins from one input and the high bins of the other.

    ::

        >>> pv_chain_a = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_chain_b = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.LFSaw.ar(),
        ... )
        >>> pv_bin_wipe = supriya.ugens.PV_BinWipe.kr(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ...     wipe=0,
        ... )
        >>> pv_bin_wipe
        <PV_BinWipe.kr()[0]>
    """

    pv_chain_a = param()
    pv_chain_b = param()
    wipe = param(0)


@ugen(kr=True, is_width_first=True)
class PV_BrickWall(PV_ChainUGen):
    """
    Zeros bins.

    - If wipe == 0 then there is no effect.
    - If wipe > 0 then it acts like a high pass filter, clearing bins from the bottom
      up.
    - If wipe < 0 then it acts like a low pass filter, clearing bins from the top down.

    ::

        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_brick_wall = supriya.ugens.PV_BrickWall.kr(
        ...     pv_chain=pv_chain,
        ...     wipe=0,
        ... )
        >>> pv_brick_wall
        <PV_BrickWall.kr()[0]>
    """

    pv_chain = param()
    wipe = param(0)


@ugen(kr=True, is_width_first=True)
class PV_ConformalMap(PV_ChainUGen):
    """
    Complex plane attack.

    ::

        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_conformal_map = supriya.ugens.PV_ConformalMap.kr(
        ...     aimag=0,
        ...     areal=0,
        ...     pv_chain=pv_chain,
        ... )
        >>> pv_conformal_map
        <PV_ConformalMap.kr()[0]>
    """

    pv_chain = param()
    areal = param(0)
    aimag = param(0)


@ugen(kr=True, is_width_first=True)
class PV_Conj(PV_ChainUGen):
    """
    Complex conjugate.

    ::

        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_conj = supriya.ugens.PV_Conj.kr(
        ...     pv_chain=pv_chain,
        ... )
        >>> pv_conj
        <PV_Conj.kr()[0]>
    """

    pv_chain = param()


@ugen(kr=True, is_width_first=True)
class PV_Copy(PV_ChainUGen):
    """
    Copies an FFT buffer.

    ::

        >>> pv_chain_a = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_chain_b = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.LFSaw.ar(),
        ... )
        >>> pv_copy = supriya.ugens.PV_Copy.kr(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ... )
        >>> pv_copy
        <PV_Copy.kr()[0]>
    """

    pv_chain_a = param()
    pv_chain_b = param()


@ugen(kr=True, is_width_first=True)
class PV_CopyPhase(PV_ChainUGen):
    """
    Copies magnitudes and phases.

    ::

        >>> pv_chain_a = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_chain_b = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.LFSaw.ar(),
        ... )
        >>> pv_copy_phase = supriya.ugens.PV_CopyPhase.kr(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ... )
        >>> pv_copy_phase
        <PV_CopyPhase.kr()[0]>
    """

    pv_chain_a = param()
    pv_chain_b = param()


@ugen(kr=True, is_width_first=True)
class PV_Diffuser(PV_ChainUGen):
    """
    Shifts phases randomly.

    ::

        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_diffuser = supriya.ugens.PV_Diffuser.kr(
        ...     pv_chain=pv_chain,
        ...     trigger=0,
        ... )
        >>> pv_diffuser
        <PV_Diffuser.kr()[0]>
    """

    pv_chain = param()
    trigger = param(0)


@ugen(kr=True, is_width_first=True)
class PV_Div(PV_ChainUGen):
    """
    Complex division.

    ::

        >>> pv_chain_a = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_chain_b = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.LFSaw.ar(),
        ... )
        >>> pv_div = supriya.ugens.PV_Div.kr(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ... )
        >>> pv_div
        <PV_Div.kr()[0]>
    """

    pv_chain_a = param()
    pv_chain_b = param()


@ugen(kr=True, is_width_first=True)
class PV_HainsworthFoote(PV_ChainUGen):
    """
    A FFT onset detector.

    ::

        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_hainsworth_foote = supriya.ugens.PV_HainsworthFoote.kr(
        ...     pv_chain=pv_chain,
        ...     propf=0,
        ...     proph=0,
        ...     threshold=1,
        ...     waittime=0.04,
        ... )
        >>> pv_hainsworth_foote
        <PV_HainsworthFoote.kr()[0]>
    """

    pv_chain = param()
    proph = param(0)
    propf = param(0)
    threshold = param(1)
    waittime = param(0.04)


@ugen(kr=True, is_width_first=True)
class PV_JensenAndersen(PV_ChainUGen):
    """
    A FFT feature detector for onset detection.

    ::

        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_jensen_andersen = supriya.ugens.PV_JensenAndersen.kr(
        ...     pv_chain=pv_chain,
        ...     prophfc=0.25,
        ...     prophfe=0.25,
        ...     propsc=0.25,
        ...     propsf=0.25,
        ...     threshold=1,
        ...     waittime=0.04,
        ... )
        >>> pv_jensen_andersen
        <PV_JensenAndersen.kr()[0]>
    """

    pv_chain = param()
    propsc = param(0.25)
    prophfe = param(0.25)
    prophfc = param(0.25)
    propsf = param(0.25)
    threshold = param(1)
    waittime = param(0.04)


@ugen(kr=True, is_width_first=True)
class PV_LocalMax(PV_ChainUGen):
    """
    Passes bins which are local maxima.

    ::

        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_local_max = supriya.ugens.PV_LocalMax.kr(
        ...     pv_chain=pv_chain,
        ...     threshold=0,
        ... )
        >>> pv_local_max
        <PV_LocalMax.kr()[0]>
    """

    pv_chain = param()
    threshold = param(0)


@ugen(kr=True, is_width_first=True)
class PV_MagAbove(PV_ChainUGen):
    """
    Passes magnitudes above threshold.

    ::

        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_mag_above = supriya.ugens.PV_MagAbove.kr(
        ...     pv_chain=pv_chain,
        ...     threshold=0,
        ... )
        >>> pv_mag_above
        <PV_MagAbove.kr()[0]>
    """

    pv_chain = param()
    threshold = param(0)


@ugen(kr=True, is_width_first=True)
class PV_MagBelow(PV_ChainUGen):
    """
    Passes magnitudes below threshold.

    ::

        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_mag_below = supriya.ugens.PV_MagBelow.kr(
        ...     pv_chain=pv_chain,
        ...     threshold=0,
        ... )
        >>> pv_mag_below
        <PV_MagBelow.kr()[0]>
    """

    pv_chain = param()
    threshold = param(0)


@ugen(kr=True, is_width_first=True)
class PV_MagClip(PV_ChainUGen):
    """
    Clips magnitudes.

    ::

        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_mag_clip = supriya.ugens.PV_MagClip.kr(
        ...     pv_chain=pv_chain,
        ...     threshold=0,
        ... )
        >>> pv_mag_clip
        <PV_MagClip.kr()[0]>
    """

    pv_chain = param()
    threshold = param(0)


@ugen(kr=True, is_width_first=True)
class PV_MagDiv(PV_ChainUGen):
    """
    Divides magnitudes.

    ::

        >>> pv_chain_a = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_chain_b = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.LFSaw.ar(),
        ... )
        >>> pv_mag_div = supriya.ugens.PV_MagDiv.kr(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ...     zeroed=0.0001,
        ... )
        >>> pv_mag_div
        <PV_MagDiv.kr()[0]>
    """

    pv_chain_a = param()
    pv_chain_b = param()
    zeroed = param(0.0001)


@ugen(kr=True, is_width_first=True)
class PV_MagFreeze(PV_ChainUGen):
    """
    Freezes magnitudes.

    ::

        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_mag_freeze = supriya.ugens.PV_MagFreeze.kr(
        ...     pv_chain=pv_chain,
        ...     freeze=0,
        ... )
        >>> pv_mag_freeze
        <PV_MagFreeze.kr()[0]>
    """

    pv_chain = param()
    freeze = param(0)


@ugen(kr=True, is_width_first=True)
class PV_MagMul(PV_ChainUGen):
    """
    Multiplies FFT magnitudes.

    ::

        >>> pv_chain_a = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_chain_b = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.LFSaw.ar(),
        ... )
        >>> pv_mag_mul = supriya.ugens.PV_MagMul.kr(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ... )
        >>> pv_mag_mul
        <PV_MagMul.kr()[0]>
    """

    pv_chain_a = param()
    pv_chain_b = param()


@ugen(kr=True, is_width_first=True)
class PV_MagNoise(PV_ChainUGen):
    """
    Multiplies magnitudes by noise.

    ::

        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_mag_noise = supriya.ugens.PV_MagNoise.kr(
        ...     pv_chain=pv_chain,
        ... )
        >>> pv_mag_noise
        <PV_MagNoise.kr()[0]>
    """

    pv_chain = param()


@ugen(kr=True, is_width_first=True)
class PV_MagShift(PV_ChainUGen):
    """
    Shifts and stretches magnitude bin position.

    ::

        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_mag_shift = supriya.ugens.PV_MagShift.kr(
        ...     pv_chain=pv_chain,
        ...     shift=0,
        ...     stretch=1,
        ... )
        >>> pv_mag_shift
        <PV_MagShift.kr()[0]>
    """

    pv_chain = param()
    stretch = param(1.0)
    shift = param(0.0)


@ugen(kr=True, is_width_first=True)
class PV_MagSmear(PV_ChainUGen):
    """
    Averages magnitudes across bins.

    ::

        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_mag_smear = supriya.ugens.PV_MagSmear.kr(
        ...     bins=0,
        ...     pv_chain=pv_chain,
        ... )
        >>> pv_mag_smear
        <PV_MagSmear.kr()[0]>
    """

    pv_chain = param()
    bins = param(0)


@ugen(kr=True, is_width_first=True)
class PV_MagSquared(PV_ChainUGen):
    """
    Squares magnitudes.

    ::

        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_mag_squared = supriya.ugens.PV_MagSquared.kr(
        ...     pv_chain=pv_chain,
        ... )
        >>> pv_mag_squared
        <PV_MagSquared.kr()[0]>
    """

    pv_chain = param()


@ugen(kr=True, is_width_first=True)
class PV_Max(PV_ChainUGen):
    """
    Maximum magnitude.

    ::

        >>> pv_chain_a = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_chain_b = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.LFSaw.ar(),
        ... )
        >>> pv_max = supriya.ugens.PV_Max.kr(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ... )
        >>> pv_max
        <PV_Max.kr()[0]>
    """

    pv_chain_a = param()
    pv_chain_b = param()


@ugen(kr=True, is_width_first=True)
class PV_Min(PV_ChainUGen):
    """
    Minimum magnitude.

    ::

        >>> pv_chain_a = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_chain_b = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.LFSaw.ar(),
        ... )
        >>> pv_min = supriya.ugens.PV_Min.kr(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ... )
        >>> pv_min
        <PV_Min.kr()[0]>
    """

    pv_chain_a = param()
    pv_chain_b = param()


@ugen(kr=True, is_width_first=True)
class PV_Mul(PV_ChainUGen):
    """
    Complex multiplication.

    ::

        >>> pv_chain_a = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_chain_b = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.LFSaw.ar(),
        ... )
        >>> pv_mul = supriya.ugens.PV_Mul.kr(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ... )
        >>> pv_mul
        <PV_Mul.kr()[0]>
    """

    pv_chain_a = param()
    pv_chain_b = param()


@ugen(kr=True, is_width_first=True)
class PV_PhaseShift(PV_ChainUGen):
    """
    Shifts phase.

    ::

        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> shift = supriya.ugens.LFNoise2.kr(frequency=1).scale(-1, 1, -180, 180)
        >>> pv_phase_shift = supriya.ugens.PV_PhaseShift.kr(
        ...     pv_chain=pv_chain,
        ...     integrate=0,
        ...     shift=shift,
        ... )
        >>> pv_phase_shift
        <PV_PhaseShift.kr()[0]>
    """

    pv_chain = param()
    shift = param()
    integrate = param(0)


@ugen(kr=True, is_width_first=True)
class PV_PhaseShift270(PV_ChainUGen):
    """
    Shifts phase by 270 degrees.

    ::

        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_phase_shift_270 = supriya.ugens.PV_PhaseShift270.kr(
        ...     pv_chain=pv_chain,
        ... )
        >>> pv_phase_shift_270
        <PV_PhaseShift270.kr()[0]>
    """

    pv_chain = param()


@ugen(kr=True, is_width_first=True)
class PV_PhaseShift90(PV_ChainUGen):
    """
    Shifts phase by 90 degrees.

    ::

        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_phase_shift_90 = supriya.ugens.PV_PhaseShift90.kr(
        ...     pv_chain=pv_chain,
        ... )
        >>> pv_phase_shift_90
        <PV_PhaseShift90.kr()[0]>
    """

    pv_chain = param()


@ugen(kr=True, is_width_first=True)
class PV_RandComb(PV_ChainUGen):
    """
    Passes random bins.

    ::

        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_rand_comb = supriya.ugens.PV_RandComb.kr(
        ...     pv_chain=pv_chain,
        ...     trigger=0,
        ...     wipe=0,
        ... )
        >>> pv_rand_comb
        <PV_RandComb.kr()[0]>
    """

    pv_chain = param()
    wipe = param(0)
    trigger = param(0)


@ugen(kr=True, is_width_first=True)
class PV_RandWipe(PV_ChainUGen):
    """
    Crossfades in random bin order.

    ::

        >>> pv_chain_a = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_chain_b = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.LFSaw.ar(),
        ... )
        >>> pv_rand_wipe = supriya.ugens.PV_RandWipe.kr(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ...     trigger=0,
        ...     wipe=0,
        ... )
        >>> pv_rand_wipe
        <PV_RandWipe.kr()[0]>
    """

    pv_chain_a = param()
    pv_chain_b = param()
    wipe = param(0)
    trigger = param(0)


@ugen(kr=True, is_width_first=True)
class PV_RectComb(PV_ChainUGen):
    """
    Makes gaps in the spectrum.

    ::

        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_rect_comb = supriya.ugens.PV_RectComb.kr(
        ...     pv_chain=pv_chain,
        ...     num_teeth=0,
        ...     phase=0,
        ...     width=0.5,
        ... )
        >>> pv_rect_comb
        <PV_RectComb.kr()[0]>
    """

    pv_chain = param()
    num_teeth = param(0)
    phase = param(0)
    width = param(0.5)


@ugen(kr=True, is_width_first=True)
class PV_RectComb2(PV_ChainUGen):
    """
    Makes gaps in the spectrum.

    ::

        >>> pv_chain_a = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_chain_b = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.LFSaw.ar(),
        ... )
        >>> pv_rect_comb_2 = supriya.ugens.PV_RectComb2.kr(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ...     num_teeth=0,
        ...     phase=0,
        ...     width=0.5,
        ... )
        >>> pv_rect_comb_2
        <PV_RectComb2.kr()[0]>
    """

    pv_chain_a = param()
    pv_chain_b = param()
    num_teeth = param(0)
    phase = param(0)
    width = param(0.5)


@ugen(ar=True, kr=True)
class RunningSum(UGen):
    """
    Tracks running sum over ``n`` frames.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> running_sum = supriya.ugens.RunningSum.ar(
        ...     sample_count=40,
        ...     source=source,
        ... )
        >>> running_sum
        <RunningSum.ar()[0]>
    """

    source = param()
    sample_count = param(40)
