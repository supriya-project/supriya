import yaml
from supriya import patterntools
from supriya import systemtools
from supriya import utils


class TestCase(systemtools.TestCase):

    def test_01(self):
        string = utils.normalize_string("""
        pattern:
            type: Pwhite
        """)
        dict_ = yaml.load(string)
        pattern = patterntools.Pattern.from_dict(dict_['pattern'])
        self.compare_strings(
            format(pattern),
            """
            supriya.tools.patterntools.Pwhite(
                minimum=0.0,
                maximum=1.0,
                )
            """)

    def test_02(self):
        string = utils.normalize_string("""
        pattern:
            type: Pbind
            frequency: $args.frequency
            amplitude:
                type: Pwhite
            pan: $args.pan
            duration:
                type: Pwhite
                minimum: $args.duration_min
                maximum: $args.duration_max
        """)
        dict_ = yaml.load(string)
        namespaces = dict(
            args=dict(
                duration_max=11,
                duration_min=0.25,
                frequency=443,
                pan=0.1,
                )
            )
        pattern = patterntools.Pattern.from_dict(
            dict_['pattern'], namespaces=namespaces)
        self.compare_strings(
            format(pattern),
            """
            supriya.tools.patterntools.Pbind(
                amplitude=supriya.tools.patterntools.Pwhite(
                    minimum=0.0,
                    maximum=1.0,
                    ),
                duration=supriya.tools.patterntools.Pwhite(
                    minimum=0.25,
                    maximum=11,
                    ),
                frequency=443,
                pan=0.1,
                )
            """)

    def test_03(self):
        string = utils.normalize_string("""
        pattern:
            type: Pbind
            frequency: $args.frequency
            amplitude:
                type: Pwhite
            pan: $args.pan
            duration:
                type: Pwhite
                minimum: $args.duration_min
                maximum: $args.duration_max
            buffer_id: $buffers.birds
        """)
        dict_ = yaml.load(string)
        namespaces = dict(
            args=dict(
                duration_max=11,
                duration_min=0.25,
                frequency=443,
                pan=0.1,
                ),
            buffers=dict(
                birds=[1, 2, 3],
                ),
            )
        pattern = patterntools.Pattern.from_dict(
            dict_['pattern'], namespaces=namespaces)
        self.compare_strings(
            format(pattern),
            """
            supriya.tools.patterntools.Pbind(
                amplitude=supriya.tools.patterntools.Pwhite(
                    minimum=0.0,
                    maximum=1.0,
                    ),
                buffer_id=[1, 2, 3],
                duration=supriya.tools.patterntools.Pwhite(
                    minimum=0.25,
                    maximum=11,
                    ),
                frequency=443,
                pan=0.1,
                )
            """)

    def test_04(self):
        string = utils.normalize_string("""
        pattern:
            type: Pbind
            frequency: $args.frequency
            amplitude:
                type: Pwhite
            pan: $args.pan
            duration:
                type: Pwhite
                minimum: $args.duration_min
                maximum: $args.duration_max
        """)
        dict_ = yaml.load(string)
        namespaces = dict(
            args=systemtools.BindableNamespace(
                duration_max=11,
                duration_min=0.25,
                frequency=443,
                pan=0.1,
                )
            )
        pattern = patterntools.Pattern.from_dict(
            dict_['pattern'], namespaces=namespaces)
        self.compare_strings(
            format(pattern),
            """
            supriya.tools.patterntools.Pbind(
                amplitude=supriya.tools.patterntools.Pwhite(
                    minimum=0.0,
                    maximum=1.0,
                    ),
                duration=supriya.tools.patterntools.Pwhite(
                    minimum=supriya.tools.systemtools.BindableFloat(0.25),
                    maximum=supriya.tools.systemtools.BindableFloat(11.0),
                    ),
                frequency=supriya.tools.systemtools.BindableFloat(443.0),
                pan=supriya.tools.systemtools.BindableFloat(0.1),
                )
            """)
