# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.CalculationRate import CalculationRate
from supriya.tools.ugentools.WidthFirstUGen import WidthFirstUGen


class PV_ChainUGen(WidthFirstUGen):
    r'''Abstract base class for all phase-vocoder-chain unit generators.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    __slots__ = ()

    _valid_calculation_rates = (
        CalculationRate.CONTROL,
        )

    ### INITIALIZER ###
    
    def __init__(
        self,
        **kwargs
        ):
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        WidthFirstUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            **kwargs
            )

    ### PRIVATE METHODS ###

    def _add_copies_if_needed(self, input_mapping):
        pass

    r'''
    addCopiesIfNeeded {
        var directDescendants, frames, buf, copy;
        // find UGens that have me as an input
        directDescendants = buildSynthDef.children.select ({ |child|
            var inputs;
            child.isKindOf(PV_Copy).not and: { child.isKindOf(Unpack1FFT).not } and: {
                inputs = child.inputs;
                inputs.notNil and: { inputs.includes(this) }
            }
        });
        if(directDescendants.size > 1, {
            // insert a PV_Copy for all but the last one
            directDescendants.drop(-1).do({|desc|
                desc.inputs.do({ arg input, j;
                    if (input === this, {
                        frames = this.fftSize;
                        frames.widthFirstAntecedents = nil;
                        buf = LocalBuf(frames);
                        buf.widthFirstAntecedents = nil;
                        copy = PV_Copy(this, buf);
                        copy.widthFirstAntecedents = widthFirstAntecedents ++ [buf];
                        desc.inputs[j] = copy;
                        buildSynthDef.children = buildSynthDef.children.drop(-3).insert(this.synthIndex + 1, frames);
                        buildSynthDef.children = buildSynthDef.children.insert(this.synthIndex + 2, buf);
                        buildSynthDef.children = buildSynthDef.children.insert(this.synthIndex + 3, copy);
                        buildSynthDef.indexUGens;
                    });
                });
            });
        });
    }
    '''

    ### PUBLIC PROPERTIES ###

    @property
    def fft_size(self):
        r'''Gets FFT size as UGen input.

        Returns ugen input.
        '''
        return self.pv_chain.fft_size