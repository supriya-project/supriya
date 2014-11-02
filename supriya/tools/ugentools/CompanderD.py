# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PseudoUGen import PseudoUGen


class CompanderD(PseudoUGen):
    r'''Convenience constructor for Compander.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Dynamics UGens'

    __slots__ = ()

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        source=0.,
        thresh=0.5,
        clamp_time=0.01,
        relax_time=0.1,
        slope_above=1.,
        slope_below=1.,
        ):
        r'''Constructs an audio-rate dynamics processor.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> compander_d = ugentools.CompanderD.ar(
            ...     source=source,
            ...     )
            >>> print(str(compander_d))
            SynthDef ... {
                const_0:0.0 -> 0_In[0:bus]
                0_In[0] -> 1_DelayN[0:source]
                const_1:0.01 -> 1_DelayN[1:maximum_delay_time]
                const_1:0.01 -> 1_DelayN[2:delay_time]
                0_In[0] -> 2_Compander[0:source]
                1_DelayN[0] -> 2_Compander[1:control]
                const_2:0.5 -> 2_Compander[2:thresh]
                const_3:1.0 -> 2_Compander[3:slope_below]
                const_3:1.0 -> 2_Compander[4:slope_above]
                const_1:0.01 -> 2_Compander[5:clamp_time]
                const_4:0.1 -> 2_Compander[6:relax_time]
            }

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        from supriya.tools import ugentools
        rate = synthdeftools.Rate.AUDIO
        control = ugentools.DelayN.ar(
            source=source,
            maximum_delay_time=clamp_time,
            delay_time=clamp_time,
            )
        ugen = ugentools.Compander._new_expanded(
            clamp_time=clamp_time,
            rate=rate,
            relax_time=relax_time,
            slope_above=slope_above,
            slope_below=slope_below,
            source=source,
            control=control,
            thresh=thresh,
            )
        return ugen