import pytest

import supriya.patterns
import supriya.system


def test___iter___01():
    pattern = supriya.patterns.Pwhite(minimum=0.0, maximum=1.0, repetitions=100)
    result = list(pattern)
    assert len(result) == 100
    assert all(0.0 <= x <= 1.0 for x in result)


def test___iter___02():
    pattern = supriya.patterns.Pwhite(minimum=-5, maximum=23, repetitions=127)
    result = list(pattern)
    assert len(result) == 127
    assert all(-5 <= x <= 23 for x in result)


def test_send_01():
    pattern = supriya.patterns.Pwhite()
    iterator = iter(pattern)
    next(iterator)
    with pytest.raises(StopIteration):
        iterator.send(True)


def test_send_02():
    pattern = supriya.patterns.Pwhite()
    iterator = iter(pattern)
    for _ in range(10):
        next(iterator)
    with pytest.raises(StopIteration):
        iterator.send(True)


def test_lazy_01():
    pattern = supriya.patterns.Pwhite(
        minimum=supriya.system.BindableFloat(0.25),
        maximum=supriya.system.BindableFloat(0.75),
    )
    iterator = iter(pattern)
    next(iterator)
