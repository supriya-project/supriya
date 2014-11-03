ugens = {
    'A2K': {
        'parent': 'PureUGen',
        'methods': {
            'kr': [
                ('in', 0),
                ],
            },
        },
    'APF': {
        'parent': 'TwoPole',
        },
    'AbstractIn': {
        'parent': 'MultiOutUGen',
        'methods': {
            'isInputUGen': [
                ('nil', None),
                ('this', None),
                ],
            },
        },
    'AbstractOut': {
        'parent': 'UGen',
        'methods': {
            'isOutputUGen': [
                ('nil', None),
                ('this', None),
                ],
            'numFixedArgs': [
                ('nil', None),
                ('this', None),
                ],
            },
        },
    'AllpassC': {
        'parent': 'CombN',
        },
    'AllpassL': {
        'parent': 'CombN',
        },
    'AllpassN': {
        'parent': 'CombN',
        },
    'AmpComp': {
        'parent': 'PureUGen',
        'methods': {
            'ir': [
                ('freq', None),
                ('root', None),
                ('exp', 0.3333),
                ],
            'ar': [
                ('freq', None),
                ('root', None),
                ('exp', 0.3333),
                ],
            'kr': [
                ('freq', None),
                ('root', None),
                ('exp', 0.3333),
                ],
            },
        },
    'AmpCompA': {
        'parent': 'AmpComp',
        'methods': {
            'ir': [
                ('freq', 1000),
                ('root', 0),
                ('minAmp', 0.32),
                ('rootAmp', 1),
                ],
            'ar': [
                ('freq', 1000),
                ('root', 0),
                ('minAmp', 0.32),
                ('rootAmp', 1),
                ],
            'kr': [
                ('freq', 1000),
                ('root', 0),
                ('minAmp', 0.32),
                ('rootAmp', 1),
                ],
            },
        },
    'Amplitude': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('in', 0),
                ('attackTime', 0.01),
                ('releaseTime', 0.01),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('in', 0),
                ('attackTime', 0.01),
                ('releaseTime', 0.01),
                ('mul', 1),
                ('add', 0),
                ],
            'new': [
                ('in', None),
                ],
            },
        },
    'AudioControl': {
        'parent': 'MultiOutUGen',
        'methods': {
            'names': [
                ('names', None),
                ],
            'ar': [
                ('values', None),
                ],
            'isAudioControlUGen': [
                ('nil', None),
                ('this', None),
                ],
            'isControlUGen': [
                ('nil', None),
                ('this', None),
                ],
            },
        },
    'BAllPass': {
        'parent': 'BEQSuite',
        'methods': {
            'ar': [
                ('in', None),
                ('freq', 1200),
                ('rq', 1),
                ('mul', 1),
                ('add', 0),
                ],
            'sc': [
                ('dummy', None),
                ('freq', 1200),
                ('rq', 1),
                ],
            'coeffs': [
                ('sr', 44100),
                ('freq', 1200),
                ('rq', 1),
                ],
            },
        },
    'BBandPass': {
        'parent': 'BEQSuite',
        'methods': {
            'ar': [
                ('in', None),
                ('freq', 1200),
                ('bw', 1),
                ('mul', 1),
                ('add', 0),
                ],
            'sc': [
                ('dummy', None),
                ('freq', 1200),
                ('bw', 1),
                ],
            'coeffs': [
                ('sr', 44100),
                ('freq', 1200),
                ('bw', 1),
                ],
            },
        },
    'BBandStop': {
        'parent': 'BEQSuite',
        'methods': {
            'ar': [
                ('in', None),
                ('freq', 1200),
                ('bw', 1),
                ('mul', 1),
                ('add', 0),
                ],
            'sc': [
                ('dummy', None),
                ('freq', 1200),
                ('bw', 1),
                ],
            'coeffs': [
                ('sr', 44100),
                ('freq', 1200),
                ('bw', 1),
                ],
            },
        },
    'BEQSuite': {
        'parent': 'Filter',
        },
    'BHiCut': {
        'parent': 'BEQSuite',
        'methods': {
            'allRQs': [],
            'initClass': [
                ('nil', None),
                ('this', None),
                ],
            'filterClass': [
                ('nil', None),
                ('this', None),
                ],
            'coeffs': [
                ('sr', None),
                ('freq', 1200),
                ('order', 2),
                ],
            'new1': [
                ('rate', 'audio'),
                ('in', None),
                ('freq', None),
                ('order', 2),
                ('maxOrder', 5),
                ],
            'newFixed': [
                ('rate', 'audio'),
                ('in', None),
                ('freq', None),
                ('order', 2),
                ],
            'newVari': [
                ('rate', 'audio'),
                ('in', None),
                ('freq', None),
                ('order', 2),
                ('maxOrder', 5),
                ],
            'ar': [
                ('in', None),
                ('freq', None),
                ('order', 2),
                ('maxOrder', 5),
                ],
            'kr': [
                ('in', None),
                ('freq', None),
                ('order', 2),
                ('maxOrder', 5),
                ],
            'magResponse': [
                ('freqs', 1000),
                ('sr', 44100),
                ('freq', 1200),
                ('order', 2),
                ],
            },
        },
    'BHiPass': {
        'parent': 'BEQSuite',
        'methods': {
            'ar': [
                ('in', None),
                ('freq', 1200),
                ('rq', 1),
                ('mul', 1),
                ('add', 0),
                ],
            'sc': [
                ('dummy', None),
                ('freq', 1200),
                ('rq', 1),
                ],
            'coeffs': [
                ('sr', 44100),
                ('freq', 1200),
                ('rq', 1),
                ],
            },
        },
    'BHiShelf': {
        'parent': 'BEQSuite',
        'methods': {
            'ar': [
                ('in', None),
                ('freq', 1200),
                ('rs', 1),
                ('db', 0),
                ('mul', 1),
                ('add', 0),
                ],
            'sc': [
                ('dummy', None),
                ('freq', 120),
                ('rs', 1),
                ('db', 0),
                ],
            'coeffs': [
                ('sr', 44100),
                ('freq', 120),
                ('rs', 1),
                ('db', 0),
                ],
            },
        },
    'BLowCut': {
        'parent': 'BHiCut',
        'methods': {
            'filterClass': [
                ('nil', None),
                ('this', None),
                ],
            },
        },
    'BLowPass': {
        'parent': 'BEQSuite',
        'methods': {
            'ar': [
                ('in', None),
                ('freq', 1200),
                ('rq', 1),
                ('mul', 1),
                ('add', 0),
                ],
            'sc': [
                ('dummy', None),
                ('freq', 1200),
                ('rq', 1),
                ],
            'coeffs': [
                ('sr', 44100),
                ('freq', 1200),
                ('rq', 1),
                ],
            },
        },
    'BLowShelf': {
        'parent': 'BEQSuite',
        'methods': {
            'ar': [
                ('in', None),
                ('freq', 1200),
                ('rs', 1),
                ('db', 0),
                ('mul', 1),
                ('add', 0),
                ],
            'sc': [
                ('dummy', None),
                ('freq', 120),
                ('rs', 1),
                ('db', 0),
                ],
            'coeffs': [
                ('sr', 44100),
                ('freq', 120),
                ('rs', 1),
                ('db', 0),
                ],
            },
        },
    'BPF': {
        'parent': 'Filter',
        'methods': {
            'ar': [
                ('in', 0),
                ('freq', 440),
                ('rq', 1),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('in', 0),
                ('freq', 440),
                ('rq', 1),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'BPZ2': {
        'parent': 'LPZ2',
        'methods': {
            'coeffs': [
                ('nil', None),
                ('this', None),
                ],
            },
        },
    'BPeakEQ': {
        'parent': 'BEQSuite',
        'methods': {
            'ar': [
                ('in', None),
                ('freq', 1200),
                ('rq', 1),
                ('db', 0),
                ('mul', 1),
                ('add', 0),
                ],
            'sc': [
                ('dummy', None),
                ('freq', 1200),
                ('rq', 1),
                ('db', 0),
                ],
            'coeffs': [
                ('sr', 44100),
                ('freq', 1200),
                ('rq', 1),
                ('db', 0),
                ],
            },
        },
    'BRF': {
        'parent': 'BPF',
        },
    'BRZ2': {
        'parent': 'LPZ2',
        'methods': {
            'coeffs': [
                ('nil', None),
                ('this', None),
                ],
            },
        },
    'Balance2': {
        'parent': 'MultiOutUGen',
        'methods': {
            'ar': [
                ('left', None),
                ('right', None),
                ('pos', 0),
                ('level', 1),
                ],
            'kr': [
                ('left', None),
                ('right', None),
                ('pos', 0),
                ('level', 1),
                ],
            },
        },
    'Ball': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('in', 0),
                ('g', 1),
                ('damp', 0),
                ('friction', 0.01),
                ],
            'kr': [
                ('in', 0),
                ('g', 1),
                ('damp', 0),
                ('friction', 0.01),
                ],
            },
        },
    'BasicOpUGen': {
        'parent': 'UGen',
        },
    'BeatTrack': {
        'parent': 'MultiOutUGen',
        'methods': {
            'kr': [
                ('chain', None),
                ('lock', 0),
                ],
            },
        },
    'BeatTrack2': {
        'parent': 'MultiOutUGen',
        'methods': {
            'kr': [
                ('busindex', None),
                ('numfeatures', None),
                ('windowsize', 2),
                ('phaseaccuracy', 0.02),
                ('lock', 0),
                ('weightingscheme', None),
                ],
            },
        },
    'BiPanB2': {
        'parent': 'MultiOutUGen',
        'methods': {
            'ar': [
                ('inA', None),
                ('inB', None),
                ('azimuth', None),
                ('gain', 1),
                ],
            'kr': [
                ('inA', None),
                ('inB', None),
                ('azimuth', None),
                ('gain', 1),
                ],
            },
        },
    'BinaryOpUGen': {
        'parent': 'BasicOpUGen',
        'methods': {
            'new': [
                ('selector', None),
                ('a', None),
                ('b', None),
                ],
            'new1': [
                ('rate', None),
                ('selector', None),
                ('a', None),
                ('b', None),
                ],
            },
        },
    'Blip': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('freq', 440),
                ('numharm', 200),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('freq', 440),
                ('numharm', 200),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'BlockSize': {
        'parent': 'InfoUGenBase',
        },
    'BrownNoise': {
        'parent': 'WhiteNoise',
        },
    'BufAllpassC': {
        'parent': 'BufCombN',
        },
    'BufAllpassL': {
        'parent': 'BufCombN',
        },
    'BufAllpassN': {
        'parent': 'BufCombN',
        },
    'BufChannels': {
        'parent': 'BufInfoUGenBase',
        },
    'BufCombC': {
        'parent': 'BufCombN',
        },
    'BufCombL': {
        'parent': 'BufCombN',
        },
    'BufCombN': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('buf', 0),
                ('in', 0),
                ('delaytime', 0.2),
                ('decaytime', 1),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'BufDelayC': {
        'parent': 'BufDelayN',
        },
    'BufDelayL': {
        'parent': 'BufDelayN',
        },
    'BufDelayN': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('buf', 0),
                ('in', 0),
                ('delaytime', 0.2),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('buf', 0),
                ('in', 0),
                ('delaytime', 0.2),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'BufDur': {
        'parent': 'BufInfoUGenBase',
        },
    'BufFrames': {
        'parent': 'BufInfoUGenBase',
        },
    'BufInfoUGenBase': {
        'parent': 'UGen',
        'methods': {
            'kr': [
                ('bufnum', None),
                ],
            'ir': [
                ('bufnum', None),
                ],
            },
        },
    'BufRateScale': {
        'parent': 'BufInfoUGenBase',
        },
    'BufRd': {
        'parent': 'MultiOutUGen',
        'methods': {
            'ar': [
                ('numChannels', None),
                ('bufnum', 0),
                ('phase', 0),
                ('loop', 1),
                ('interpolation', 2),
                ],
            'kr': [
                ('numChannels', None),
                ('bufnum', 0),
                ('phase', 0),
                ('loop', 1),
                ('interpolation', 2),
                ],
            },
        },
    'BufSampleRate': {
        'parent': 'BufInfoUGenBase',
        },
    'BufSamples': {
        'parent': 'BufInfoUGenBase',
        },
    'BufWr': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('inputArray', None),
                ('bufnum', 0),
                ('phase', 0),
                ('loop', 1),
                ],
            'kr': [
                ('inputArray', None),
                ('bufnum', 0),
                ('phase', 0),
                ('loop', 1),
                ],
            },
        },
    'COsc': {
        'parent': 'PureUGen',
        'methods': {
            'ar': [
                ('bufnum', None),
                ('freq', 440),
                ('beats', 0.5),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('bufnum', None),
                ('freq', 440),
                ('beats', 0.5),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'Changed': {
        'parent': 'Filter',
        'methods': {
            'kr': [
                ('input', None),
                ('threshold', 0),
                ],
            'ar': [
                ('input', None),
                ('threshold', 0),
                ],
            },
        },
    'ChaosGen': {
        'parent': 'UGen',
        },
    'CheckBadValues': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('in', 0),
                ('id', 0),
                ('post', 2),
                ],
            'kr': [
                ('in', 0),
                ('id', 0),
                ('post', 2),
                ],
            },
        },
    'ClearBuf': {
        'parent': 'WidthFirstUGen',
        'methods': {
            'new': [
                ('buf', None),
                ],
            },
        },
    'Clip': {
        'parent': 'InRange',
        },
    'ClipNoise': {
        'parent': 'WhiteNoise',
        },
    'CoinGate': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('prob', None),
                ('in', None),
                ],
            'kr': [
                ('prob', None),
                ('in', None),
                ],
            },
        },
    'CombC': {
        'parent': 'CombN',
        },
    'CombFormlet': {
        'parent': 'Filter',
        'methods': {
            'ar': [
                ('in', 0),
                ('freq', 440),
                ('attacktime', 1),
                ('decaytime', 1),
                ('mul', 1),
                ('add', 0),
                ('minFreq', 20),
                ],
            },
        },
    'CombL': {
        'parent': 'CombN',
        },
    'CombN': {
        'parent': 'PureUGen',
        'methods': {
            'ar': [
                ('in', 0),
                ('maxdelaytime', 0.2),
                ('delaytime', 0.2),
                ('decaytime', 1),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('in', 0),
                ('maxdelaytime', 0.2),
                ('delaytime', 0.2),
                ('decaytime', 1),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'Compander': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('in', 0),
                ('control', 0),
                ('thresh', 0.5),
                ('slopeBelow', 1),
                ('slopeAbove', 1),
                ('clampTime', 0.01),
                ('relaxTime', 0.1),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'CompanderD': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('in', 0),
                ('thresh', 0.5),
                ('slopeBelow', 1),
                ('slopeAbove', 1),
                ('clampTime', 0.01),
                ('relaxTime', 0.01),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'Control': {
        'parent': 'MultiOutUGen',
        'methods': {
            'names': [
                ('names', None),
                ],
            'kr': [
                ('values', None),
                ],
            'ir': [
                ('values', None),
                ],
            'isControlUGen': [
                ('nil', None),
                ('this', None),
                ],
            },
        },
    'ControlDur': {
        'parent': 'InfoUGenBase',
        },
    'ControlRate': {
        'parent': 'InfoUGenBase',
        },
    'Convolution': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('in', None),
                ('kernel', None),
                ('framesize', 512),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'Convolution2': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('in', None),
                ('kernel', None),
                ('trigger', 0),
                ('framesize', 2048),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'Convolution2L': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('in', None),
                ('kernel', None),
                ('trigger', 0),
                ('framesize', 2048),
                ('crossfade', 1),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'Convolution3': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('in', None),
                ('kernel', None),
                ('trigger', 0),
                ('framesize', 2048),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('in', None),
                ('kernel', None),
                ('trigger', 0),
                ('framesize', 2048),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'Crackle': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('chaosParam', 1.5),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('chaosParam', 1.5),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'CuspL': {
        'parent': 'CuspN',
        },
    'CuspN': {
        'parent': 'ChaosGen',
        'methods': {
            'equation': [],
            'ar': [
                ('freq', 22050),
                ('a', 1),
                ('b', 1.9),
                ('xi', 0),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'DC': {
        'parent': 'PureMultiOutUGen',
        'methods': {
            'ar': [
                ('in', 0),
                ],
            'kr': [
                ('in', 0),
                ],
            },
        },
    'DUGen': {
        'parent': 'UGen',
        },
    'Dbrown': {
        'parent': 'DUGen',
        'methods': {
            'new': [
                ('lo', 0),
                ('hi', 1),
                ('step', 0.01),
                ('length', "float('inf')"),
                ],
            },
        },
    'Dbufrd': {
        'parent': 'DUGen',
        'methods': {
            'new': [
                ('bufnum', 0),
                ('phase', 0),
                ('loop', 1),
                ],
            },
        },
    'Dbufwr': {
        'parent': 'DUGen',
        'methods': {
            'new': [
                ('input', 0),
                ('bufnum', 0),
                ('phase', 0),
                ('loop', 1),
                ],
            },
        },
    'Decay': {
        'parent': 'Filter',
        'methods': {
            'ar': [
                ('in', 0),
                ('decayTime', 1),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('in', 0),
                ('decayTime', 1),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'Decay2': {
        'parent': 'Filter',
        'methods': {
            'ar': [
                ('in', 0),
                ('attackTime', 0.01),
                ('decayTime', 1),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('in', 0),
                ('attackTime', 0.01),
                ('decayTime', 1),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'DecodeB2': {
        'parent': 'MultiOutUGen',
        'methods': {
            'ar': [
                ('numChans', None),
                ('w', None),
                ('x', None),
                ('y', None),
                ('orientation', 0.5),
                ],
            'kr': [
                ('numChans', None),
                ('w', None),
                ('x', None),
                ('y', None),
                ('orientation', 0.5),
                ],
            },
        },
    'DegreeToKey': {
        'parent': 'PureUGen',
        'methods': {
            'ar': [
                ('bufnum', None),
                ('in', 0),
                ('octave', 12),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('bufnum', None),
                ('in', 0),
                ('octave', 12),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'DelTapRd': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('buffer', None),
                ('phase', None),
                ('delTime', None),
                ('interp', 1),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('buffer', None),
                ('phase', None),
                ('delTime', None),
                ('interp', 1),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'DelTapWr': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('buffer', None),
                ('in', None),
                ],
            'kr': [
                ('buffer', None),
                ('in', None),
                ],
            },
        },
    'Delay1': {
        'parent': 'PureUGen',
        'methods': {
            'ar': [
                ('in', 0),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('in', 0),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'Delay2': {
        'parent': 'Delay1',
        },
    'DelayC': {
        'parent': 'DelayN',
        },
    'DelayL': {
        'parent': 'DelayN',
        },
    'DelayN': {
        'parent': 'PureUGen',
        'methods': {
            'ar': [
                ('in', 0),
                ('maxdelaytime', 0.2),
                ('delaytime', 0.2),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('in', 0),
                ('maxdelaytime', 0.2),
                ('delaytime', 0.2),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'Demand': {
        'parent': 'MultiOutUGen',
        'methods': {
            'ar': [
                ('trig', None),
                ('reset', None),
                ('demandUGens', None),
                ],
            'kr': [
                ('trig', None),
                ('reset', None),
                ('demandUGens', None),
                ],
            },
        },
    'DemandEnvGen': {
        'parent': 'UGen',
        'methods': {
            'kr': [
                ('level', None),
                ('dur', None),
                ('shape', 1),
                ('curve', 0),
                ('gate', 1),
                ('reset', 1),
                ('levelScale', 1),
                ('levelBias', 0),
                ('timeScale', 1),
                ('doneAction', 0),
                ],
            'ar': [
                ('level', None),
                ('dur', None),
                ('shape', 1),
                ('curve', 0),
                ('gate', 1),
                ('reset', 1),
                ('levelScale', 1),
                ('levelBias', 0),
                ('timeScale', 1),
                ('doneAction', 0),
                ],
            },
        },
    'DetectIndex': {
        'parent': 'Index',
        },
    'DetectSilence': {
        'parent': 'Filter',
        'methods': {
            'ar': [
                ('in', 0),
                ('amp', 0.0001),
                ('time', 0.1),
                ('doneAction', 0),
                ],
            'kr': [
                ('in', 0),
                ('amp', 0.0001),
                ('time', 0.1),
                ('doneAction', 0),
                ],
            },
        },
    'Dgeom': {
        'parent': 'DUGen',
        'methods': {
            'new': [
                ('start', 1),
                ('grow', 2),
                ('length', "float('inf')"),
                ],
            },
        },
    'Dibrown': {
        'parent': 'Dbrown',
        },
    'DiskIn': {
        'parent': 'MultiOutUGen',
        'methods': {
            'ar': [
                ('numChannels', None),
                ('bufnum', None),
                ('loop', 0),
                ],
            },
        },
    'DiskOut': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('bufnum', None),
                ('channelsArray', None),
                ],
            },
        },
    'Diwhite': {
        'parent': 'Dwhite',
        },
    'Donce': {
        'parent': 'DUGen',
        'methods': {
            'new': [
                ('in', None),
                ],
            },
        },
    'Done': {
        'parent': 'UGen',
        'methods': {
            'kr': [
                ('src', None),
                ],
            },
        },
    'Dpoll': {
        'parent': 'DUGen',
        'methods': {
            'new': [
                ('in', None),
                ('label', None),
                ('run', 1),
                ('trigid', -1),
                ],
            'new1': [
                ('rate', None),
                ('in', None),
                ('label', None),
                ('run', None),
                ('trigid', None),
                ],
            },
        },
    'Drand': {
        'parent': 'ListDUGen',
        },
    'Dreset': {
        'parent': 'DUGen',
        'methods': {
            'new': [
                ('in', None),
                ('reset', 0),
                ],
            },
        },
    'Dseq': {
        'parent': 'ListDUGen',
        },
    'Dser': {
        'parent': 'ListDUGen',
        },
    'Dseries': {
        'parent': 'DUGen',
        'methods': {
            'new': [
                ('start', 1),
                ('step', 1),
                ('length', "float('inf')"),
                ],
            },
        },
    'Dshuf': {
        'parent': 'ListDUGen',
        },
    'Dstutter': {
        'parent': 'DUGen',
        'methods': {
            'new': [
                ('n', None),
                ('in', None),
                ],
            },
        },
    'Dswitch': {
        'parent': 'Dswitch1',
        },
    'Dswitch1': {
        'parent': 'DUGen',
        'methods': {
            'new': [
                ('list', None),
                ('index', None),
                ],
            },
        },
    'Dunique': {
        'parent': 'UGen',
        'methods': {
            'new': [
                ('source', None),
                ('maxBufferSize', 1024),
                ('protected', True),
                ],
            },
        },
    'Dust': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('density', 0),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('density', 0),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'Dust2': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('density', 0),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('density', 0),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'Duty': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('dur', 1),
                ('reset', 0),
                ('level', 1),
                ('doneAction', 0),
                ],
            'kr': [
                ('dur', 1),
                ('reset', 0),
                ('level', 1),
                ('doneAction', 0),
                ],
            },
        },
    'Dwhite': {
        'parent': 'DUGen',
        'methods': {
            'new': [
                ('lo', 0),
                ('hi', 1),
                ('length', "float('inf')"),
                ],
            },
        },
    'Dwrand': {
        'parent': 'DUGen',
        'methods': {
            'new': [
                ('list', None),
                ('weights', None),
                ('repeats', 1),
                ],
            },
        },
    'Dxrand': {
        'parent': 'ListDUGen',
        },
    'DynKlang': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('specificationsArrayRef', None),
                ('freqscale', 1),
                ('freqoffset', 0),
                ],
            'kr': [
                ('specificationsArrayRef', None),
                ('freqscale', 1),
                ('freqoffset', 0),
                ],
            'new1': [
                ('rate', None),
                ('specificationsArrayRef', None),
                ('freqscale', 1),
                ('freqoffset', 0),
                ],
            },
        },
    'DynKlank': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('specificationsArrayRef', None),
                ('input', None),
                ('freqscale', 1),
                ('freqoffset', 0),
                ('decayscale', 1),
                ],
            'kr': [
                ('specificationsArrayRef', None),
                ('input', None),
                ('freqscale', 1),
                ('freqoffset', 0),
                ('decayscale', 1),
                ],
            'new1': [
                ('rate', None),
                ('specificationsArrayRef', None),
                ('input', None),
                ('freqscale', 1),
                ('freqoffset', 0),
                ('decayscale', 1),
                ],
            },
        },
    'EnvGen': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('envelope', None),
                ('gate', 1),
                ('levelScale', 1),
                ('levelBias', 0),
                ('timeScale', 1),
                ('doneAction', 0),
                ],
            'kr': [
                ('envelope', None),
                ('gate', 1),
                ('levelScale', 1),
                ('levelBias', 0),
                ('timeScale', 1),
                ('doneAction', 0),
                ],
            'convertEnv': [
                ('env', None),
                ],
            'new1': [
                ('rate', None),
                ('gate', None),
                ('levelScale', None),
                ('levelBias', None),
                ('timeScale', None),
                ('doneAction', None),
                ('envArray', None),
                ],
            },
        },
    'ExpRand': {
        'parent': 'UGen',
        'methods': {
            'new': [
                ('lo', 0.01),
                ('hi', 1),
                ],
            },
        },
    'FBSineC': {
        'parent': 'FBSineN',
        },
    'FBSineL': {
        'parent': 'FBSineN',
        },
    'FBSineN': {
        'parent': 'ChaosGen',
        'methods': {
            'equation': [],
            'ar': [
                ('freq', 22050),
                ('im', 1),
                ('fb', 0.1),
                ('a', 1.1),
                ('c', 0.5),
                ('xi', 0.1),
                ('yi', 0.1),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'FFT': {
        'parent': 'PV_ChainUGen',
        'methods': {
            'new': [
                ('buffer', None),
                ('in', 0),
                ('hop', 0.5),
                ('wintype', 0),
                ('active', 1),
                ('winsize', 0),
                ],
            },
        },
    'FFTTrigger': {
        'parent': 'PV_ChainUGen',
        'methods': {
            'new': [
                ('buffer', None),
                ('hop', 0.5),
                ('polar', 0),
                ],
            },
        },
    'FOS': {
        'parent': 'Filter',
        'methods': {
            'ar': [
                ('in', 0),
                ('a0', 0),
                ('a1', 0),
                ('b1', 0),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('in', 0),
                ('a0', 0),
                ('a1', 0),
                ('b1', 0),
                ('mul', 1),
                ('add', 0),
                ],
            'coeffs': [
                ('sr', 44100),
                ('a0', 0),
                ('a1', 0),
                ('b1', 0),
                ],
            },
        },
    'FSinOsc': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('freq', 440),
                ('iphase', 0),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('freq', 440),
                ('iphase', 0),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'Filter': {
        'parent': 'PureUGen',
        'methods': {
            'scopeResponse': [
                ('server', None),
                ('freqMode', 1),
                ('label', None),
                ('args', None),
                ],
            'coeffs': [
                ('nil', None),
                ('this', None),
                ],
            'magResponse': [
                ('freqs', 1000),
                ('sr', 44100),
                ('rest', '[  ]'),
                ],
            'magResponse2': [
                ('freqs', None),
                ('sr', None),
                ('ma', None),
                ('ar', None),
                ],
            'magResponse5': [
                ('freqs', None),
                ('sr', None),
                ('ma', None),
                ('ar', None),
                ],
            'magResponseN': [
                ('freqs', None),
                ('sr', None),
                ('ma', None),
                ('ar', None),
                ('size', None),
                ],
            },
        },
    'Fold': {
        'parent': 'InRange',
        },
    'Formant': {
        'parent': 'PureUGen',
        'methods': {
            'ar': [
                ('fundfreq', 440),
                ('formfreq', 1760),
                ('bwfreq', 880),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'Formlet': {
        'parent': 'Filter',
        'methods': {
            'ar': [
                ('in', 0),
                ('freq', 440),
                ('attacktime', 1),
                ('decaytime', 1),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('in', 0),
                ('freq', 440),
                ('attacktime', 1),
                ('decaytime', 1),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'Free': {
        'parent': 'UGen',
        'methods': {
            'kr': [
                ('trig', None),
                ('id', None),
                ],
            },
        },
    'FreeSelf': {
        'parent': 'UGen',
        'methods': {
            'kr': [
                ('in', None),
                ],
            },
        },
    'FreeSelfWhenDone': {
        'parent': 'UGen',
        'methods': {
            'kr': [
                ('src', None),
                ],
            },
        },
    'FreeVerb': {
        'parent': 'Filter',
        'methods': {
            'ar': [
                ('in', None),
                ('mix', 0.33),
                ('room', 0.5),
                ('damp', 0.5),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'FreeVerb2': {
        'parent': 'MultiOutUGen',
        'methods': {
            'ar': [
                ('in', None),
                ('in2', None),
                ('mix', 0.33),
                ('room', 0.5),
                ('damp', 0.5),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'FreqShift': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('in', None),
                ('freq', 0),
                ('phase', 0),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'GVerb': {
        'parent': 'MultiOutUGen',
        'methods': {
            'ar': [
                ('in', None),
                ('roomsize', 10),
                ('revtime', 3),
                ('damping', 0.5),
                ('inputbw', 0.5),
                ('spread', 15),
                ('drylevel', 1),
                ('earlyreflevel', 0.7),
                ('taillevel', 0.5),
                ('maxroomsize', 300),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'Gate': {
        'parent': 'Latch',
        },
    'GbmanL': {
        'parent': 'GbmanN',
        },
    'GbmanN': {
        'parent': 'ChaosGen',
        'methods': {
            'equation': [],
            'ar': [
                ('freq', 22050),
                ('xi', 1.2),
                ('yi', 2.1),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'Gendy1': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('ampdist', 1),
                ('durdist', 1),
                ('adparam', 1),
                ('ddparam', 1),
                ('minfreq', 440),
                ('maxfreq', 660),
                ('ampscale', 0.5),
                ('durscale', 0.5),
                ('initCPs', 12),
                ('knum', None),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('ampdist', 1),
                ('durdist', 1),
                ('adparam', 1),
                ('ddparam', 1),
                ('minfreq', 20),
                ('maxfreq', 1000),
                ('ampscale', 0.5),
                ('durscale', 0.5),
                ('initCPs', 12),
                ('knum', None),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'Gendy2': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('ampdist', 1),
                ('durdist', 1),
                ('adparam', 1),
                ('ddparam', 1),
                ('minfreq', 440),
                ('maxfreq', 660),
                ('ampscale', 0.5),
                ('durscale', 0.5),
                ('initCPs', 12),
                ('knum', None),
                ('a', 1.17),
                ('c', 0.31),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('ampdist', 1),
                ('durdist', 1),
                ('adparam', 1),
                ('ddparam', 1),
                ('minfreq', 20),
                ('maxfreq', 1000),
                ('ampscale', 0.5),
                ('durscale', 0.5),
                ('initCPs', 12),
                ('knum', None),
                ('a', 1.17),
                ('c', 0.31),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'Gendy3': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('ampdist', 1),
                ('durdist', 1),
                ('adparam', 1),
                ('ddparam', 1),
                ('freq', 440),
                ('ampscale', 0.5),
                ('durscale', 0.5),
                ('initCPs', 12),
                ('knum', None),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('ampdist', 1),
                ('durdist', 1),
                ('adparam', 1),
                ('ddparam', 1),
                ('freq', 440),
                ('ampscale', 0.5),
                ('durscale', 0.5),
                ('initCPs', 12),
                ('knum', None),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'GrainBuf': {
        'parent': 'MultiOutUGen',
        'methods': {
            'ar': [
                ('numChannels', 1),
                ('trigger', 0),
                ('dur', 1),
                ('sndbuf', None),
                ('rate', 1),
                ('pos', 0),
                ('interp', 2),
                ('pan', 0),
                ('envbufnum', -1),
                ('maxGrains', 512),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'GrainFM': {
        'parent': 'MultiOutUGen',
        'methods': {
            'ar': [
                ('numChannels', 1),
                ('trigger', 0),
                ('dur', 1),
                ('carfreq', 440),
                ('modfreq', 200),
                ('index', 1),
                ('pan', 0),
                ('envbufnum', -1),
                ('maxGrains', 512),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'GrainIn': {
        'parent': 'MultiOutUGen',
        'methods': {
            'ar': [
                ('numChannels', 1),
                ('trigger', 0),
                ('dur', 1),
                ('in', None),
                ('pan', 0),
                ('envbufnum', -1),
                ('maxGrains', 512),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'GrainSin': {
        'parent': 'MultiOutUGen',
        'methods': {
            'ar': [
                ('numChannels', 1),
                ('trigger', 0),
                ('dur', 1),
                ('freq', 440),
                ('pan', 0),
                ('envbufnum', -1),
                ('maxGrains', 512),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'GrayNoise': {
        'parent': 'WhiteNoise',
        },
    'HPF': {
        'parent': 'LPF',
        },
    'HPZ1': {
        'parent': 'LPZ1',
        'methods': {
            'coeffs': [
                ('nil', None),
                ('this', None),
                ],
            },
        },
    'HPZ2': {
        'parent': 'LPZ2',
        'methods': {
            'coeffs': [
                ('nil', None),
                ('this', None),
                ],
            },
        },
    'Hasher': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('in', 0),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('in', 0),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'HenonC': {
        'parent': 'HenonN',
        },
    'HenonL': {
        'parent': 'HenonN',
        },
    'HenonN': {
        'parent': 'ChaosGen',
        'methods': {
            'equation': [],
            'ar': [
                ('freq', 22050),
                ('a', 1.4),
                ('b', 0.3),
                ('x0', 0),
                ('x1', 0),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'Hilbert': {
        'parent': 'MultiOutUGen',
        'methods': {
            'ar': [
                ('in', None),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'HilbertFIR': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('in', None),
                ('buffer', None),
                ],
            },
        },
    'IEnvGen': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('envelope', None),
                ('index', None),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('envelope', None),
                ('index', None),
                ('mul', 1),
                ('add', 0),
                ],
            'convertEnv': [
                ('env', None),
                ],
            'new1': [
                ('rate', None),
                ('index', None),
                ('envArray', None),
                ],
            },
        },
    'IFFT': {
        'parent': 'WidthFirstUGen',
        'methods': {
            'new': [
                ('buffer', None),
                ('wintype', 0),
                ('winsize', 0),
                ],
            'ar': [
                ('buffer', None),
                ('wintype', 0),
                ('winsize', 0),
                ],
            'kr': [
                ('buffer', None),
                ('wintype', 0),
                ('winsize', 0),
                ],
            },
        },
    'IRand': {
        'parent': 'UGen',
        'methods': {
            'new': [
                ('lo', 0),
                ('hi', 127),
                ],
            },
        },
    'Impulse': {
        'parent': 'PureUGen',
        'methods': {
            'ar': [
                ('freq', 440),
                ('phase', 0),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('freq', 440),
                ('phase', 0),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'In': {
        'parent': 'AbstractIn',
        'methods': {
            'ar': [
                ('bus', 0),
                ('numChannels', 1),
                ],
            'kr': [
                ('bus', 0),
                ('numChannels', 1),
                ],
            },
        },
    'InBus': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('bus', None),
                ('numChannels', None),
                ('offset', 0),
                ('clip', None),
                ],
            'kr': [
                ('bus', None),
                ('numChannels', None),
                ('offset', 0),
                ('clip', None),
                ],
            'new1': [
                ('rate', None),
                ('bus', None),
                ('numChannels', None),
                ('offset', None),
                ('clip', None),
                ],
            },
        },
    'InFeedback': {
        'parent': 'AbstractIn',
        'methods': {
            'ar': [
                ('bus', 0),
                ('numChannels', 1),
                ],
            },
        },
    'InRange': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('in', 0),
                ('lo', 0),
                ('hi', 1),
                ],
            'kr': [
                ('in', 0),
                ('lo', 0),
                ('hi', 1),
                ],
            'ir': [
                ('in', 0),
                ('lo', 0),
                ('hi', 1),
                ],
            },
        },
    'InRect': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('x', 0),
                ('y', 0),
                ('rect', None),
                ],
            'kr': [
                ('x', 0),
                ('y', 0),
                ('rect', None),
                ],
            },
        },
    'InTrig': {
        'parent': 'AbstractIn',
        'methods': {
            'kr': [
                ('bus', 0),
                ('numChannels', 1),
                ],
            },
        },
    'Index': {
        'parent': 'PureUGen',
        'methods': {
            'ar': [
                ('bufnum', None),
                ('in', 0),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('bufnum', None),
                ('in', 0),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'IndexInBetween': {
        'parent': 'Index',
        },
    'IndexL': {
        'parent': 'Index',
        },
    'InfoUGenBase': {
        'parent': 'UGen',
        'methods': {
            'ir': [
                ('nil', None),
                ('this', None),
                ],
            },
        },
    'Integrator': {
        'parent': 'Filter',
        'methods': {
            'ar': [
                ('in', 0),
                ('coef', 1),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('in', 0),
                ('coef', 1),
                ('mul', 1),
                ('add', 0),
                ],
            'coeffs': [
                ('sr', 44100),
                ('coef', 1),
                ],
            },
        },
    'K2A': {
        'parent': 'PureUGen',
        'methods': {
            'ar': [
                ('in', 0),
                ],
            },
        },
    'KeyState': {
        'parent': 'UGen',
        'methods': {
            'kr': [
                ('keycode', 0),
                ('minval', 0),
                ('maxval', 1),
                ('lag', 0.2),
                ],
            },
        },
    'KeyTrack': {
        'parent': 'UGen',
        'methods': {
            'kr': [
                ('chain', None),
                ('keydecay', 2),
                ('chromaleak', 0.5),
                ],
            },
        },
    'Klang': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('specificationsArrayRef', None),
                ('freqscale', 1),
                ('freqoffset', 0),
                ],
            'new1': [
                ('rate', None),
                ('freqscale', None),
                ('freqoffset', None),
                ('arrayRef', None),
                ],
            },
        },
    'Klank': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('specificationsArrayRef', None),
                ('input', None),
                ('freqscale', 1),
                ('freqoffset', 0),
                ('decayscale', 1),
                ],
            'new1': [
                ('rate', None),
                ('input', None),
                ('freqscale', None),
                ('freqoffset', None),
                ('decayscale', None),
                ('arrayRef', None),
                ],
            },
        },
    'LFClipNoise': {
        'parent': 'LFNoise0',
        },
    'LFCub': {
        'parent': 'LFSaw',
        },
    'LFDClipNoise': {
        'parent': 'LFNoise0',
        },
    'LFDNoise0': {
        'parent': 'LFNoise0',
        },
    'LFDNoise1': {
        'parent': 'LFNoise0',
        },
    'LFDNoise3': {
        'parent': 'LFNoise0',
        },
    'LFGauss': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('duration', 1),
                ('width', 0.1),
                ('iphase', 0),
                ('loop', 1),
                ('doneAction', 0),
                ],
            'kr': [
                ('duration', 1),
                ('width', 0.1),
                ('iphase', 0),
                ('loop', 1),
                ('doneAction', 0),
                ],
            },
        },
    'LFNoise0': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('freq', 500),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('freq', 500),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'LFNoise1': {
        'parent': 'LFNoise0',
        },
    'LFNoise2': {
        'parent': 'LFNoise0',
        },
    'LFPar': {
        'parent': 'LFSaw',
        },
    'LFPulse': {
        'parent': 'PureUGen',
        'methods': {
            'ar': [
                ('freq', 440),
                ('iphase', 0),
                ('width', 0.5),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('freq', 440),
                ('iphase', 0),
                ('width', 0.5),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'LFSaw': {
        'parent': 'PureUGen',
        'methods': {
            'ar': [
                ('freq', 440),
                ('iphase', 0),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('freq', 440),
                ('iphase', 0),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'LFTri': {
        'parent': 'LFSaw',
        },
    'LPF': {
        'parent': 'Filter',
        'methods': {
            'ar': [
                ('in', 0),
                ('freq', 440),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('in', 0),
                ('freq', 440),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'LPZ1': {
        'parent': 'Filter',
        'methods': {
            'ar': [
                ('in', 0),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('in', 0),
                ('mul', 1),
                ('add', 0),
                ],
            'coeffs': [
                ('nil', None),
                ('this', None),
                ],
            },
        },
    'LPZ2': {
        'parent': 'Filter',
        'methods': {
            'ar': [
                ('in', 0),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('in', 0),
                ('mul', 1),
                ('add', 0),
                ],
            'coeffs': [
                ('nil', None),
                ('this', None),
                ],
            },
        },
    'LRHiCut': {
        'parent': 'BHiCut',
        'methods': {
            'ar': [
                ('in', None),
                ('freq', None),
                ('order', 2),
                ('maxOrder', 5),
                ],
            'kr': [
                ('in', None),
                ('freq', None),
                ('order', 2),
                ('maxOrder', 5),
                ],
            'magResponse': [
                ('freqs', 1000),
                ('sr', 44100),
                ('freq', 1200),
                ('order', 2),
                ],
            },
        },
    'LRLowCut': {
        'parent': 'BLowCut',
        'methods': {
            'ar': [
                ('in', None),
                ('freq', None),
                ('order', 2),
                ('maxOrder', 5),
                ],
            'kr': [
                ('in', None),
                ('freq', None),
                ('order', 2),
                ('maxOrder', 5),
                ],
            'magResponse': [
                ('freqs', 1000),
                ('sr', 44100),
                ('freq', 1200),
                ('order', 2),
                ],
            },
        },
    'Lag': {
        'parent': 'Filter',
        'methods': {
            'ar': [
                ('in', 0),
                ('lagTime', 0.1),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('in', 0),
                ('lagTime', 0.1),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'Lag2': {
        'parent': 'Lag',
        },
    'Lag2UD': {
        'parent': 'LagUD',
        },
    'Lag3': {
        'parent': 'Lag',
        },
    'Lag3UD': {
        'parent': 'LagUD',
        },
    'LagControl': {
        'parent': 'Control',
        'methods': {
            'kr': [
                ('values', None),
                ('lags', None),
                ],
            'ir': [
                ('nil', None),
                ('this', None),
                ],
            },
        },
    'LagIn': {
        'parent': 'AbstractIn',
        'methods': {
            'kr': [
                ('bus', 0),
                ('numChannels', 1),
                ('lag', 0.1),
                ],
            },
        },
    'LagUD': {
        'parent': 'Filter',
        'methods': {
            'ar': [
                ('in', 0),
                ('lagTimeU', 0.1),
                ('lagTimeD', 0.1),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('in', 0),
                ('lagTimeU', 0.1),
                ('lagTimeD', 0.1),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'LastValue': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('in', 0),
                ('diff', 0.01),
                ],
            'kr': [
                ('in', 0),
                ('diff', 0.01),
                ],
            },
        },
    'Latch': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('in', 0),
                ('trig', 0),
                ],
            'kr': [
                ('in', 0),
                ('trig', 0),
                ],
            },
        },
    'LatoocarfianC': {
        'parent': 'LatoocarfianN',
        },
    'LatoocarfianL': {
        'parent': 'LatoocarfianN',
        },
    'LatoocarfianN': {
        'parent': 'ChaosGen',
        'methods': {
            'equation': [],
            'ar': [
                ('freq', 22050),
                ('a', 1),
                ('b', 3),
                ('c', 0.5),
                ('d', 0.5),
                ('xi', 0.5),
                ('yi', 0.5),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'LeakDC': {
        'parent': 'Filter',
        'methods': {
            'ar': [
                ('in', 0),
                ('coef', 0.995),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('in', 0),
                ('coef', 0.9),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'LeastChange': {
        'parent': 'MostChange',
        },
    'Limiter': {
        'parent': 'Normalizer',
        },
    'LinCongC': {
        'parent': 'LinCongN',
        },
    'LinCongL': {
        'parent': 'LinCongN',
        },
    'LinCongN': {
        'parent': 'ChaosGen',
        'methods': {
            'equation': [],
            'ar': [
                ('freq', 22050),
                ('a', 1.1),
                ('c', 0.13),
                ('m', 1),
                ('xi', 0),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'LinExp': {
        'parent': 'PureUGen',
        'methods': {
            'ar': [
                ('in', 0),
                ('srclo', 0),
                ('srchi', 1),
                ('dstlo', 1),
                ('dsthi', 2),
                ],
            'kr': [
                ('in', 0),
                ('srclo', 0),
                ('srchi', 1),
                ('dstlo', 1),
                ('dsthi', 2),
                ],
            },
        },
    'LinPan2': {
        'parent': 'Pan2',
        },
    'LinRand': {
        'parent': 'UGen',
        'methods': {
            'new': [
                ('lo', 0),
                ('hi', 1),
                ('minmax', 0),
                ],
            },
        },
    'LinXFade2': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('inA', None),
                ('inB', 0),
                ('pan', 0),
                ('level', 1),
                ],
            'kr': [
                ('inA', None),
                ('inB', 0),
                ('pan', 0),
                ('level', 1),
                ],
            },
        },
    'Line': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('start', 0),
                ('end', 1),
                ('dur', 1),
                ('mul', 1),
                ('add', 0),
                ('doneAction', 0),
                ],
            'kr': [
                ('start', 0),
                ('end', 1),
                ('dur', 1),
                ('mul', 1),
                ('add', 0),
                ('doneAction', 0),
                ],
            },
        },
    'Linen': {
        'parent': 'UGen',
        'methods': {
            'kr': [
                ('gate', 1),
                ('attackTime', 0.01),
                ('susLevel', 1),
                ('releaseTime', 1),
                ('doneAction', 0),
                ],
            },
        },
    'ListDUGen': {
        'parent': 'DUGen',
        'methods': {
            'new': [
                ('list', None),
                ('repeats', 1),
                ],
            },
        },
    'LocalBuf': {
        'parent': 'WidthFirstUGen',
        'methods': {
            'new': [
                ('numFrames', 1),
                ('numChannels', 1),
                ],
            'new1': [
                ('rate', None),
                ('args', '[  ]'),
                ],
            'newFrom': [
                ('list', None),
                ],
            },
        },
    'LocalIn': {
        'parent': 'AbstractIn',
        'methods': {
            'ar': [
                ('numChannels', 1),
                ('default', 0),
                ],
            'kr': [
                ('numChannels', 1),
                ('default', 0),
                ],
            },
        },
    'LocalOut': {
        'parent': 'AbstractOut',
        'methods': {
            'ar': [
                ('channelsArray', None),
                ],
            'kr': [
                ('channelsArray', None),
                ],
            'numFixedArgs': [
                ('nil', None),
                ('this', None),
                ],
            },
        },
    'Logistic': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('chaosParam', 3),
                ('freq', 1000),
                ('init', 0.5),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('chaosParam', 3),
                ('freq', 1000),
                ('init', 0.5),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'LorenzL': {
        'parent': 'ChaosGen',
        'methods': {
            'equation': [],
            'ar': [
                ('freq', 22050),
                ('s', 10),
                ('r', 28),
                ('b', 2.667),
                ('h', 0.05),
                ('xi', 0.1),
                ('yi', 0),
                ('zi', 0),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'Loudness': {
        'parent': 'UGen',
        'methods': {
            'kr': [
                ('chain', None),
                ('smask', 0.25),
                ('tmask', 1),
                ],
            },
        },
    'MFCC': {
        'parent': 'MultiOutUGen',
        'methods': {
            'kr': [
                ('chain', None),
                ('numcoeff', 13),
                ],
            },
        },
    'MantissaMask': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('in', 0),
                ('bits', 3),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('in', 0),
                ('bits', 3),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'MaxLocalBufs': {
        'parent': 'UGen',
        'methods': {
            'new': [
                ('nil', None),
                ('this', None),
                ],
            },
        },
    'Median': {
        'parent': 'Filter',
        'methods': {
            'ar': [
                ('length', 3),
                ('in', 0),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('length', 3),
                ('in', 0),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'MidEQ': {
        'parent': 'Filter',
        'methods': {
            'ar': [
                ('in', 0),
                ('freq', 440),
                ('rq', 1),
                ('db', 0),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('in', 0),
                ('freq', 440),
                ('rq', 1),
                ('db', 0),
                ('mul', 1),
                ('add', 0),
                ],
            'coeffs': [
                ('sr', None),
                ('freq', 440),
                ('rq', 1),
                ('db', 0),
                ],
            },
        },
    'ModDif': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('x', 0),
                ('y', 0),
                ('mod', 1),
                ],
            'kr': [
                ('x', 0),
                ('y', 0),
                ('mod', 1),
                ],
            'ir': [
                ('x', 0),
                ('y', 0),
                ('mod', 1),
                ],
            },
        },
    'MoogFF': {
        'parent': 'Filter',
        'methods': {
            'ar': [
                ('in', None),
                ('freq', 100),
                ('gain', 2),
                ('reset', 0),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('in', None),
                ('freq', 100),
                ('gain', 2),
                ('reset', 0),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'MostChange': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('a', 0),
                ('b', 0),
                ],
            'kr': [
                ('a', 0),
                ('b', 0),
                ],
            },
        },
    'MouseButton': {
        'parent': 'UGen',
        'methods': {
            'kr': [
                ('minval', 0),
                ('maxval', 1),
                ('lag', 0.2),
                ],
            },
        },
    'MouseX': {
        'parent': 'UGen',
        'methods': {
            'kr': [
                ('minval', 0),
                ('maxval', 1),
                ('warp', 0),
                ('lag', 0.2),
                ],
            },
        },
    'MouseY': {
        'parent': 'MouseX',
        },
    'MulAdd': {
        'parent': 'UGen',
        'methods': {
            'new': [
                ('in', None),
                ('mul', 1),
                ('add', 0),
                ],
            'new1': [
                ('rate', None),
                ('in', None),
                ('mul', None),
                ('add', None),
                ],
            'canBeMulAdd': [
                ('in', None),
                ('mul', None),
                ('add', None),
                ],
            },
        },
    'MultiOutUGen': {
        'parent': 'UGen',
        'methods': {
            'newFromDesc': [
                ('rate', None),
                ('numOutputs', None),
                ('inputs', None),
                ],
            },
        },
    'NRand': {
        'parent': 'UGen',
        'methods': {
            'new': [
                ('lo', 0),
                ('hi', 1),
                ('n', 0),
                ],
            },
        },
    'Normalizer': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('in', 0),
                ('level', 1),
                ('dur', 0.01),
                ],
            },
        },
    'NumAudioBuses': {
        'parent': 'InfoUGenBase',
        },
    'NumBuffers': {
        'parent': 'InfoUGenBase',
        },
    'NumControlBuses': {
        'parent': 'InfoUGenBase',
        },
    'NumInputBuses': {
        'parent': 'InfoUGenBase',
        },
    'NumOutputBuses': {
        'parent': 'InfoUGenBase',
        },
    'NumRunningSynths': {
        'parent': 'InfoUGenBase',
        'methods': {
            'kr': [
                ('nil', None),
                ('this', None),
                ],
            },
        },
    'OffsetOut': {
        'parent': 'Out',
        'methods': {
            'kr': [
                ('nil', None),
                ('this', None),
                ],
            },
        },
    'OnePole': {
        'parent': 'Filter',
        'methods': {
            'ar': [
                ('in', 0),
                ('coef', 0.5),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('in', 0),
                ('coef', 0.5),
                ('mul', 1),
                ('add', 0),
                ],
            'coeffs': [
                ('sr', 44100),
                ('coef', 0.5),
                ],
            },
        },
    'OneZero': {
        'parent': 'OnePole',
        'methods': {
            'coeffs': [
                ('sr', 44100),
                ('coef', 0.5),
                ],
            },
        },
    'Onsets': {
        'parent': 'UGen',
        'methods': {
            'kr': [
                ('chain', None),
                ('threshold', 0.5),
                ('odftype', '"rcomplex"'),
                ('relaxtime', 1),
                ('floor', 0.1),
                ('mingap', 10),
                ('medianspan', 11),
                ('whtype', 1),
                ('rawodf', 0),
                ],
            },
        },
    'Osc': {
        'parent': 'PureUGen',
        'methods': {
            'ar': [
                ('bufnum', None),
                ('freq', 440),
                ('phase', 0),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('bufnum', None),
                ('freq', 440),
                ('phase', 0),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'OscN': {
        'parent': 'PureUGen',
        'methods': {
            'ar': [
                ('bufnum', None),
                ('freq', 440),
                ('phase', 0),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('bufnum', None),
                ('freq', 440),
                ('phase', 0),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'Out': {
        'parent': 'AbstractOut',
        'methods': {
            'ar': [
                ('bus', None),
                ('channelsArray', None),
                ],
            'kr': [
                ('bus', None),
                ('channelsArray', None),
                ],
            'numFixedArgs': [
                ('nil', None),
                ('this', None),
                ],
            },
        },
    'OutputProxy': {
        'parent': 'UGen',
        'methods': {
            'new': [
                ('rate', None),
                ('itsSourceUGen', None),
                ('index', None),
                ],
            },
        },
    'PSinGrain': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('freq', 440),
                ('dur', 0.2),
                ('amp', 1),
                ],
            },
        },
    'PV_Add': {
        'parent': 'PV_MagMul',
        },
    'PV_BinScramble': {
        'parent': 'PV_ChainUGen',
        'methods': {
            'new': [
                ('buffer', None),
                ('wipe', 0),
                ('width', 0.2),
                ('trig', 0),
                ],
            },
        },
    'PV_BinShift': {
        'parent': 'PV_ChainUGen',
        'methods': {
            'new': [
                ('buffer', None),
                ('stretch', 1),
                ('shift', 0),
                ('interp', 0),
                ],
            },
        },
    'PV_BinWipe': {
        'parent': 'PV_ChainUGen',
        'methods': {
            'new': [
                ('bufferA', None),
                ('bufferB', None),
                ('wipe', 0),
                ],
            },
        },
    'PV_BrickWall': {
        'parent': 'PV_ChainUGen',
        'methods': {
            'new': [
                ('buffer', None),
                ('wipe', 0),
                ],
            },
        },
    'PV_ChainUGen': {
        'parent': 'WidthFirstUGen',
        },
    'PV_ConformalMap': {
        'parent': 'PV_ChainUGen',
        'methods': {
            'new': [
                ('buffer', None),
                ('areal', 0),
                ('aimag', 0),
                ],
            },
        },
    'PV_Conj': {
        'parent': 'PV_MagSquared',
        },
    'PV_Copy': {
        'parent': 'PV_MagMul',
        },
    'PV_CopyPhase': {
        'parent': 'PV_MagMul',
        },
    'PV_Diffuser': {
        'parent': 'PV_ChainUGen',
        'methods': {
            'new': [
                ('buffer', None),
                ('trig', 0),
                ],
            },
        },
    'PV_Div': {
        'parent': 'PV_MagMul',
        },
    'PV_HainsworthFoote': {
        'parent': 'PV_ChainUGen',
        'methods': {
            'ar': [
                ('buffer', None),
                ('proph', 0),
                ('propf', 0),
                ('threshold', 1),
                ('waittime', 0.04),
                ],
            },
        },
    'PV_JensenAndersen': {
        'parent': 'PV_ChainUGen',
        'methods': {
            'ar': [
                ('buffer', None),
                ('propsc', 0.25),
                ('prophfe', 0.25),
                ('prophfc', 0.25),
                ('propsf', 0.25),
                ('threshold', 1),
                ('waittime', 0.04),
                ],
            },
        },
    'PV_LocalMax': {
        'parent': 'PV_MagAbove',
        },
    'PV_MagAbove': {
        'parent': 'PV_ChainUGen',
        'methods': {
            'new': [
                ('buffer', None),
                ('threshold', 0),
                ],
            },
        },
    'PV_MagBelow': {
        'parent': 'PV_MagAbove',
        },
    'PV_MagClip': {
        'parent': 'PV_MagAbove',
        },
    'PV_MagDiv': {
        'parent': 'PV_ChainUGen',
        'methods': {
            'new': [
                ('bufferA', None),
                ('bufferB', None),
                ('zeroed', 0.0001),
                ],
            },
        },
    'PV_MagFreeze': {
        'parent': 'PV_ChainUGen',
        'methods': {
            'new': [
                ('buffer', None),
                ('freeze', 0),
                ],
            },
        },
    'PV_MagMul': {
        'parent': 'PV_ChainUGen',
        'methods': {
            'new': [
                ('bufferA', None),
                ('bufferB', None),
                ],
            },
        },
    'PV_MagNoise': {
        'parent': 'PV_MagSquared',
        },
    'PV_MagShift': {
        'parent': 'PV_ChainUGen',
        'methods': {
            'new': [
                ('buffer', None),
                ('stretch', 1),
                ('shift', 0),
                ],
            },
        },
    'PV_MagSmear': {
        'parent': 'PV_ChainUGen',
        'methods': {
            'new': [
                ('buffer', None),
                ('bins', 0),
                ],
            },
        },
    'PV_MagSquared': {
        'parent': 'PV_ChainUGen',
        'methods': {
            'new': [
                ('buffer', None),
                ],
            },
        },
    'PV_Max': {
        'parent': 'PV_MagMul',
        },
    'PV_Min': {
        'parent': 'PV_MagMul',
        },
    'PV_Mul': {
        'parent': 'PV_MagMul',
        },
    'PV_PhaseShift': {
        'parent': 'PV_ChainUGen',
        'methods': {
            'new': [
                ('buffer', None),
                ('shift', None),
                ('integrate', 0),
                ],
            },
        },
    'PV_PhaseShift270': {
        'parent': 'PV_MagSquared',
        },
    'PV_PhaseShift90': {
        'parent': 'PV_MagSquared',
        },
    'PV_RandComb': {
        'parent': 'PV_ChainUGen',
        'methods': {
            'new': [
                ('buffer', None),
                ('wipe', 0),
                ('trig', 0),
                ],
            },
        },
    'PV_RandWipe': {
        'parent': 'PV_ChainUGen',
        'methods': {
            'new': [
                ('bufferA', None),
                ('bufferB', None),
                ('wipe', 0),
                ('trig', 0),
                ],
            },
        },
    'PV_RectComb': {
        'parent': 'PV_ChainUGen',
        'methods': {
            'new': [
                ('buffer', None),
                ('numTeeth', 0),
                ('phase', 0),
                ('width', 0.5),
                ],
            },
        },
    'PV_RectComb2': {
        'parent': 'PV_ChainUGen',
        'methods': {
            'new': [
                ('bufferA', None),
                ('bufferB', None),
                ('numTeeth', 0),
                ('phase', 0),
                ('width', 0.5),
                ],
            },
        },
    'PackFFT': {
        'parent': 'PV_ChainUGen',
        'methods': {
            'new': [
                ('chain', None),
                ('bufsize', None),
                ('magsphases', None),
                ('frombin', 0),
                ('tobin', None),
                ('zeroothers', 0),
                ],
            },
        },
    'Pan2': {
        'parent': 'MultiOutUGen',
        'methods': {
            'ar': [
                ('in', None),
                ('pos', 0),
                ('level', 1),
                ],
            'kr': [
                ('in', None),
                ('pos', 0),
                ('level', 1),
                ],
            },
        },
    'Pan4': {
        'parent': 'MultiOutUGen',
        'methods': {
            'ar': [
                ('in', None),
                ('xpos', 0),
                ('ypos', 0),
                ('level', 1),
                ],
            'kr': [
                ('in', None),
                ('xpos', 0),
                ('ypos', 0),
                ('level', 1),
                ],
            },
        },
    'PanAz': {
        'parent': 'MultiOutUGen',
        'methods': {
            'ar': [
                ('numChans', None),
                ('in', None),
                ('pos', 0),
                ('level', 1),
                ('width', 2),
                ('orientation', 0.5),
                ],
            'kr': [
                ('numChans', None),
                ('in', None),
                ('pos', 0),
                ('level', 1),
                ('width', 2),
                ('orientation', 0.5),
                ],
            },
        },
    'PanB': {
        'parent': 'MultiOutUGen',
        'methods': {
            'ar': [
                ('in', None),
                ('azimuth', 0),
                ('elevation', 0),
                ('gain', 1),
                ],
            'kr': [
                ('in', None),
                ('azimuth', 0),
                ('elevation', 0),
                ('gain', 1),
                ],
            },
        },
    'PanB2': {
        'parent': 'MultiOutUGen',
        'methods': {
            'ar': [
                ('in', None),
                ('azimuth', 0),
                ('gain', 1),
                ],
            'kr': [
                ('in', None),
                ('azimuth', 0),
                ('gain', 1),
                ],
            },
        },
    'PartConv': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('in', None),
                ('fftsize', None),
                ('irbufnum', None),
                ('mul', 1),
                ('add', 0),
                ],
            'calcNumPartitions': [
                ('fftsize', None),
                ('irbuffer', None),
                ],
            'calcBufSize': [
                ('fftsize', None),
                ('irbuffer', None),
                ],
            },
        },
    'Pause': {
        'parent': 'UGen',
        'methods': {
            'kr': [
                ('gate', None),
                ('id', None),
                ],
            },
        },
    'PauseSelf': {
        'parent': 'UGen',
        'methods': {
            'kr': [
                ('in', None),
                ],
            },
        },
    'PauseSelfWhenDone': {
        'parent': 'UGen',
        'methods': {
            'kr': [
                ('src', None),
                ],
            },
        },
    'Peak': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('in', 0),
                ('trig', 0),
                ],
            'kr': [
                ('in', 0),
                ('trig', 0),
                ],
            },
        },
    'PeakFollower': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('in', 0),
                ('decay', 0.999),
                ],
            'kr': [
                ('in', 0),
                ('decay', 0.999),
                ],
            },
        },
    'Phasor': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('trig', 0),
                ('rate', 1),
                ('start', 0),
                ('end', 1),
                ('resetPos', 0),
                ],
            'kr': [
                ('trig', 0),
                ('rate', 1),
                ('start', 0),
                ('end', 1),
                ('resetPos', 0),
                ],
            },
        },
    'PinkNoise': {
        'parent': 'WhiteNoise',
        },
    'Pitch': {
        'parent': 'MultiOutUGen',
        'methods': {
            'kr': [
                ('in', 0),
                ('initFreq', 440),
                ('minFreq', 60),
                ('maxFreq', 4000),
                ('execFreq', 100),
                ('maxBinsPerOctave', 16),
                ('median', 1),
                ('ampThreshold', 0.01),
                ('peakThreshold', 0.5),
                ('downSample', 1),
                ('clar', 0),
                ],
            },
        },
    'PitchShift': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('in', 0),
                ('windowSize', 0.2),
                ('pitchRatio', 1),
                ('pitchDispersion', 0),
                ('timeDispersion', 0),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'PlayBuf': {
        'parent': 'MultiOutUGen',
        'methods': {
            'ar': [
                ('numChannels', None),
                ('bufnum', 0),
                ('rate', 1),
                ('trigger', 1),
                ('startPos', 0),
                ('loop', 0),
                ('doneAction', 0),
                ],
            'kr': [
                ('numChannels', None),
                ('bufnum', 0),
                ('rate', 1),
                ('trigger', 1),
                ('startPos', 0),
                ('loop', 0),
                ('doneAction', 0),
                ],
            },
        },
    'Pluck': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('in', 0),
                ('trig', 1),
                ('maxdelaytime', 0.2),
                ('delaytime', 0.2),
                ('decaytime', 1),
                ('coef', 0.5),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'Poll': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('trig', None),
                ('in', None),
                ('label', None),
                ('trigid', -1),
                ],
            'kr': [
                ('trig', None),
                ('in', None),
                ('label', None),
                ('trigid', -1),
                ],
            'new': [
                ('trig', None),
                ('in', None),
                ('label', None),
                ('trigid', -1),
                ],
            'new1': [
                ('rate', None),
                ('trig', None),
                ('in', None),
                ('label', None),
                ('trigid', None),
                ],
            },
        },
    'Pulse': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('freq', 440),
                ('width', 0.5),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('freq', 440),
                ('width', 0.5),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'PulseCount': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('trig', 0),
                ('reset', 0),
                ],
            'kr': [
                ('trig', 0),
                ('reset', 0),
                ],
            },
        },
    'PulseDivider': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('trig', 0),
                ('div', 2),
                ('start', 0),
                ],
            'kr': [
                ('trig', 0),
                ('div', 2),
                ('start', 0),
                ],
            },
        },
    'PureMultiOutUGen': {
        'parent': 'MultiOutUGen',
        },
    'PureUGen': {
        'parent': 'UGen',
        },
    'QuadC': {
        'parent': 'QuadN',
        },
    'QuadL': {
        'parent': 'QuadN',
        },
    'QuadN': {
        'parent': 'ChaosGen',
        'methods': {
            'equation': [],
            'ar': [
                ('freq', 22050),
                ('a', 1),
                ('b', -1),
                ('c', -0.75),
                ('xi', 0),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'RHPF': {
        'parent': 'RLPF',
        },
    'RLPF': {
        'parent': 'Filter',
        'methods': {
            'ar': [
                ('in', 0),
                ('freq', 440),
                ('rq', 1),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('in', 0),
                ('freq', 440),
                ('rq', 1),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'RadiansPerSample': {
        'parent': 'InfoUGenBase',
        },
    'Ramp': {
        'parent': 'Lag',
        },
    'Rand': {
        'parent': 'UGen',
        'methods': {
            'new': [
                ('lo', 0),
                ('hi', 1),
                ],
            },
        },
    'RandID': {
        'parent': 'WidthFirstUGen',
        'methods': {
            'kr': [
                ('id', 0),
                ],
            'ir': [
                ('id', 0),
                ],
            },
        },
    'RandSeed': {
        'parent': 'WidthFirstUGen',
        'methods': {
            'ar': [
                ('trig', 0),
                ('seed', 56789),
                ],
            'kr': [
                ('trig', 0),
                ('seed', 56789),
                ],
            'ir': [
                ('trig', 0),
                ('seed', 56789),
                ],
            },
        },
    'RecordBuf': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('inputArray', None),
                ('bufnum', 0),
                ('offset', 0),
                ('recLevel', 1),
                ('preLevel', 0),
                ('run', 1),
                ('loop', 1),
                ('trigger', 1),
                ('doneAction', 0),
                ],
            'kr': [
                ('inputArray', None),
                ('bufnum', 0),
                ('offset', 0),
                ('recLevel', 1),
                ('preLevel', 0),
                ('run', 1),
                ('loop', 1),
                ('trigger', 1),
                ('doneAction', 0),
                ],
            },
        },
    'ReplaceOut': {
        'parent': 'Out',
        },
    'Resonz': {
        'parent': 'Filter',
        'methods': {
            'ar': [
                ('in', 0),
                ('freq', 440),
                ('bwr', 1),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('in', 0),
                ('freq', 440),
                ('bwr', 1),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'Ringz': {
        'parent': 'Filter',
        'methods': {
            'ar': [
                ('in', 0),
                ('freq', 440),
                ('decaytime', 1),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('in', 0),
                ('freq', 440),
                ('decaytime', 1),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'Rotate2': {
        'parent': 'MultiOutUGen',
        'methods': {
            'ar': [
                ('x', None),
                ('y', None),
                ('pos', 0),
                ],
            'kr': [
                ('x', None),
                ('y', None),
                ('pos', 0),
                ],
            },
        },
    'RunningMax': {
        'parent': 'Peak',
        },
    'RunningMin': {
        'parent': 'Peak',
        },
    'RunningSum': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('in', None),
                ('numsamp', 40),
                ],
            'kr': [
                ('in', None),
                ('numsamp', 40),
                ],
            'rms': [
                ('in', None),
                ('numsamp', 40),
                ],
            },
        },
    'SOS': {
        'parent': 'Filter',
        'methods': {
            'ar': [
                ('in', 0),
                ('a0', 0),
                ('a1', 0),
                ('a2', 0),
                ('b1', 0),
                ('b2', 0),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('in', 0),
                ('a0', 0),
                ('a1', 0),
                ('a2', 0),
                ('b1', 0),
                ('b2', 0),
                ('mul', 1),
                ('add', 0),
                ],
            'coeffs': [
                ('sr', 44100),
                ('a0', 0),
                ('a1', 0),
                ('a2', 0),
                ('b1', 0),
                ('b2', 0),
                ],
            },
        },
    'SampleDur': {
        'parent': 'InfoUGenBase',
        },
    'SampleRate': {
        'parent': 'InfoUGenBase',
        },
    'Saw': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('freq', 440),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('freq', 440),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'Schmidt': {
        'parent': 'InRange',
        },
    'ScopeOut': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('inputArray', None),
                ('bufnum', 0),
                ],
            'kr': [
                ('inputArray', None),
                ('bufnum', 0),
                ],
            },
        },
    'ScopeOut2': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('inputArray', None),
                ('scopeNum', 0),
                ('maxFrames', 4096),
                ('scopeFrames', None),
                ],
            'kr': [
                ('inputArray', None),
                ('scopeNum', 0),
                ('maxFrames', 4096),
                ('scopeFrames', None),
                ],
            },
        },
    'Select': {
        'parent': 'PureUGen',
        'methods': {
            'ar': [
                ('which', None),
                ('array', None),
                ],
            'kr': [
                ('which', None),
                ('array', None),
                ],
            },
        },
    'SelectL': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('which', None),
                ('array', None),
                ],
            'arSwitch': [
                ('which', None),
                ('array', None),
                ],
            'kr': [
                ('which', None),
                ('array', None),
                ],
            },
        },
    'SendPeakRMS': {
        'parent': 'UGen',
        'methods': {
            'kr': [
                ('sig', None),
                ('replyRate', 20),
                ('peakLag', 3),
                ('cmdName', '/reply'),
                ('replyID', -1),
                ],
            'ar': [
                ('sig', None),
                ('replyRate', 20),
                ('peakLag', 3),
                ('cmdName', '/reply'),
                ('replyID', -1),
                ],
            'new1': [
                ('rate', None),
                ('sig', None),
                ('replyRate', None),
                ('peakLag', None),
                ('cmdName', None),
                ('replyID', None),
                ],
            },
        },
    'SendReply': {
        'parent': 'SendTrig',
        'methods': {
            'kr': [
                ('trig', 0),
                ('cmdName', '/reply'),
                ('values', None),
                ('replyID', -1),
                ],
            'ar': [
                ('trig', 0),
                ('cmdName', '/reply'),
                ('values', None),
                ('replyID', -1),
                ],
            'new1': [
                ('rate', None),
                ('trig', 0),
                ('cmdName', '/reply'),
                ('values', None),
                ('replyID', -1),
                ],
            },
        },
    'SendTrig': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('in', 0),
                ('id', 0),
                ('value', 0),
                ],
            'kr': [
                ('in', 0),
                ('id', 0),
                ('value', 0),
                ],
            },
        },
    'SetBuf': {
        'parent': 'WidthFirstUGen',
        'methods': {
            'new': [
                ('buf', None),
                ('values', None),
                ('offset', 0),
                ],
            },
        },
    'SetResetFF': {
        'parent': 'PulseCount',
        },
    'Shaper': {
        'parent': 'Index',
        },
    'SharedIn': {
        'parent': 'AbstractIn',
        'methods': {
            'kr': [
                ('bus', 0),
                ('numChannels', 1),
                ],
            },
        },
    'SharedOut': {
        'parent': 'AbstractOut',
        'methods': {
            'kr': [
                ('bus', None),
                ('channelsArray', None),
                ],
            'numFixedArgs': [
                ('nil', None),
                ('this', None),
                ],
            },
        },
    'SinOsc': {
        'parent': 'PureUGen',
        'methods': {
            'ar': [
                ('freq', 440),
                ('phase', 0),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('freq', 440),
                ('phase', 0),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'SinOscFB': {
        'parent': 'PureUGen',
        'methods': {
            'ar': [
                ('freq', 440),
                ('feedback', 0),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('freq', 440),
                ('feedback', 0),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'Slew': {
        'parent': 'Filter',
        'methods': {
            'ar': [
                ('in', 0),
                ('up', 1),
                ('dn', 1),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('in', 0),
                ('up', 1),
                ('dn', 1),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'Slope': {
        'parent': 'Filter',
        'methods': {
            'ar': [
                ('in', 0),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('in', 0),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'SpecCentroid': {
        'parent': 'UGen',
        'methods': {
            'kr': [
                ('buffer', None),
                ],
            },
        },
    'SpecFlatness': {
        'parent': 'UGen',
        'methods': {
            'kr': [
                ('buffer', None),
                ],
            },
        },
    'SpecPcile': {
        'parent': 'UGen',
        'methods': {
            'kr': [
                ('buffer', None),
                ('fraction', 0.5),
                ('interpolate', 0),
                ],
            },
        },
    'Splay': {
        'parent': 'UGen',
        'methods': {
            'new1': [
                ('rate', None),
                ('spread', 1),
                ('level', 1),
                ('center', 0),
                ('levelComp', True),
                ('inArray', '[  ]'),
                ],
            'kr': [
                ('inArray', None),
                ('spread', 1),
                ('level', 1),
                ('center', 0),
                ('levelComp', True),
                ],
            'ar': [
                ('inArray', None),
                ('spread', 1),
                ('level', 1),
                ('center', 0),
                ('levelComp', True),
                ],
            'arFill': [
                ('n', None),
                ('function', None),
                ('spread', 1),
                ('level', 1),
                ('center', 0),
                ('levelComp', True),
                ],
            },
        },
    'SplayAz': {
        'parent': 'UGen',
        'methods': {
            'kr': [
                ('numChans', 4),
                ('inArray', None),
                ('spread', 1),
                ('level', 1),
                ('width', 2),
                ('center', 0),
                ('orientation', 0.5),
                ('levelComp', True),
                ],
            'ar': [
                ('numChans', 4),
                ('inArray', None),
                ('spread', 1),
                ('level', 1),
                ('width', 2),
                ('center', 0),
                ('orientation', 0.5),
                ('levelComp', True),
                ],
            'arFill': [
                ('numChans', 4),
                ('n', None),
                ('function', None),
                ('spread', 1),
                ('level', 1),
                ('width', 2),
                ('center', 0),
                ('orientation', 0.5),
                ('levelComp', True),
                ],
            },
        },
    'Spring': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('in', 0),
                ('spring', 1),
                ('damp', 0),
                ],
            'kr': [
                ('in', 0),
                ('spring', 1),
                ('damp', 0),
                ],
            },
        },
    'StandardL': {
        'parent': 'StandardN',
        },
    'StandardN': {
        'parent': 'ChaosGen',
        'methods': {
            'equation': [],
            'ar': [
                ('freq', 22050),
                ('k', 1),
                ('xi', 0.5),
                ('yi', 0),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'Stepper': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('trig', 0),
                ('reset', 0),
                ('min', 0),
                ('max', 7),
                ('step', 1),
                ('resetval', None),
                ],
            'kr': [
                ('trig', 0),
                ('reset', 0),
                ('min', 0),
                ('max', 7),
                ('step', 1),
                ('resetval', None),
                ],
            },
        },
    'StereoConvolution2L': {
        'parent': 'MultiOutUGen',
        'methods': {
            'ar': [
                ('in', None),
                ('kernelL', None),
                ('kernelR', None),
                ('trigger', 0),
                ('framesize', 2048),
                ('crossfade', 1),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'SubsampleOffset': {
        'parent': 'InfoUGenBase',
        },
    'Sum3': {
        'parent': 'UGen',
        'methods': {
            'new': [
                ('in0', None),
                ('in1', None),
                ('in2', None),
                ],
            'new1': [
                ('dummyRate', None),
                ('in0', None),
                ('in1', None),
                ('in2', None),
                ],
            },
        },
    'Sum4': {
        'parent': 'UGen',
        'methods': {
            'new': [
                ('in0', None),
                ('in1', None),
                ('in2', None),
                ('in3', None),
                ],
            'new1': [
                ('dummyRate', None),
                ('in0', None),
                ('in1', None),
                ('in2', None),
                ('in3', None),
                ],
            },
        },
    'Sweep': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('trig', 0),
                ('rate', 1),
                ],
            'kr': [
                ('trig', 0),
                ('rate', 1),
                ],
            },
        },
    'SyncSaw': {
        'parent': 'PureUGen',
        'methods': {
            'ar': [
                ('syncFreq', 440),
                ('sawFreq', 440),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('syncFreq', 440),
                ('sawFreq', 440),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'T2A': {
        'parent': 'K2A',
        'methods': {
            'ar': [
                ('in', 0),
                ('offset', 0),
                ],
            },
        },
    'T2K': {
        'parent': 'A2K',
        },
    'TBall': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('in', 0),
                ('g', 10),
                ('damp', 0),
                ('friction', 0.01),
                ],
            'kr': [
                ('in', 0),
                ('g', 10),
                ('damp', 0),
                ('friction', 0.01),
                ],
            },
        },
    'TDelay': {
        'parent': 'Trig1',
        },
    'TDuty': {
        'parent': 'Duty',
        'methods': {
            'ar': [
                ('dur', 1),
                ('reset', 0),
                ('level', 1),
                ('doneAction', 0),
                ('gapFirst', 0),
                ],
            'kr': [
                ('dur', 1),
                ('reset', 0),
                ('level', 1),
                ('doneAction', 0),
                ('gapFirst', 0),
                ],
            },
        },
    'TExpRand': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('lo', 0.01),
                ('hi', 1),
                ('trig', 0),
                ],
            'kr': [
                ('lo', 0.01),
                ('hi', 1),
                ('trig', 0),
                ],
            },
        },
    'TGrains': {
        'parent': 'MultiOutUGen',
        'methods': {
            'ar': [
                ('numChannels', None),
                ('trigger', 0),
                ('bufnum', 0),
                ('rate', 1),
                ('centerPos', 0),
                ('dur', 0.1),
                ('pan', 0),
                ('amp', 0.1),
                ('interp', 4),
                ],
            },
        },
    'TIRand': {
        'parent': 'UGen',
        'methods': {
            'kr': [
                ('lo', 0),
                ('hi', 127),
                ('trig', 0),
                ],
            'ar': [
                ('lo', 0),
                ('hi', 127),
                ('trig', 0),
                ],
            },
        },
    'TRand': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('lo', 0),
                ('hi', 1),
                ('trig', 0),
                ],
            'kr': [
                ('lo', 0),
                ('hi', 1),
                ('trig', 0),
                ],
            },
        },
    'TWindex': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('in', None),
                ('array', None),
                ('normalize', 0),
                ],
            'kr': [
                ('in', None),
                ('array', None),
                ('normalize', 0),
                ],
            },
        },
    'Tap': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('bufnum', 0),
                ('numChannels', 1),
                ('delaytime', 0.2),
                ],
            },
        },
    'Timer': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('trig', 0),
                ],
            'kr': [
                ('trig', 0),
                ],
            },
        },
    'ToggleFF': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('trig', 0),
                ],
            'kr': [
                ('trig', 0),
                ],
            },
        },
    'Trig': {
        'parent': 'Trig1',
        },
    'Trig1': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('in', 0),
                ('dur', 0.1),
                ],
            'kr': [
                ('in', 0),
                ('dur', 0.1),
                ],
            },
        },
    'TrigControl': {
        'parent': 'Control',
        },
    'TwoPole': {
        'parent': 'Filter',
        'methods': {
            'ar': [
                ('in', 0),
                ('freq', 440),
                ('radius', 0.8),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('in', 0),
                ('freq', 440),
                ('radius', 0.8),
                ('mul', 1),
                ('add', 0),
                ],
            'coeffs': [
                ('sr', 44100),
                ('freq', 440),
                ('radius', 0.8),
                ],
            },
        },
    'TwoZero': {
        'parent': 'TwoPole',
        'methods': {
            'coeffs': [
                ('sr', 44100),
                ('freq', 440),
                ('radius', 0.8),
                ],
            },
        },
    'UnaryOpUGen': {
        'parent': 'BasicOpUGen',
        'methods': {
            'new': [
                ('selector', None),
                ('a', None),
                ],
            },
        },
    'Unpack1FFT': {
        'parent': 'UGen',
        'methods': {
            'new': [
                ('chain', None),
                ('bufsize', None),
                ('binindex', None),
                ('whichmeasure', 0),
                ],
            },
        },
    'UnpackFFT': {
        'parent': 'MultiOutUGen',
        'methods': {
            'new': [
                ('chain', None),
                ('bufsize', None),
                ('frombin', 0),
                ('tobin', None),
                ],
            },
        },
    'VDiskIn': {
        'parent': 'MultiOutUGen',
        'methods': {
            'ar': [
                ('numChannels', None),
                ('bufnum', None),
                ('rate', 1),
                ('loop', 0),
                ('sendID', 0),
                ],
            },
        },
    'VOsc': {
        'parent': 'PureUGen',
        'methods': {
            'ar': [
                ('bufpos', None),
                ('freq', 440),
                ('phase', 0),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('bufpos', None),
                ('freq', 440),
                ('phase', 0),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'VOsc3': {
        'parent': 'PureUGen',
        'methods': {
            'ar': [
                ('bufpos', None),
                ('freq1', 110),
                ('freq2', 220),
                ('freq3', 440),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('bufpos', None),
                ('freq1', 110),
                ('freq2', 220),
                ('freq3', 440),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'VarLag': {
        'parent': 'Filter',
        'methods': {
            'ar': [
                ('in', 0),
                ('time', 0.1),
                ('curvature', 0),
                ('warp', 5),
                ('start', None),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('in', 0),
                ('time', 0.1),
                ('curvature', 0),
                ('warp', 5),
                ('start', None),
                ('mul', 1),
                ('add', 0),
                ],
            'new1': [
                ('rate', None),
                ('in', None),
                ('time', None),
                ('curvature', None),
                ('warp', None),
                ('start', None),
                ],
            },
        },
    'VarSaw': {
        'parent': 'PureUGen',
        'methods': {
            'ar': [
                ('freq', 440),
                ('iphase', 0),
                ('width', 0.5),
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('freq', 440),
                ('iphase', 0),
                ('width', 0.5),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'Vibrato': {
        'parent': 'PureUGen',
        'methods': {
            'ar': [
                ('freq', 440),
                ('rate', 6),
                ('depth', 0.02),
                ('delay', 0),
                ('onset', 0),
                ('rateVariation', 0.04),
                ('depthVariation', 0.1),
                ('iphase', 0),
                ],
            'kr': [
                ('freq', 440),
                ('rate', 6),
                ('depth', 0.02),
                ('delay', 0),
                ('onset', 0),
                ('rateVariation', 0.04),
                ('depthVariation', 0.1),
                ('iphase', 0),
                ],
            },
        },
    'Warp1': {
        'parent': 'MultiOutUGen',
        'methods': {
            'ar': [
                ('numChannels', 1),
                ('bufnum', 0),
                ('pointer', 0),
                ('freqScale', 1),
                ('windowSize', 0.2),
                ('envbufnum', -1),
                ('overlaps', 8),
                ('windowRandRatio', 0),
                ('interp', 1),
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'WhiteNoise': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('mul', 1),
                ('add', 0),
                ],
            'kr': [
                ('mul', 1),
                ('add', 0),
                ],
            },
        },
    'WidthFirstUGen': {
        'parent': 'UGen',
        },
    'Wrap': {
        'parent': 'InRange',
        },
    'WrapIndex': {
        'parent': 'Index',
        },
    'XFade2': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('inA', None),
                ('inB', 0),
                ('pan', 0),
                ('level', 1),
                ],
            'kr': [
                ('inA', None),
                ('inB', 0),
                ('pan', 0),
                ('level', 1),
                ],
            },
        },
    'XFadeRotate': {
        'parent': 'MultiOutUGen',
        'methods': {
            'ar': [
                ('n', 0),
                ('in', None),
                ],
            'kr': [
                ('n', 0),
                ('in', None),
                ],
            },
        },
    'XLine': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('start', 1),
                ('end', 2),
                ('dur', 1),
                ('mul', 1),
                ('add', 0),
                ('doneAction', 0),
                ],
            'kr': [
                ('start', 1),
                ('end', 2),
                ('dur', 1),
                ('mul', 1),
                ('add', 0),
                ('doneAction', 0),
                ],
            },
        },
    'XOut': {
        'parent': 'AbstractOut',
        'methods': {
            'ar': [
                ('bus', None),
                ('xfade', None),
                ('channelsArray', None),
                ],
            'kr': [
                ('bus', None),
                ('xfade', None),
                ('channelsArray', None),
                ],
            'numFixedArgs': [
                ('nil', None),
                ('this', None),
                ],
            },
        },
    'ZeroCrossing': {
        'parent': 'UGen',
        'methods': {
            'ar': [
                ('in', 0),
                ],
            'kr': [
                ('in', 0),
                ],
            },
        },
    }