from supriya.ugens.PseudoUGen import PseudoUGen


class Silence(PseudoUGen):
    """
    An audio-rate silence pseudo-unit generator.

    ::

        >>> supriya.ugens.Silence.ar(channel_count=2)
        UGenArray({2})

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utility UGens'

    __slots__ = ()

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        channel_count=1,
        ):
        import supriya.synthdefs
        import supriya.ugens
        channel_count = int(channel_count)
        assert 0 <= channel_count
        silence = supriya.ugens.DC.ar(0)
        if channel_count == 1:
            return silence
        output_proxies = [silence[0]] * channel_count
        return supriya.synthdefs.UGenArray(output_proxies)
