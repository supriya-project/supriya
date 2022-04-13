import collections

from supriya import CalculationRate
from supriya.synthdefs import UGen, WidthFirstUGen


class PV_ChainUGen(WidthFirstUGen):
    """
    Abstract base class for all phase-vocoder-chain unit generators.
    """

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        calculation_rate = CalculationRate.CONTROL
        WidthFirstUGen.__init__(self, calculation_rate=calculation_rate, **kwargs)

    ### PUBLIC PROPERTIES ###

    @property
    def fft_size(self):
        """
        Gets FFT size as UGen input.

        Returns ugen input.
        """
        return self.pv_chain.fft_size


class FFT(PV_ChainUGen):
    """
    A fast Fourier transform.

    ::

        >>> buffer_id = supriya.ugens.LocalBuf(2048)
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> fft = supriya.ugens.FFT(
        ...     active=1,
        ...     buffer_id=buffer_id,
        ...     hop=0.5,
        ...     source=source,
        ...     window_size=0,
        ...     window_type=0,
        ... )
        >>> fft
        FFT.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [
            ("buffer_id", None),
            ("source", None),
            ("hop", 0.5),
            ("window_type", 0),
            ("active", 1),
            ("window_size", 0),
        ]
    )

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        source=None,
        active=1,
        hop=0.5,
        window_size=0,
        window_type=0,
    ):
        import supriya.ugens

        if buffer_id is None:
            buffer_size = window_size or 2048
            buffer_id = supriya.ugens.LocalBuf(buffer_size)
        PV_ChainUGen.__init__(
            self,
            active=active,
            buffer_id=buffer_id,
            hop=hop,
            source=source,
            window_size=window_size,
            window_type=window_type,
        )

    ### PUBLIC PROPERTIES ###

    @property
    def fft_size(self):
        """
        Gets FFT size as UGen input.

        Returns ugen input.
        """
        import supriya.ugens

        return supriya.ugens.BufFrames.ir(self.buffer_id)


class IFFT(WidthFirstUGen):
    """
    An inverse fast Fourier transform.

    ::

        >>> pv_chain = supriya.ugens.LocalBuf(2048)
        >>> ifft = supriya.ugens.IFFT.ar(
        ...     pv_chain=pv_chain,
        ...     window_size=0,
        ...     window_type=0,
        ... )
        >>> ifft
        IFFT.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("pv_chain", None), ("window_type", 0), ("window_size", 0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class PV_Add(PV_ChainUGen):
    """
    Complex addition.

    ::

        >>> pv_chain_a = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_chain_b = supriya.ugens.FFT(
        ...     source=supriya.ugens.LFSaw.ar(),
        ... )
        >>> pv_add = supriya.ugens.PV_Add.new(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ... )
        >>> pv_add
        PV_Add.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [("pv_chain_a", None), ("pv_chain_b", None)]
    )


class PV_BinScramble(PV_ChainUGen):
    """
    Scrambles bins.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_bin_scramble = supriya.ugens.PV_BinScramble.new(
        ...     pv_chain=pv_chain,
        ...     trigger=0,
        ...     width=0.2,
        ...     wipe=0,
        ... )
        >>> pv_bin_scramble
        PV_BinScramble.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [("pv_chain", None), ("wipe", 0), ("width", 0.2), ("trigger", 0)]
    )


class PV_BinShift(PV_ChainUGen):
    """
    Shifts and stretches bin positions.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_bin_shift = supriya.ugens.PV_BinShift.new(
        ...     pv_chain=pv_chain,
        ...     interpolate=0,
        ...     shift=0,
        ...     stretch=1,
        ... )
        >>> pv_bin_shift
        PV_BinShift.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [("pv_chain", None), ("stretch", 1), ("shift", 0), ("interpolate", 0)]
    )


class PV_BinWipe(PV_ChainUGen):
    """
    Copies low bins from one input and the high bins of the other.

    ::

        >>> pv_chain_a = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_chain_b = supriya.ugens.FFT.new(
        ...     source=supriya.ugens.LFSaw.ar(),
        ... )
        >>> pv_bin_wipe = supriya.ugens.PV_BinWipe.new(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ...     wipe=0,
        ... )
        >>> pv_bin_wipe
        PV_BinWipe.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [("pv_chain_a", None), ("pv_chain_b", None), ("wipe", 0)]
    )


