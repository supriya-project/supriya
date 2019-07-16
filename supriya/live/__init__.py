"""
Tools for performing live, including models of virtual mixers, instruments and
performance applications.

MIDI -> Track -> DeviceChain -> RequestBundle
Transport -> Track -> Clip -> DeviceChain -> RequestBundle
Transport -> Track -> Clip -> DeviceChain[...] -> DeviceChain[Arpeggiator] -> Transport
Transport -> DeviceChain[Arpeggiator] -> DeviceChain[...] -> RequestBundle

"""
from .Application import Application  # noqa
from .AudioEffect import AudioEffect  # noqa
from .Device import Device  # noqa
from .DeviceChain import DeviceChain  # noqa
from .Direct import Direct  # noqa
from .Instrument import Instrument  # noqa
from .MidiEffect import MidiEffect  # noqa
from .Mixer import Mixer  # noqa
from .PolyphonicVoicer import PolyphonicVoicer  # noqa
from .Rack import Rack  # noqa
from .Send import Send  # noqa
from .SendManager import SendManager  # noqa
from .Track import Track  # noqa
