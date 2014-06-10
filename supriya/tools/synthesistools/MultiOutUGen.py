# -*- encoding: utf-8 -*-
from supriya.tools.synthesistools.UGen import UGen


class MultiOutUGen(UGen):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_channel_count',
        '_output_proxies',
        )

    ### INTIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        special_index=0,
        channel_count=1,
        **kwargs
        ):
        self._channel_count = int(channel_count)
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            special_index=special_index,
            **kwargs
            )

    ### SPECIAL METHODS ###

    def __len__(self):
        return self.channel_count

    ### PRIVATE METHODS ###

    def _get_outputs(self):
        return [self.calculation_rate] * len(self)

    ### PUBLIC PROPERTIES ###

    @classmethod
    def ar(cls, **kwargs):
        from supriya.tools import synthesistools
        ugen = cls._new(
            calculation_rate=synthesistools.CalculationRate.AUDIO,
            special_index=0,
            **kwargs
            )
        output_proxies = []
        if isinstance(ugen, synthesistools.UGen):
            output_proxies.extend(ugen[:])
        else:
            for x in ugen:
                output_proxies.extend(x[:])
        result = synthesistools.UGenArray(output_proxies)
        return result

    @property
    def channel_count(self):
        return self._channel_count

    @classmethod
    def kr(cls, **kwargs):
        from supriya.tools import synthesistools
        ugen = cls._new(
            calculation_rate=synthesistools.CalculationRate.CONTROL,
            special_index=0,
            **kwargs
            )
        output_proxies = []
        if isinstance(ugen, synthesistools.UGen):
            output_proxies.extend(ugen[:])
        else:
            for x in ugen:
                output_proxies.extend(x[:])
        result = synthesistools.UgenArray(output_proxies)
        return result

    @property
    def outputs(self):
        return [self.calculation_rate for _ in range(len(self))]