class PV_BrickWall(PV_ChainUGen):
    """
    Zeros bins.

    - If wipe == 0 then there is no effect.
    - If wipe > 0 then it acts like a high pass filter, clearing bins from the
      bottom up.
    - If wipe < 0 then it acts like a low pass filter, clearing bins from the
      top down.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_brick_wall = supriya.ugens.PV_BrickWall.new(
        ...     pv_chain=pv_chain,
        ...     wipe=0,
        ... )
        >>> pv_brick_wall
        PV_BrickWall.kr()

    """

    _ordered_input_names = collections.OrderedDict([("pv_chain", None), ("wipe", 0)])


class PV_ConformalMap(PV_ChainUGen):
    """
    Complex plane attack.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_conformal_map = supriya.ugens.PV_ConformalMap.new(
        ...     aimag=0,
        ...     areal=0,
        ...     pv_chain=pv_chain,
        ... )
        >>> pv_conformal_map
        PV_ConformalMap.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [("pv_chain", None), ("areal", 0), ("aimag", 0)]
    )


class PV_Conj(PV_ChainUGen):
    """
    Complex conjugate.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_conj = supriya.ugens.PV_Conj.new(
        ...     pv_chain=pv_chain,
        ... )
        >>> pv_conj
        PV_Conj.kr()

    """

    _ordered_input_names = collections.OrderedDict([("pv_chain", None)])


class PV_Copy(PV_ChainUGen):
    """
    Copies an FFT buffer.

    ::

        >>> pv_chain_a = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_chain_b = supriya.ugens.FFT(
        ...     source=supriya.ugens.LFSaw.ar(),
        ... )
        >>> pv_copy = supriya.ugens.PV_Copy.new(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ... )
        >>> pv_copy
        PV_Copy.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [("pv_chain_a", None), ("pv_chain_b", None)]
    )


class PV_CopyPhase(PV_ChainUGen):
    """
    Copies magnitudes and phases.

    ::

        >>> pv_chain_a = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_chain_b = supriya.ugens.FFT(
        ...     source=supriya.ugens.LFSaw.ar(),
        ... )
        >>> pv_copy_phase = supriya.ugens.PV_CopyPhase.new(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ... )
        >>> pv_copy_phase
        PV_CopyPhase.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [("pv_chain_a", None), ("pv_chain_b", None)]
    )


class PV_Diffuser(PV_ChainUGen):
    """
    Shifts phases randomly.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_diffuser = supriya.ugens.PV_Diffuser.new(
        ...     pv_chain=pv_chain,
        ...     trigger=0,
        ... )
        >>> pv_diffuser
        PV_Diffuser.kr()

    """

    _ordered_input_names = collections.OrderedDict([("pv_chain", None), ("trigger", 0)])


class PV_Div(PV_ChainUGen):
    """
    Complex division.

    ::

        >>> pv_chain_a = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_chain_b = supriya.ugens.FFT(
        ...     source=supriya.ugens.LFSaw.ar(),
        ... )
        >>> pv_div = supriya.ugens.PV_Div.new(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ... )
        >>> pv_div
        PV_Div.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [("pv_chain_a", None), ("pv_chain_b", None)]
    )


class PV_HainsworthFoote(PV_ChainUGen):
    """
    A FFT onset detector.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_hainsworth_foote = supriya.ugens.PV_HainsworthFoote.new(
        ...     pv_chain=pv_chain,
        ...     propf=0,
        ...     proph=0,
        ...     threshold=1,
        ...     waittime=0.04,
        ... )
        >>> pv_hainsworth_foote
        PV_HainsworthFoote.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [
            ("pv_chain", None),
            ("proph", 0),
            ("propf", 0),
            ("threshold", 1),
            ("waittime", 0.04),
        ]
    )


class PV_JensenAndersen(PV_ChainUGen):
    """
    A FFT feature detector for onset detection.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_jensen_andersen = supriya.ugens.PV_JensenAndersen.new(
        ...     pv_chain=pv_chain,
        ...     prophfc=0.25,
        ...     prophfe=0.25,
        ...     propsc=0.25,
        ...     propsf=0.25,
        ...     threshold=1,
        ...     waittime=0.04,
        ... )
        >>> pv_jensen_andersen
        PV_JensenAndersen.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [
            ("pv_chain", None),
            ("propsc", 0.25),
            ("prophfe", 0.25),
            ("prophfc", 0.25),
            ("propsf", 0.25),
            ("threshold", 1),
            ("waittime", 0.04),
        ]
    )


