"""
Tools for modeling unit generators (UGens).
"""
from .A2K import A2K  # noqa
from .APF import APF  # noqa
from .AmpComp import AmpComp  # noqa
from .AmpCompA import AmpCompA  # noqa
from .Amplitude import Amplitude  # noqa
from .BAllPass import BAllPass  # noqa
from .BBandPass import BBandPass  # noqa
from .BBandStop import BBandStop  # noqa
from .BEQSuite import BEQSuite  # noqa
from .BHiCut import BHiCut  # noqa
from .BHiPass import BHiPass  # noqa
from .BHiShelf import BHiShelf  # noqa
from .BLowCut import BLowCut  # noqa
from .BLowPass import BLowPass  # noqa
from .BLowShelf import BLowShelf  # noqa
from .BPF import BPF  # noqa
from .BPZ2 import BPZ2  # noqa
from .BPeakEQ import BPeakEQ  # noqa
from .BRF import BRF  # noqa
from .BRZ2 import BRZ2  # noqa
from .Balance2 import Balance2  # noqa
from .Ball import Ball  # noqa
from .BeatTrack import BeatTrack  # noqa
from .BeatTrack2 import BeatTrack2  # noqa
from .BiPanB2 import BiPanB2  # noqa
from .Blip import Blip  # noqa
from .BlockSize import BlockSize  # noqa
from .BufChannels import BufChannels  # noqa
from .BufDur import BufDur  # noqa
from .BufFrames import BufFrames  # noqa
from .BufInfoUGenBase import BufInfoUGenBase  # noqa
from .BufRateScale import BufRateScale  # noqa
from .BufRd import BufRd  # noqa
from .BufSampleRate import BufSampleRate  # noqa
from .BufSamples import BufSamples  # noqa
from .BufWr import BufWr  # noqa
from .COsc import COsc  # noqa
from .Changed import Changed  # noqa
from .CheckBadValues import CheckBadValues  # noqa
from .ClearBuf import ClearBuf  # noqa
from .Clip import Clip  # noqa
from .ClipNoise import ClipNoise  # noqa
from .CoinGate import CoinGate  # noqa
from .Compander import Compander  # noqa
from .CompanderD import CompanderD  # noqa
from .ControlDur import ControlDur  # noqa
from .ControlRate import ControlRate  # noqa
from .Convolution import Convolution  # noqa
from .Convolution2 import Convolution2  # noqa
from .Convolution2L import Convolution2L  # noqa
from .Convolution3 import Convolution3  # noqa
from .DC import DC  # noqa
from .DUGen import DUGen  # noqa
from .Dbrown import Dbrown  # noqa
from .Dbufrd import Dbufrd  # noqa
from .Dbufwr import Dbufwr  # noqa
from .Decay import Decay  # noqa
from .Decay2 import Decay2  # noqa
from .DecodeB2 import DecodeB2  # noqa
from .DegreeToKey import DegreeToKey  # noqa
from .Demand import Demand  # noqa
from .DemandEnvGen import DemandEnvGen  # noqa
from .DetectSilence import DetectSilence  # noqa
from .Dgeom import Dgeom  # noqa
from .Dibrown import Dibrown  # noqa
from .DiskIn import DiskIn  # noqa
from .DiskOut import DiskOut  # noqa
from .Diwhite import Diwhite  # noqa
from .Done import Done  # noqa
from .Drand import Drand  # noqa
from .Dreset import Dreset  # noqa
from .Dseq import Dseq  # noqa
from .Dser import Dser  # noqa
from .Dseries import Dseries  # noqa
from .Dshuf import Dshuf  # noqa
from .Dstutter import Dstutter  # noqa
from .Dswitch import Dswitch  # noqa
from .Dswitch1 import Dswitch1  # noqa
from .Dunique import Dunique  # noqa
from .Duty import Duty  # noqa
from .Dwhite import Dwhite  # noqa
from .Dwrand import Dwrand  # noqa
from .Dxrand import Dxrand  # noqa
from .EnvGen import EnvGen  # noqa
from .ExpRand import ExpRand  # noqa
from .FFT import FFT  # noqa
from .FOS import FOS  # noqa
from .FSinOsc import FSinOsc  # noqa
from .Filter import Filter  # noqa
from .Fold import Fold  # noqa
from .Formlet import Formlet  # noqa
from .Free import Free  # noqa
from .FreeSelf import FreeSelf  # noqa
from .FreeSelfWhenDone import FreeSelfWhenDone  # noqa
from .FreeVerb import FreeVerb  # noqa
from .FreqShift import FreqShift  # noqa
from .Gate import Gate  # noqa
from .Gendy1 import Gendy1  # noqa
from .Gendy2 import Gendy2  # noqa
from .Gendy3 import Gendy3  # noqa
from .GrainBuf import GrainBuf  # noqa
from .GrainIn import GrainIn  # noqa
from .GrayNoise import GrayNoise  # noqa
from .HPF import HPF  # noqa
from .HPZ1 import HPZ1  # noqa
from .HPZ2 import HPZ2  # noqa
from .Hasher import Hasher  # noqa
from .Hilbert import Hilbert  # noqa
from .HilbertFIR import HilbertFIR  # noqa
from .IFFT import IFFT  # noqa
from .IRand import IRand  # noqa
from .Impulse import Impulse  # noqa
from .In import In  # noqa
from .InFeedback import InFeedback  # noqa
from .InRange import InRange  # noqa
from .Index import Index  # noqa
from .InfoUGenBase import InfoUGenBase  # noqa
from .Integrator import Integrator  # noqa
from .K2A import K2A  # noqa
from .KeyTrack import KeyTrack  # noqa
from .Klank import Klank  # noqa
from .LFClipNoise import LFClipNoise  # noqa
from .LFCub import LFCub  # noqa
from .LFDClipNoise import LFDClipNoise  # noqa
from .LFDNoise0 import LFDNoise0  # noqa
from .LFDNoise1 import LFDNoise1  # noqa
from .LFDNoise3 import LFDNoise3  # noqa
from .LFGauss import LFGauss  # noqa
from .LFPar import LFPar  # noqa
from .LFPulse import LFPulse  # noqa
from .LFSaw import LFSaw  # noqa
from .LFTri import LFTri  # noqa
from .LPF import LPF  # noqa
from .LPZ1 import LPZ1  # noqa
from .LPZ2 import LPZ2  # noqa
from .Lag import Lag  # noqa
from .Lag2 import Lag2  # noqa
from .Lag2UD import Lag2UD  # noqa
from .Lag3 import Lag3  # noqa
from .Lag3UD import Lag3UD  # noqa
from .LagUD import LagUD  # noqa
from .Latch import Latch  # noqa
from .LeakDC import LeakDC  # noqa
from .LeastChange import LeastChange  # noqa
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
from .Median import Median  # noqa
from .MidEQ import MidEQ  # noqa
from .Mix import Mix  # noqa
from .MoogFF import MoogFF  # noqa
from .MostChange import MostChange  # noqa
from .MouseButton import MouseButton  # noqa
from .MouseX import MouseX  # noqa
from .MouseY import MouseY  # noqa
from .MulAdd import MulAdd  # noqa
from .NRand import NRand  # noqa
from .Normalizer import Normalizer  # noqa
from .NumAudioBuses import NumAudioBuses  # noqa
from .NumBuffers import NumBuffers  # noqa
from .NumControlBuses import NumControlBuses  # noqa
from .NumInputBuses import NumInputBuses  # noqa
from .NumOutputBuses import NumOutputBuses  # noqa
from .NumRunningSynths import NumRunningSynths  # noqa
from .OffsetOut import OffsetOut  # noqa
from .OnePole import OnePole  # noqa
from .OneZero import OneZero  # noqa
from .Onsets import Onsets  # noqa
from .Out import Out  # noqa
from .PV_Add import PV_Add  # noqa
from .PV_BinScramble import PV_BinScramble  # noqa
from .PV_BinShift import PV_BinShift  # noqa
from .PV_BinWipe import PV_BinWipe  # noqa
from .PV_BrickWall import PV_BrickWall  # noqa
from .PV_ChainUGen import PV_ChainUGen  # noqa
from .PV_ConformalMap import PV_ConformalMap  # noqa
from .PV_Conj import PV_Conj  # noqa
from .PV_Copy import PV_Copy  # noqa
from .PV_CopyPhase import PV_CopyPhase  # noqa
from .PV_Diffuser import PV_Diffuser  # noqa
from .PV_Div import PV_Div  # noqa
from .PV_HainsworthFoote import PV_HainsworthFoote  # noqa
from .PV_JensenAndersen import PV_JensenAndersen  # noqa
from .PV_LocalMax import PV_LocalMax  # noqa
from .PV_MagAbove import PV_MagAbove  # noqa
from .PV_MagBelow import PV_MagBelow  # noqa
from .PV_MagClip import PV_MagClip  # noqa
from .PV_MagDiv import PV_MagDiv  # noqa
from .PV_MagFreeze import PV_MagFreeze  # noqa
from .PV_MagMul import PV_MagMul  # noqa
from .PV_MagNoise import PV_MagNoise  # noqa
from .PV_MagShift import PV_MagShift  # noqa
from .PV_MagSmear import PV_MagSmear  # noqa
from .PV_MagSquared import PV_MagSquared  # noqa
from .PV_Max import PV_Max  # noqa
from .PV_Min import PV_Min  # noqa
from .PV_Mul import PV_Mul  # noqa
from .PV_PhaseShift import PV_PhaseShift  # noqa
from .PV_PhaseShift90 import PV_PhaseShift90  # noqa
from .PV_PhaseShift270 import PV_PhaseShift270  # noqa
from .PV_RandComb import PV_RandComb  # noqa
from .PV_RandWipe import PV_RandWipe  # noqa
from .PV_RectComb import PV_RectComb  # noqa
from .PV_RectComb2 import PV_RectComb2  # noqa
from .Pan2 import Pan2  # noqa
from .Pan4 import Pan4  # noqa
from .PanAz import PanAz  # noqa
from .PanB import PanB  # noqa
from .PanB2 import PanB2  # noqa
from .Pause import Pause  # noqa
from .PauseSelf import PauseSelf  # noqa
from .PauseSelfWhenDone import PauseSelfWhenDone  # noqa
from .Peak import Peak  # noqa
from .PeakFollower import PeakFollower  # noqa
from .Phasor import Phasor  # noqa
from .PitchShift import PitchShift  # noqa
from .PlayBuf import PlayBuf  # noqa
from .Pluck import Pluck  # noqa
from .Poll import Poll  # noqa
from .PseudoUGen import PseudoUGen  # noqa
from .Pulse import Pulse  # noqa
from .RHPF import RHPF  # noqa
from .RLPF import RLPF  # noqa
from .RadiansPerSample import RadiansPerSample  # noqa
from .Ramp import Ramp  # noqa
from .Rand import Rand  # noqa
from .RandID import RandID  # noqa
from .RandSeed import RandSeed  # noqa
from .RecordBuf import RecordBuf  # noqa
from .ReplaceOut import ReplaceOut  # noqa
from .Ringz import Ringz  # noqa
from .Rotate2 import Rotate2  # noqa
from .RunningMax import RunningMax  # noqa
from .RunningMin import RunningMin  # noqa
from .RunningSum import RunningSum  # noqa
from .SOS import SOS  # noqa
from .SampleDur import SampleDur  # noqa
from .SampleRate import SampleRate  # noqa
from .Sanitize import Sanitize  # noqa
from .Saw import Saw  # noqa
from .Schmidt import Schmidt  # noqa
from .Select import Select  # noqa
from .SendPeakRMS import SendPeakRMS  # noqa
from .SendTrig import SendTrig  # noqa
from .Silence import Silence  # noqa
from .SinOsc import SinOsc  # noqa
from .Slew import Slew  # noqa
from .Slope import Slope  # noqa
from .SoundIn import SoundIn  # noqa
from .SpecCentroid import SpecCentroid  # noqa
from .SpecFlatness import SpecFlatness  # noqa
from .SpecPcile import SpecPcile  # noqa
from .Splay import Splay  # noqa
from .Spring import Spring  # noqa
from .SubsampleOffset import SubsampleOffset  # noqa
from .Sum3 import Sum3  # noqa
from .Sum4 import Sum4  # noqa
from .Sweep import Sweep  # noqa
from .SyncSaw import SyncSaw  # noqa
from .TBall import TBall  # noqa
from .TDelay import TDelay  # noqa
from .TExpRand import TExpRand  # noqa
from .TIRand import TIRand  # noqa
from .TRand import TRand  # noqa
from .TWindex import TWindex  # noqa
from .ToggleFF import ToggleFF  # noqa
from .Trig import Trig  # noqa
from .Trig1 import Trig1  # noqa
from .TwoPole import TwoPole  # noqa
from .TwoZero import TwoZero  # noqa
from .VDiskIn import VDiskIn  # noqa
from .VOsc import VOsc  # noqa
from .VOsc3 import VOsc3  # noqa
from .VarSaw import VarSaw  # noqa
from .Vibrato import Vibrato  # noqa
from .Warp1 import Warp1  # noqa
from .Wrap import Wrap  # noqa
from .WrapIndex import WrapIndex  # noqa
from .XFade2 import XFade2  # noqa
from .XLine import XLine  # noqa
from .XOut import XOut  # noqa
from .ZeroCrossing import ZeroCrossing  # noqa
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
from .delays import (
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
