import uqbar.strings
import yaml

import supriya.patterns


def test_01():
    string = uqbar.strings.normalize(
        """
    pattern:
        type: Pwhite
    """
    )
    dict_ = yaml.load(string)
    pattern = supriya.patterns.Pattern.from_dict(dict_["pattern"])
    assert repr(pattern) == uqbar.strings.normalize(
        """
        Pwhite()
        """
    )


def test_02():
    string = uqbar.strings.normalize(
        """
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
    """
    )
    dict_ = yaml.load(string)
    namespaces = dict(
        args=dict(duration_max=11, duration_min=0.25, frequency=443, pan=0.1)
    )
    pattern = supriya.patterns.Pattern.from_dict(
        dict_["pattern"], namespaces=namespaces
    )
    assert repr(pattern) == uqbar.strings.normalize(
        """
        Pbind(
            amplitude=Pwhite(),
            duration=Pwhite(
                maximum=11,
                minimum=0.25,
                ),
            frequency=443,
            pan=0.1,
            )
        """
    )


def test_03():
    string = uqbar.strings.normalize(
        """
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
    """
    )
    dict_ = yaml.load(string)
    namespaces = dict(
        args=dict(duration_max=11, duration_min=0.25, frequency=443, pan=0.1),
        buffers=dict(birds=[1, 2, 3]),
    )
    pattern = supriya.patterns.Pattern.from_dict(
        dict_["pattern"], namespaces=namespaces
    )
    assert repr(pattern) == uqbar.strings.normalize(
        """
        Pbind(
            amplitude=Pwhite(),
            buffer_id=[1, 2, 3],
            duration=Pwhite(
                maximum=11,
                minimum=0.25,
                ),
            frequency=443,
            pan=0.1,
            )
        """
    )


def test_04():
    string = uqbar.strings.normalize(
        """
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
    """
    )
    dict_ = yaml.load(string)
    namespaces = dict(
        args=supriya.system.BindableNamespace(
            duration_max=11, duration_min=0.25, frequency=443, pan=0.1
        )
    )
    pattern = supriya.patterns.Pattern.from_dict(
        dict_["pattern"], namespaces=namespaces
    )
    assert repr(pattern) == uqbar.strings.normalize(
        """
        Pbind(
            amplitude=Pwhite(),
            duration=Pwhite(
                maximum=BindableFloat(11.0),
                minimum=BindableFloat(0.25),
                ),
            frequency=BindableFloat(443.0),
            pan=BindableFloat(0.1),
            )
        """
    )
