import supriya.nonrealtime


def test_01():
    session = supriya.nonrealtime.Session()
    assert session.offsets == [float("-inf"), 0.0]
    assert session.duration == 0.0


def test_02():
    session = supriya.nonrealtime.Session()
    with session.at(0):
        session.add_group()
    assert session.offsets == [float("-inf"), 0.0, float("inf")]
    assert session.duration == 0.0


def test_03():
    session = supriya.nonrealtime.Session()
    with session.at(23.5):
        session.add_group()
    assert session.offsets == [float("-inf"), 0.0, 23.5, float("inf")]
    assert session.duration == 23.5


def test_04():
    session = supriya.nonrealtime.Session()
    with session.at(23.5):
        session.add_group(duration=1.0)
    assert session.offsets == [float("-inf"), 0.0, 23.5, 24.5]
    assert session.duration == 24.5


def test_05():
    session = supriya.nonrealtime.Session()
    with session.at(0):
        session.add_group()
    with session.at(23.5):
        session.add_group(duration=1.0)
    assert session.offsets == [float("-inf"), 0.0, 23.5, 24.5, float("inf")]
    assert session.duration == 24.5


def test_06():
    session = supriya.nonrealtime.Session(padding=11.0)
    assert session.offsets == [float("-inf"), 0.0]
    assert session.duration == 0.0


def test_07():
    session = supriya.nonrealtime.Session(padding=11.0)
    with session.at(0):
        session.add_group()
    assert session.offsets == [float("-inf"), 0.0, float("inf")]
    assert session.duration == 0.0


def test_08():
    session = supriya.nonrealtime.Session(padding=11.0)
    with session.at(23.5):
        session.add_group()
    assert session.offsets == [float("-inf"), 0.0, 23.5, float("inf")]
    assert session.duration == 34.5


def test_09():
    session = supriya.nonrealtime.Session(padding=11.0)
    with session.at(23.5):
        session.add_group(duration=1.0)
    assert session.offsets == [float("-inf"), 0.0, 23.5, 24.5]
    assert session.duration == 35.5


def test_10():
    session = supriya.nonrealtime.Session(padding=11.0)
    with session.at(0):
        session.add_group()
    with session.at(23.5):
        session.add_group(duration=1.0)
    assert session.offsets == [float("-inf"), 0.0, 23.5, 24.5, float("inf")]
    assert session.duration == 35.5