class PV_LocalMax(PV_ChainUGen):
    """
    Passes bins which are local maxima.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_local_max = supriya.ugens.PV_LocalMax.new(
        ...     pv_chain=pv_chain,
        ...     threshold=0,
        ... )
        >>> pv_local_max
        PV_LocalMax.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [("pv_chain", None), ("threshold", 0)]
    )


class PV_MagAbove(PV_ChainUGen):
    """
    Passes magnitudes above threshold.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_mag_above = supriya.ugens.PV_MagAbove.new(
        ...     pv_chain=pv_chain,
        ...     threshold=0,
        ... )
        >>> pv_mag_above
        PV_MagAbove.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [("pv_chain", None), ("threshold", 0)]
    )


class PV_MagBelow(PV_MagAbove):
    """
    Passes magnitudes below threshold.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_mag_below = supriya.ugens.PV_MagBelow.new(
        ...     pv_chain=pv_chain,
        ...     threshold=0,
        ... )
        >>> pv_mag_below
        PV_MagBelow.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [("pv_chain", None), ("threshold", 0)]
    )


class PV_MagClip(PV_MagAbove):
    """
    Clips magnitudes.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_mag_clip = supriya.ugens.PV_MagClip.new(
        ...     pv_chain=pv_chain,
        ...     threshold=0,
        ... )
        >>> pv_mag_clip
        PV_MagClip.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [("pv_chain", None), ("threshold", 0)]
    )


class PV_MagDiv(PV_ChainUGen):
    """
    Divides magnitudes.

    ::

        >>> pv_chain_a = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_chain_b = supriya.ugens.FFT(
        ...     source=supriya.ugens.LFSaw.ar(),
        ... )
        >>> pv_mag_div = supriya.ugens.PV_MagDiv.new(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ...     zeroed=0.0001,
        ... )
        >>> pv_mag_div
        PV_MagDiv.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [("pv_chain_a", None), ("pv_chain_b", None), ("zeroed", 0.0001)]
    )


class PV_MagFreeze(PV_ChainUGen):
    """
    Freezes magnitudes.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_mag_freeze = supriya.ugens.PV_MagFreeze.new(
        ...     pv_chain=pv_chain,
        ...     freeze=0,
        ... )
        >>> pv_mag_freeze
        PV_MagFreeze.kr()

    """

    _ordered_input_names = collections.OrderedDict([("pv_chain", None), ("freeze", 0)])


class PV_MagMul(PV_ChainUGen):
    """
    Multiplies FFT magnitudes.

    ::

        >>> pv_chain_a = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_chain_b = supriya.ugens.FFT(
        ...     source=supriya.ugens.LFSaw.ar(),
        ... )
        >>> pv_mag_mul = supriya.ugens.PV_MagMul.new(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ... )
        >>> pv_mag_mul
        PV_MagMul.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [("pv_chain_a", None), ("pv_chain_b", None)]
    )


class PV_MagNoise(PV_ChainUGen):
    """
    Multiplies magnitudes by noise.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_mag_noise = supriya.ugens.PV_MagNoise.new(
        ...     pv_chain=pv_chain,
        ... )
        >>> pv_mag_noise
        PV_MagNoise.kr()

    """

    _ordered_input_names = collections.OrderedDict([("pv_chain", None)])


class PV_MagShift(PV_ChainUGen):
    """
    Shifts and stretches magnitude bin position.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_mag_shift = supriya.ugens.PV_MagShift.new(
        ...     pv_chain=pv_chain,
        ...     shift=0,
        ...     stretch=1,
        ... )
        >>> pv_mag_shift
        PV_MagShift.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [("pv_chain", None), ("stretch", 1), ("shift", 0)]
    )


class PV_MagSmear(PV_ChainUGen):
    """
    Averages magnitudes across bins.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_mag_smear = supriya.ugens.PV_MagSmear.new(
        ...     bins=0,
        ...     pv_chain=pv_chain,
        ... )
        >>> pv_mag_smear
        PV_MagSmear.kr()

    """

    _ordered_input_names = collections.OrderedDict([("pv_chain", None), ("bins", 0)])


class PV_MagSquared(PV_ChainUGen):
    """
    Squares magnitudes.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_mag_squared = supriya.ugens.PV_MagSquared.new(
        ...     pv_chain=pv_chain,
        ... )
        >>> pv_mag_squared
        PV_MagSquared.kr()

    """

    _ordered_input_names = collections.OrderedDict([("pv_chain", None)])


class PV_Max(PV_ChainUGen):
    """
    Maximum magnitude.

    ::

        >>> pv_chain_a = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_chain_b = supriya.ugens.FFT(
        ...     source=supriya.ugens.LFSaw.ar(),
        ... )
        >>> pv_max = supriya.ugens.PV_Max.new(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ... )
        >>> pv_max
        PV_Max.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [("pv_chain_a", None), ("pv_chain_b", None)]
    )


