from uqbar.strings import normalize

import supriya


def test():
    osc_message = supriya.osc.OscMessage(
        "/foo",
        1,
        2.5,
        supriya.osc.OscBundle(
            contents=(
                supriya.osc.OscMessage("/bar", "baz", 3.0),
                supriya.osc.OscMessage("/ffff", False, True, None),
            )
        ),
        ["a", "b", ["c", "d"]],
    )
    assert repr(osc_message) == normalize(
        """
    OscMessage('/foo', 1, 2.5, OscBundle(
        contents=(
            OscMessage('/bar', 'baz', 3.0),
            OscMessage('/ffff', False, True, None),
        ),
    ), ['a', 'b', ['c', 'd']])
    """
    )
    assert str(osc_message) == normalize(
        """
    size 112
       0   2f 66 6f 6f  00 00 00 00  2c 69 66 62  5b 73 73 5b   |/foo....,ifb[ss[|
      16   73 73 5d 5d  00 00 00 00  00 00 00 01  40 20 00 00   |ss]]........@ ..|
      32   00 00 00 3c  23 62 75 6e  64 6c 65 00  00 00 00 00   |...<#bundle.....|
      48   00 00 00 01  00 00 00 14  2f 62 61 72  00 00 00 00   |......../bar....|
      64   2c 73 66 00  62 61 7a 00  40 40 00 00  00 00 00 10   |,sf.baz.@@......|
      80   2f 66 66 66  66 00 00 00  2c 46 54 4e  00 00 00 00   |/ffff...,FTN....|
      96   61 00 00 00  62 00 00 00  63 00 00 00  64 00 00 00   |a...b...c...d...|
    """
    )
    datagram = osc_message.to_datagram()
    new_osc_message = supriya.osc.OscMessage.from_datagram(datagram)
    assert osc_message == new_osc_message
    assert repr(new_osc_message) == normalize(
        """
    OscMessage('/foo', 1, 2.5, OscBundle(
        contents=(
            OscMessage('/bar', 'baz', 3.0),
            OscMessage('/ffff', False, True, None),
        ),
    ), ['a', 'b', ['c', 'd']])
    """
    )
