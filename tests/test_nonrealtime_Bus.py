import supriya.nonrealtime
import supriya.osc


def test_01():
    session = supriya.nonrealtime.Session()
    bus_one = session.add_bus()
    bus_two = session.add_bus()
    with session.at(0):
        bus_one.set_(10)
    with session.at(2):
        bus_one.set_(20)
        bus_two.set_(30)
    with session.at(3):
        bus_two.set_(40)
    assert session.to_osc_bundles() == [
        supriya.osc.OscBundle(
            timestamp=0.0, contents=(supriya.osc.OscMessage("/c_set", 0, 10.0),)
        ),
        supriya.osc.OscBundle(
            timestamp=2.0,
            contents=(supriya.osc.OscMessage("/c_set", 0, 20.0, 1, 30.0),),
        ),
        supriya.osc.OscBundle(
            timestamp=3.0,
            contents=(
                supriya.osc.OscMessage("/c_set", 1, 40.0),
                supriya.osc.OscMessage(0),
            ),
        ),
    ]
