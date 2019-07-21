import supriya.nonrealtime
import supriya.osc


def test_01():
    session = supriya.nonrealtime.Session()
    bus_group_one = session.add_bus_group()
    bus_group_two = session.add_bus_group(bus_count=2)
    with session.at(0):
        bus_group_one[0].set_(10)
    with session.at(3):
        bus_group_two[1].set_(20)
    with session.at(6):
        bus_group_two[0].set_(30)
    assert session.to_lists(10) == [
        [0.0, [["/c_set", 0, 10.0]]],
        [3.0, [["/c_set", 2, 20.0]]],
        [6.0, [["/c_set", 1, 30.0]]],
        [10.0, [[0]]],
    ]
