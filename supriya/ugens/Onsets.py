from uqbar.enums import IntEnumeration
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class Onsets(UGen):
    """
    An onset detector.

    ::

        >>> source = supriya.ugens.SoundIn.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT(source=source)
        >>> onsets = supriya.ugens.Onsets.kr(
        ...     pv_chain=pv_chain,
        ...     floor=0.1,
        ...     medianspan=11,
        ...     mingap=10,
        ...     odftype=supriya.ugens.Onsets.ODFType.RCOMPLEX,
        ...     rawodf=0,
        ...     relaxtime=1,
        ...     threshold=0.5,
        ...     whtype=1,
        ...     )
        >>> onsets
        Onsets.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Machine Listening UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        'threshold',
        'odftype',
        'relaxtime',
        'floor',
        'mingap',
        'medianspan',
        'whtype',
        'rawodf',
        )

    _valid_calculation_rates = (
        CalculationRate.CONTROL,
        )


    class ODFType(IntEnumeration):
        POWER = 0
        MAGSUM = 1
        COMPLEX = 2
        RCOMPLEX = 3
        PHASE = 4
        WPHASE = 5
        MKL = 6

    ### INITIALIZER ###

    def __init__(
        self,
        pv_chain=None,
        floor=0.1,
        medianspan=11,
        mingap=10,
        odftype=ODFType.RCOMPLEX,
        rawodf=0,
        relaxtime=1,
        threshold=0.5,
        whtype=1,
        ):
        UGen.__init__(
            self,
            calculation_rate=CalculationRate.CONTROL,
            pv_chain=pv_chain,
            floor=floor,
            medianspan=medianspan,
            mingap=mingap,
            odftype=odftype,
            rawodf=rawodf,
            relaxtime=relaxtime,
            threshold=threshold,
            whtype=whtype,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        pv_chain=None,
        floor=0.1,
        medianspan=11,
        mingap=10,
        odftype=ODFType.RCOMPLEX,
        rawodf=0,
        relaxtime=1,
        threshold=0.5,
        whtype=1,
        ):
        """
        Constructs a control-rate Onsets.

        ::

            >>> source = supriya.ugens.SoundIn.ar(bus=0)
            >>> pv_chain = supriya.ugens.FFT(source=source)
            >>> onsets = supriya.ugens.Onsets.kr(
            ...     pv_chain=pv_chain,
            ...     floor=0.1,
            ...     medianspan=11,
            ...     mingap=10,
            ...     odftype=supriya.ugens.Onsets.ODFType.RCOMPLEX,
            ...     rawodf=0,
            ...     relaxtime=1,
            ...     threshold=0.5,
            ...     whtype=1,
            ...     )
            >>> onsets
            Onsets.kr()

        Returns ugen graph.
        """
        ugen = cls._new_expanded(
            pv_chain=pv_chain,
            floor=floor,
            medianspan=medianspan,
            mingap=mingap,
            odftype=odftype,
            rawodf=rawodf,
            relaxtime=relaxtime,
            threshold=threshold,
            whtype=whtype,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        """
        Gets `pv_chain` input of Onsets.

        ::

            >>> source = supriya.ugens.SoundIn.ar(bus=0)
            >>> pv_chain = supriya.ugens.FFT(source=source)
            >>> onsets = supriya.ugens.Onsets.kr(
            ...     pv_chain=pv_chain,
            ...     floor=0.1,
            ...     medianspan=11,
            ...     mingap=10,
            ...     odftype=supriya.ugens.Onsets.ODFType.RCOMPLEX,
            ...     rawodf=0,
            ...     relaxtime=1,
            ...     threshold=0.5,
            ...     whtype=1,
            ...     )
            >>> onsets.pv_chain
            FFT.kr()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]

    @property
    def floor(self):
        """
        Gets `floor` input of Onsets.

        ::

            >>> source = supriya.ugens.SoundIn.ar(bus=0)
            >>> pv_chain = supriya.ugens.FFT(source=source)
            >>> onsets = supriya.ugens.Onsets.kr(
            ...     pv_chain=pv_chain,
            ...     floor=0.1,
            ...     medianspan=11,
            ...     mingap=10,
            ...     odftype=supriya.ugens.Onsets.ODFType.RCOMPLEX,
            ...     rawodf=0,
            ...     relaxtime=1,
            ...     threshold=0.5,
            ...     whtype=1,
            ...     )
            >>> onsets.floor
            0.1

        Returns ugen input.
        """
        index = self._ordered_input_names.index('floor')
        return self._inputs[index]

    @property
    def medianspan(self):
        """
        Gets `medianspan` input of Onsets.

        ::

            >>> source = supriya.ugens.SoundIn.ar(bus=0)
            >>> pv_chain = supriya.ugens.FFT(source=source)
            >>> onsets = supriya.ugens.Onsets.kr(
            ...     pv_chain=pv_chain,
            ...     floor=0.1,
            ...     medianspan=11,
            ...     mingap=10,
            ...     odftype=supriya.ugens.Onsets.ODFType.RCOMPLEX,
            ...     rawodf=0,
            ...     relaxtime=1,
            ...     threshold=0.5,
            ...     whtype=1,
            ...     )
            >>> onsets.medianspan
            11.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('medianspan')
        return self._inputs[index]

    @property
    def mingap(self):
        """
        Gets `mingap` input of Onsets.

        ::

            >>> source = supriya.ugens.SoundIn.ar(bus=0)
            >>> pv_chain = supriya.ugens.FFT(source=source)
            >>> onsets = supriya.ugens.Onsets.kr(
            ...     pv_chain=pv_chain,
            ...     floor=0.1,
            ...     medianspan=11,
            ...     mingap=10,
            ...     odftype=supriya.ugens.Onsets.ODFType.RCOMPLEX,
            ...     rawodf=0,
            ...     relaxtime=1,
            ...     threshold=0.5,
            ...     whtype=1,
            ...     )
            >>> onsets.mingap
            10.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('mingap')
        return self._inputs[index]

    @property
    def odftype(self):
        """
        Gets `odftype` input of Onsets.

        ::

            >>> source = supriya.ugens.SoundIn.ar(bus=0)
            >>> pv_chain = supriya.ugens.FFT(source=source)
            >>> onsets = supriya.ugens.Onsets.kr(
            ...     pv_chain=pv_chain,
            ...     floor=0.1,
            ...     medianspan=11,
            ...     mingap=10,
            ...     odftype=supriya.ugens.Onsets.ODFType.RCOMPLEX,
            ...     rawodf=0,
            ...     relaxtime=1,
            ...     threshold=0.5,
            ...     whtype=1,
            ...     )
            >>> onsets.odftype
            3.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('odftype')
        return self._inputs[index]

    @property
    def rawodf(self):
        """
        Gets `rawodf` input of Onsets.

        ::

            >>> source = supriya.ugens.SoundIn.ar(bus=0)
            >>> pv_chain = supriya.ugens.FFT(source=source)
            >>> onsets = supriya.ugens.Onsets.kr(
            ...     pv_chain=pv_chain,
            ...     floor=0.1,
            ...     medianspan=11,
            ...     mingap=10,
            ...     odftype=supriya.ugens.Onsets.ODFType.RCOMPLEX,
            ...     rawodf=0,
            ...     relaxtime=1,
            ...     threshold=0.5,
            ...     whtype=1,
            ...     )
            >>> onsets.rawodf
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('rawodf')
        return self._inputs[index]

    @property
    def relaxtime(self):
        """
        Gets `relaxtime` input of Onsets.

        ::

            >>> source = supriya.ugens.SoundIn.ar(bus=0)
            >>> pv_chain = supriya.ugens.FFT(source=source)
            >>> onsets = supriya.ugens.Onsets.kr(
            ...     pv_chain=pv_chain,
            ...     floor=0.1,
            ...     medianspan=11,
            ...     mingap=10,
            ...     odftype=supriya.ugens.Onsets.ODFType.RCOMPLEX,
            ...     rawodf=0,
            ...     relaxtime=1,
            ...     threshold=0.5,
            ...     whtype=1,
            ...     )
            >>> onsets.relaxtime
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('relaxtime')
        return self._inputs[index]

    @property
    def threshold(self):
        """
        Gets `threshold` input of Onsets.

        ::

            >>> source = supriya.ugens.SoundIn.ar(bus=0)
            >>> pv_chain = supriya.ugens.FFT(source=source)
            >>> onsets = supriya.ugens.Onsets.kr(
            ...     pv_chain=pv_chain,
            ...     floor=0.1,
            ...     medianspan=11,
            ...     mingap=10,
            ...     odftype=supriya.ugens.Onsets.ODFType.RCOMPLEX,
            ...     rawodf=0,
            ...     relaxtime=1,
            ...     threshold=0.5,
            ...     whtype=1,
            ...     )
            >>> onsets.threshold
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('threshold')
        return self._inputs[index]

    @property
    def whtype(self):
        """
        Gets `whtype` input of Onsets.

        ::

            >>> source = supriya.ugens.SoundIn.ar(bus=0)
            >>> pv_chain = supriya.ugens.FFT(source=source)
            >>> onsets = supriya.ugens.Onsets.kr(
            ...     pv_chain=pv_chain,
            ...     floor=0.1,
            ...     medianspan=11,
            ...     mingap=10,
            ...     odftype=supriya.ugens.Onsets.ODFType.RCOMPLEX,
            ...     rawodf=0,
            ...     relaxtime=1,
            ...     threshold=0.5,
            ...     whtype=1,
            ...     )
            >>> onsets.whtype
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('whtype')
        return self._inputs[index]