class PV_Min(PV_ChainUGen):
    """
    Minimum magnitude.

    ::

        >>> pv_chain_a = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_chain_b = supriya.ugens.FFT(
        ...     source=supriya.ugens.LFSaw.ar(),
        ... )
        >>> pv_min = supriya.ugens.PV_Min.new(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ... )
        >>> pv_min
        PV_Min.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [("pv_chain_a", None), ("pv_chain_b", None)]
    )


class PV_Mul(PV_ChainUGen):
    """
    Complex multiplication.

    ::

        >>> pv_chain_a = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_chain_b = supriya.ugens.FFT(
        ...     source=supriya.ugens.LFSaw.ar(),
        ... )
        >>> pv_mul = supriya.ugens.PV_Mul.new(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ... )
        >>> pv_mul
        PV_Mul.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [("pv_chain_a", None), ("pv_chain_b", None)]
    )


class PV_PhaseShift(PV_ChainUGen):
    """
    Shifts phase.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> shift = supriya.ugens.LFNoise2.kr(1).scale(-1, 1, -180, 180)
        >>> pv_phase_shift = supriya.ugens.PV_PhaseShift.new(
        ...     pv_chain=pv_chain,
        ...     integrate=0,
        ...     shift=shift,
        ... )
        >>> pv_phase_shift
        PV_PhaseShift.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [("pv_chain", None), ("shift", None), ("integrate", 0)]
    )


class PV_PhaseShift270(PV_ChainUGen):
    """
    Shifts phase by 270 degrees.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_phase_shift_270 = supriya.ugens.PV_PhaseShift270.new(
        ...     pv_chain=pv_chain,
        ... )
        >>> pv_phase_shift_270
        PV_PhaseShift270.kr()

    """

    _ordered_input_names = collections.OrderedDict([("pv_chain", None)])


class PV_PhaseShift90(PV_ChainUGen):
    """
    Shifts phase by 90 degrees.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_phase_shift_90 = supriya.ugens.PV_PhaseShift90.new(
        ...     pv_chain=pv_chain,
        ... )
        >>> pv_phase_shift_90
        PV_PhaseShift90.kr()

    """

    _ordered_input_names = collections.OrderedDict([("pv_chain", None)])


class PV_RandComb(PV_ChainUGen):
    """
    Passes random bins.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_rand_comb = supriya.ugens.PV_RandComb.new(
        ...     pv_chain=pv_chain,
        ...     trigger=0,
        ...     wipe=0,
        ... )
        >>> pv_rand_comb
        PV_RandComb.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [("pv_chain", None), ("wipe", 0), ("trigger", 0)]
    )


class PV_RandWipe(PV_ChainUGen):
    """
    Crossfades in random bin order.

    ::

        >>> pv_chain_a = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_chain_b = supriya.ugens.FFT(
        ...     source=supriya.ugens.LFSaw.ar(),
        ... )
        >>> pv_rand_wipe = supriya.ugens.PV_RandWipe.new(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ...     trigger=0,
        ...     wipe=0,
        ... )
        >>> pv_rand_wipe
        PV_RandWipe.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [("pv_chain_a", None), ("pv_chain_b", None), ("wipe", 0), ("trigger", 0)]
    )


class PV_RectComb(PV_ChainUGen):
    """
    Makes gaps in the spectrum.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_rect_comb = supriya.ugens.PV_RectComb.new(
        ...     pv_chain=pv_chain,
        ...     num_teeth=0,
        ...     phase=0,
        ...     width=0.5,
        ... )
        >>> pv_rect_comb
        PV_RectComb.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [("pv_chain", None), ("num_teeth", 0), ("phase", 0), ("width", 0.5)]
    )


class PV_RectComb2(PV_ChainUGen):
    """
    Makes gaps in the spectrum.

    ::

        >>> pv_chain_a = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_chain_b = supriya.ugens.FFT(
        ...     source=supriya.ugens.LFSaw.ar(),
        ... )
        >>> pv_rect_comb_2 = supriya.ugens.PV_RectComb2.new(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ...     num_teeth=0,
        ...     phase=0,
        ...     width=0.5,
        ... )
        >>> pv_rect_comb_2
        PV_RectComb2.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [
            ("pv_chain_a", None),
            ("pv_chain_b", None),
            ("num_teeth", 0),
            ("phase", 0),
            ("width", 0.5),
        ]
    )


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
        RunningSum.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("sample_count", 40)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
