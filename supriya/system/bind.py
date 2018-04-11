from supriya.system.Binding import Binding


def bind(
    source,
    target,
    source_range=None,
    target_range=None,
    clip_minimum=None,
    clip_maximum=None,
    exponent=None,
    symmetric=None,
    ):
    return Binding(
        source,
        target,
        source_range=source_range,
        target_range=target_range,
        clip_minimum=clip_minimum,
        clip_maximum=clip_maximum,
        exponent=exponent,
        symmetric=symmetric,
        )
