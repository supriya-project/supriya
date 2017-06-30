from abjad.tools import systemtools as abjad_systemtools
from supriya.tools import livetools


class TestCase(abjad_systemtools.TestCase):

    def test_01(self):
        mixer = livetools.Mixer(1, 1)
        mixer.add_track('foo')
        mixer.add_track('bar')
        mixer['foo'].add_synth_slot(
            'synth',
            frequency=443,
            )
        assert mixer.lookup('allow_multiple') is mixer.allow_multiple
        assert mixer.lookup('foo') is mixer['foo']
        assert mixer.lookup('bar') is mixer['bar']
        assert mixer.lookup('0') is mixer['foo']
        assert mixer.lookup('1') is mixer['bar']
        assert mixer.lookup('foo:synth') is mixer['foo']['synth']
        assert mixer.lookup('foo:synth:frequency') is \
            mixer['foo']['synth']['frequency']
        assert mixer.lookup('foo:synth.play') is mixer['foo']['synth'].play
