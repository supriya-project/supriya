# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Filter import Filter


class VarLag(Filter):
    r"""

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> var_lag = ugentools.VarLag.ar(
        ...     curvature=0,
        ...     source=source,
        ...     start=start,
        ...     time=0.1,
        ...     warp=5,
        ...     )
        >>> var_lag
        VarLag.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'time',
        'curvature',
        'warp',
        'start',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        curvature=0,
        source=None,
        start=None,
        time=0.1,
        warp=5,
        ):
        Filter.__init__(
            self,
            calculation_rate=calculation_rate,
            curvature=curvature,
            source=source,
            start=start,
            time=time,
            warp=warp,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        curvature=0,
        source=None,
        start=None,
        time=0.1,
        warp=5,
        ):
        r"""
        Constructs an audio-rate VarLag.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> var_lag = ugentools.VarLag.ar(
            ...     curvature=0,
            ...     source=source,
            ...     start=start,
            ...     time=0.1,
            ...     warp=5,
            ...     )
            >>> var_lag
            VarLag.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            curvature=curvature,
            source=source,
            start=start,
            time=time,
            warp=warp,
            )
        return ugen

    # def coeffs(): ...

    @classmethod
    def kr(
        cls,
        curvature=0,
        source=None,
        start=None,
        time=0.1,
        warp=5,
        ):
        r"""
        Constructs a control-rate VarLag.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> var_lag = ugentools.VarLag.kr(
            ...     curvature=0,
            ...     source=source,
            ...     start=start,
            ...     time=0.1,
            ...     warp=5,
            ...     )
            >>> var_lag
            VarLag.kr()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            curvature=curvature,
            source=source,
            start=start,
            time=time,
            warp=warp,
            )
        return ugen

    # def magResponse(): ...

    # def magResponse2(): ...

    # def magResponse5(): ...

    # def magResponseN(): ...

    # def new1(): ...

    # def scopeResponse(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def curvature(self):
        r"""
        Gets `curvature` input of VarLag.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> var_lag = ugentools.VarLag.ar(
            ...     curvature=0,
            ...     source=source,
            ...     start=start,
            ...     time=0.1,
            ...     warp=5,
            ...     )
            >>> var_lag.curvature
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('curvature')
        return self._inputs[index]

    @property
    def source(self):
        r"""
        Gets `source` input of VarLag.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> var_lag = ugentools.VarLag.ar(
            ...     curvature=0,
            ...     source=source,
            ...     start=start,
            ...     time=0.1,
            ...     warp=5,
            ...     )
            >>> var_lag.source
            OutputProxy(
                source=In(
                    bus=0.0,
                    calculation_rate=CalculationRate.AUDIO,
                    channel_count=1
                    ),
                output_index=0
                )

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def start(self):
        r"""
        Gets `start` input of VarLag.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> var_lag = ugentools.VarLag.ar(
            ...     curvature=0,
            ...     source=source,
            ...     start=start,
            ...     time=0.1,
            ...     warp=5,
            ...     )
            >>> var_lag.start

        Returns ugen input.
        """
        index = self._ordered_input_names.index('start')
        return self._inputs[index]

    @property
    def time(self):
        r"""
        Gets `time` input of VarLag.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> var_lag = ugentools.VarLag.ar(
            ...     curvature=0,
            ...     source=source,
            ...     start=start,
            ...     time=0.1,
            ...     warp=5,
            ...     )
            >>> var_lag.time
            0.1

        Returns ugen input.
        """
        index = self._ordered_input_names.index('time')
        return self._inputs[index]

    @property
    def warp(self):
        r"""
        Gets `warp` input of VarLag.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> var_lag = ugentools.VarLag.ar(
            ...     curvature=0,
            ...     source=source,
            ...     start=start,
            ...     time=0.1,
            ...     warp=5,
            ...     )
            >>> var_lag.warp
            5.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('warp')
        return self._inputs[index]
