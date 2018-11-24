import supriya.patterns


pattern_01 = supriya.patterns.Prand(["A", "B", "C"], repetitions=10)


pattern_02 = supriya.patterns.Prand(
    [
        supriya.patterns.Pseq(["A", "B"]),
        supriya.patterns.Pseq(["C", "D"]),
        supriya.patterns.Pseq(["E", "F"]),
    ],
    repetitions=4,
)


pattern_03 = supriya.patterns.Pseed(pattern_01)


pattern_04 = supriya.patterns.Pseed(pattern_02)


def test_01():
    results = []
    count = 10
    for _ in range(count):
        result = "".join(pattern_01)
        assert len(result) == pattern_01.repetitions
        results.append(result)
    assert len(set(results)) > 1


def test_02():
    results = []
    count = 10
    for _ in range(count):
        result = "".join(pattern_02)
        assert len(result) == pattern_02.repetitions * 2
        results.append(result)
    assert len(set(results)) > 1


def test_03():
    results = []
    count = 10
    for _ in range(count):
        result = "".join(pattern_03)
        assert len(result) == pattern_01.repetitions
        results.append(result)
    assert len(set(results)) == 1


def test_04():
    results = []
    count = 10
    for _ in range(count):
        result = "".join(pattern_04)
        assert len(result) == pattern_02.repetitions * 2
        results.append(result)
    assert len(set(results)) == 1
