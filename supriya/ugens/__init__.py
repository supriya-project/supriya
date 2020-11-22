"""
Tools for modeling unit generators (UGens).
"""
from .A2K import A2K  # noqa
from .AmpComp import AmpComp  # noqa
from .AmpCompA import AmpCompA  # noqa
from .Amplitude import Amplitude  # noqa
from .Balance2 import Balance2  # noqa
from .Ball import Ball  # noqa
from .BeatTrack import BeatTrack  # noqa
from .BeatTrack2 import BeatTrack2  # noqa
from .BiPanB2 import BiPanB2  # noqa
from .Blip import Blip  # noqa
from .BufRd import BufRd  # noqa
from .BufWr import BufWr  # noqa
from .CheckBadValues import CheckBadValues  # noqa
from .ClearBuf import ClearBuf  # noqa
from .ClipNoise import ClipNoise  # noqa
from .CoinGate import CoinGate  # noqa
from .Compander import Compander  # noqa
from .CompanderD import CompanderD  # noqa
from .Convolution import Convolution  # noqa
from .Convolution2 import Convolution2  # noqa
from .Convolution2L import Convolution2L  # noqa
from .Convolution3 import Convolution3  # noqa
from .DC import DC  # noqa
from .DecodeB2 import DecodeB2  # noqa
from .DiskIn import DiskIn  # noqa
from .DiskOut import DiskOut  # noqa
from .Done import Done  # noqa
from .EnvGen import EnvGen  # noqa
from .ExpRand import ExpRand  # noqa
from .FSinOsc import FSinOsc  # noqa
from .Free import Free  # noqa
from .FreeSelf import FreeSelf  # noqa
from .FreeSelfWhenDone import FreeSelfWhenDone  # noqa
from .FreeVerb import FreeVerb  # noqa
from .FreqShift import FreqShift  # noqa
from .Gendy1 import Gendy1  # noqa
from .Gendy2 import Gendy2  # noqa
from .Gendy3 import Gendy3  # noqa
from .GrainBuf import GrainBuf  # noqa
from .GrainIn import GrainIn  # noqa
from .GrayNoise import GrayNoise  # noqa
from .Hasher import Hasher  # noqa
from .Hilbert import Hilbert  # noqa
from .HilbertFIR import HilbertFIR  # noqa
from .IRand import IRand  # noqa
from .In import In  # noqa
from .InFeedback import InFeedback  # noqa
from .K2A import K2A  # noqa
from .KeyTrack import KeyTrack  # noqa
from .Klank import Klank  # noqa
from .LFClipNoise import LFClipNoise  # noqa
from .LFCub import LFCub  # noqa
from .LFDClipNoise import LFDClipNoise  # noqa
from .LFDNoise0 import LFDNoise0  # noqa
from .LFDNoise1 import LFDNoise1  # noqa
from .LFDNoise3 import LFDNoise3  # noqa
from .Limiter import Limiter  # noqa
from .LinExp import LinExp  # noqa
from .LinLin import LinLin  # noqa
from .LinRand import LinRand  # noqa
from .Line import Line  # noqa
from .Linen import Linen  # noqa
from .LocalBuf import LocalBuf  # noqa
from .LocalIn import LocalIn  # noqa
from .LocalOut import LocalOut  # noqa
from .Logistic import Logistic  # noqa
from .Loudness import Loudness  # noqa
from .MFCC import MFCC  # noqa
from .MantissaMask import MantissaMask  # noqa
from .MaxLocalBufs import MaxLocalBufs  # noqa
from .Mix import Mix  # noqa
from .MoogFF import MoogFF  # noqa
from .MouseButton import MouseButton  # noqa
from .MouseX import MouseX  # noqa
from .MouseY import MouseY  # noqa
from .MulAdd import MulAdd  # noqa
from .NRand import NRand  # noqa
from .Normalizer import Normalizer  # noqa
from .OffsetOut import OffsetOut  # noqa
from .Onsets import Onsets  # noqa
from .Out import Out  # noqa
from .Pan2 import Pan2  # noqa
from .Pan4 import Pan4  # noqa
from .PanAz import PanAz  # noqa
from .PanB import PanB  # noqa
from .PanB2 import PanB2  # noqa
from .Pause import Pause  # noqa
from .PauseSelf import PauseSelf  # noqa
from .PauseSelfWhenDone import PauseSelfWhenDone  # noqa
from .PitchShift import PitchShift  # noqa
from .PlayBuf import PlayBuf  # noqa
from .Pluck import Pluck  # noqa
from .Poll import Poll  # noqa
from .PseudoUGen import PseudoUGen  # noqa
from .Pulse import Pulse  # noqa
from .Rand import Rand  # noqa
from .RandID import RandID  # noqa
from .RandSeed import RandSeed  # noqa
from .RecordBuf import RecordBuf  # noqa
from .ReplaceOut import ReplaceOut  # noqa
from .Rotate2 import Rotate2  # noqa
from .RunningSum import RunningSum  # noqa
from .Sanitize import Sanitize  # noqa
from .Saw import Saw  # noqa
from .Silence import Silence  # noqa
from .SoundIn import SoundIn  # noqa
from .SpecCentroid import SpecCentroid  # noqa
from .SpecFlatness import SpecFlatness  # noqa
from .SpecPcile import SpecPcile  # noqa
from .Splay import Splay  # noqa
from .Spring import Spring  # noqa
from .Sum3 import Sum3  # noqa
from .Sum4 import Sum4  # noqa
from .TBall import TBall  # noqa
from .TExpRand import TExpRand  # noqa
from .TIRand import TIRand  # noqa
from .TRand import TRand  # noqa
from .TWindex import TWindex  # noqa
from .VDiskIn import VDiskIn  # noqa
from .Warp1 import Warp1  # noqa
from .XFade2 import XFade2  # noqa
from .XLine import XLine  # noqa
from .XOut import XOut  # noqa
from .beq import (
    BAllPass,
    BBandPass,
    BBandStop,
    BHiCut,
    BHiPass,
    BHiShelf,
    BLowCut,
    BLowPass,
    BLowShelf,
    BPeakEQ,
)
from .chaos import (
    CuspL,
    CuspN,
    FBSineC,
    FBSineL,
    FBSineN,
    GbmanL,
    GbmanN,
    HenonC,
    HenonL,
    HenonN,
    LatoocarfianC,
    LatoocarfianL,
    LatoocarfianN,
    LinCongC,
    LinCongL,
    LinCongN,
    LorenzL,
    QuadC,
    QuadL,
    QuadN,
    StandardL,
    StandardN,
)
from .delay import (
    AllpassC,
    AllpassL,
    AllpassN,
    BufAllpassC,
    BufAllpassL,
    BufAllpassN,
    BufCombC,
    BufCombL,
    BufCombN,
    BufDelayC,
    BufDelayL,
    BufDelayN,
    CombC,
    CombL,
    CombN,
    DelTapRd,
    DelTapWr,
    Delay1,
    Delay2,
    DelayC,
    DelayL,
    DelayN,
)
from .demand import (
    DUGen,
    Dbrown,
    Dbufrd,
    Dbufwr,
    Demand,
    DemandEnvGen,
    Dgeom,
    Dibrown,
    Diwhite,
    Drand,
    Dreset,
    Dseq,
    Dser,
    Dseries,
    Dshuf,
    Dstutter,
    Dswitch,
    Dswitch1,
    Dunique,
    Duty,
    Dwhite,
    Dwrand,
    Dxrand,
)
from .filters import (
    APF,
    BPF,
    BPZ2,
    BRF,
    BRZ2,
    FOS,
    HPF,
    HPZ1,
    HPZ2,
    LPF,
    LPZ1,
    LPZ2,
    RHPF,
    RLPF,
    SOS,
    Changed,
    Decay,
    Decay2,
    DetectSilence,
    Filter,
    Formlet,
    Integrator,
    Lag,
    Lag2,
    Lag2UD,
    Lag3,
    Lag3UD,
    LagUD,
    LeakDC,
    Median,
    MidEQ,
    OnePole,
    OneZero,
    Ramp,
    Ringz,
    Slew,
    Slope,
    TwoPole,
    TwoZero,
)
from .info import (
    BlockSize,
    BufChannels,
    BufDur,
    BufFrames,
    BufRateScale,
    BufSampleRate,
    BufSamples,
    ControlDur,
    ControlRate,
    NodeID,
    NumAudioBuses,
    NumBuffers,
    NumControlBuses,
    NumInputBuses,
    NumOutputBuses,
    NumRunningSynths,
    RadiansPerSample,
    SampleDur,
    SampleRate,
    SubsampleOffset,
)
from .noise import (
    BrownNoise,
    Crackle,
    Dust,
    Dust2,
    LFNoise0,
    LFNoise1,
    LFNoise2,
    PinkNoise,
    WhiteNoise,
)
from .osc import (
    COsc,
    DegreeToKey,
    Impulse,
    Index,
    LFGauss,
    LFPar,
    LFPulse,
    LFSaw,
    LFTri,
    Select,
    SinOsc,
    SyncSaw,
    VOsc,
    VOsc3,
    VarSaw,
    Vibrato,
    WrapIndex,
)
from .pv import (
    FFT,
    IFFT,
    PV_Add,
    PV_BinScramble,
    PV_BinShift,
    PV_BinWipe,
    PV_BrickWall,
    PV_ChainUGen,
    PV_ConformalMap,
    PV_Conj,
    PV_Copy,
    PV_CopyPhase,
    PV_Diffuser,
    PV_Div,
    PV_HainsworthFoote,
    PV_JensenAndersen,
    PV_LocalMax,
    PV_MagAbove,
    PV_MagBelow,
    PV_MagClip,
    PV_MagDiv,
    PV_MagFreeze,
    PV_MagMul,
    PV_MagNoise,
    PV_MagShift,
    PV_MagSmear,
    PV_MagSquared,
    PV_Max,
    PV_Min,
    PV_Mul,
    PV_PhaseShift,
    PV_PhaseShift90,
    PV_PhaseShift270,
    PV_RandComb,
    PV_RandWipe,
    PV_RectComb,
    PV_RectComb2,
)
from .triggers import (
    Clip,
    Fold,
    Gate,
    InRange,
    Latch,
    LeastChange,
    MostChange,
    Peak,
    PeakFollower,
    Phasor,
    RunningMax,
    RunningMin,
    Schmidt,
    SendPeakRMS,
    SendTrig,
    Sweep,
    TDelay,
    ToggleFF,
    Trig,
    Trig1,
    Wrap,
    ZeroCrossing,
)
