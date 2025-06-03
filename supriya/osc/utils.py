import pprint
from typing import Sequence

from ..ugens import decompile_synthdefs
from .messages import OscBundle, OscMessage


def format_messages(messages: Sequence[OscBundle | OscMessage]) -> str:
    """
    Format a sequence of OSC messages as a string.

    Provides a more concise means of verifying OSC contents in the test suite
    than comparing the messages directly.
    """

    def sanitize(list_):
        for i, x in enumerate(list_):
            if isinstance(x, bytes):
                try:
                    decompiled = decompile_synthdefs(x)
                    list_[i] = decompiled[0] if len(decompiled) == 1 else decompiled
                except Exception:
                    pass
            elif isinstance(x, list):
                sanitize(x)
        return list_

    lines: list[str] = []
    for message in messages:
        sanitized = sanitize(message.to_list())
        formatted = pprint.pformat(sanitized, width=120)
        for i, line in enumerate(formatted.splitlines()):
            if i == 0:
                prefix = "-"
            else:
                prefix = " "
            lines.append(f"{prefix} {line}")
    return "\n".join(lines)
