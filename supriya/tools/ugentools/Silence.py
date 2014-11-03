# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PseudoUGen import PseudoUGen


class Silence(PseudoUGen):
    r'''Audio-calculation_rate silence pseudo-unit generator.

    ::

        >>> ugentools.Silence.ar(channel_count=2)
        UGenArray({2})

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utility UGens'

    __slots__ = ()

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        channel_count=1,
        ):
        from supriya.tools import synthdeftools
        from supriya.tools import ugentools
        channel_count = int(channel_count)
        assert 0 <= channel_count
        silence = ugentools.DC.ar(0)
        if channel_count == 1:
            return silence
        output_proxies = [silence[0]] * channel_count
        return synthdeftools.UGenArray(output_proxies)