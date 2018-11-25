import supriya.nonrealtime


def test_01():
    """
    No containment.
    """
    session = supriya.nonrealtime.Session()
    with session.at(0):
        one = session.add_group(duration=10)
        session.add_group(duration=10)
    with session.at(0):
        entering, exiting, occupying, starting, stopping = one.inspect_children()
        assert entering == ()
        assert exiting == ()
        assert occupying == ()
        assert starting == ()
        assert stopping == ()
    with session.at(5):
        entering, exiting, occupying, starting, stopping = one.inspect_children()
        assert entering == ()
        assert exiting == ()
        assert occupying == ()
        assert starting == ()
        assert stopping == ()
    with session.at(10):
        entering, exiting, occupying, starting, stopping = one.inspect_children()
        assert entering == ()
        assert exiting == ()
        assert occupying == ()
        assert starting == ()
        assert stopping == ()


def test_02():
    """
    Full containment.
    """
    session = supriya.nonrealtime.Session()
    with session.at(0):
        one = session.add_group(duration=10)
        two = one.add_group(duration=10)
    with session.at(0):
        entering, exiting, occupying, starting, stopping = one.inspect_children()
        assert entering == ()
        assert exiting == ()
        assert occupying == ()
        assert starting == (two,)
        assert stopping == ()
    with session.at(5):
        entering, exiting, occupying, starting, stopping = one.inspect_children()
        assert entering == ()
        assert exiting == ()
        assert occupying == (two,)
        assert starting == ()
        assert stopping == ()
    with session.at(10):
        entering, exiting, occupying, starting, stopping = one.inspect_children()
        assert entering == ()
        assert exiting == ()
        assert occupying == ()
        assert starting == ()
        assert stopping == (two,)


def test_03():
    """
    Stop at midpoint.
    """
    session = supriya.nonrealtime.Session()
    with session.at(0):
        one = session.add_group(duration=10)
        two = one.add_group(duration=5)
    with session.at(0):
        entering, exiting, occupying, starting, stopping = one.inspect_children()
        assert entering == ()
        assert exiting == ()
        assert occupying == ()
        assert starting == (two,)
        assert stopping == ()
    with session.at(5):
        entering, exiting, occupying, starting, stopping = one.inspect_children()
        assert entering == ()
        assert exiting == ()
        assert occupying == ()
        assert starting == ()
        assert stopping == (two,)
    with session.at(10):
        entering, exiting, occupying, starting, stopping = one.inspect_children()
        assert entering == ()
        assert exiting == ()
        assert occupying == ()
        assert starting == ()
        assert stopping == ()


def test_04():
    """
    Start at midpoint.
    """
    session = supriya.nonrealtime.Session()
    with session.at(0):
        one = session.add_group(duration=10)
    with session.at(5):
        two = one.add_group(duration=5)
    with session.at(0):
        entering, exiting, occupying, starting, stopping = one.inspect_children()
        assert entering == ()
        assert exiting == ()
        assert occupying == ()
        assert starting == ()
        assert stopping == ()
    with session.at(5):
        entering, exiting, occupying, starting, stopping = one.inspect_children()
        assert entering == ()
        assert exiting == ()
        assert occupying == ()
        assert starting == (two,)
        assert stopping == ()
    with session.at(10):
        entering, exiting, occupying, starting, stopping = one.inspect_children()
        assert entering == ()
        assert exiting == ()
        assert occupying == ()
        assert starting == ()
        assert stopping == (two,)


def test_05():
    """
    Enter at midpoint.
    """
    session = supriya.nonrealtime.Session()
    with session.at(0):
        one = session.add_group(duration=10)
        two = session.add_group(duration=10)
    with session.at(5):
        one.move_node(two)
    with session.at(0):
        entering, exiting, occupying, starting, stopping = one.inspect_children()
        assert entering == ()
        assert exiting == ()
        assert occupying == ()
        assert starting == ()
        assert stopping == ()
    with session.at(5):
        entering, exiting, occupying, starting, stopping = one.inspect_children()
        assert entering == (two,)
        assert exiting == ()
        assert occupying == ()
        assert starting == ()
        assert stopping == ()
    with session.at(10):
        entering, exiting, occupying, starting, stopping = one.inspect_children()
        assert entering == ()
        assert exiting == ()
        assert occupying == ()
        assert starting == ()
        assert stopping == (two,)


def test_06():
    """
    Exit at midpoint.
    """
    session = supriya.nonrealtime.Session()
    with session.at(0):
        one = session.add_group(duration=10)
        two = one.add_group(duration=10)
    with session.at(5):
        session.move_node(two)
    with session.at(0):
        entering, exiting, occupying, starting, stopping = one.inspect_children()
        assert entering == ()
        assert exiting == ()
        assert occupying == ()
        assert starting == (two,)
        assert stopping == ()
    with session.at(5):
        entering, exiting, occupying, starting, stopping = one.inspect_children()
        assert entering == ()
        assert exiting == (two,)
        assert occupying == ()
        assert starting == ()
        assert stopping == ()
    with session.at(10):
        entering, exiting, occupying, starting, stopping = one.inspect_children()
        assert entering == ()
        assert exiting == ()
        assert occupying == ()
        assert starting == ()
        assert stopping == ()
