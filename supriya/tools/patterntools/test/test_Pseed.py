# -*- encoding: utf-8 -*-
from abjad.tools import systemtools
from supriya.tools import patterntools


class TestCase(systemtools.TestCase):

    def test_indeterministic(self):
        """
        Unseeded patterns share no state, use stdlib RNG.
        """
        pattern_one = patterntools.Pwhite()
        pattern_two = patterntools.Pwhite()
        iterator_a = iter(pattern_one)
        iterator_b = iter(pattern_one)
        iterator_c = iter(pattern_two)
        iterator_d = iter(pattern_two)
        output_a = [next(iterator_a) for _ in range(10)]
        output_b = [next(iterator_b) for _ in range(10)]
        output_c = [next(iterator_c) for _ in range(10)]
        output_d = [next(iterator_d) for _ in range(10)]
        assert output_a != output_b
        assert output_a != output_c
        assert output_a != output_d
        assert output_b != output_c
        assert output_b != output_d
        assert output_c != output_d

    def test_deterministic(self):
        """
        Seeded patterns share no state, but are deterministic.
        """
        pattern_one = patterntools.Pwhite()
        pattern_two = patterntools.Pseed(patterntools.Pwhite())
        iterator_a = iter(pattern_one)
        iterator_b = iter(pattern_one)
        iterator_c = iter(pattern_two)
        iterator_d = iter(pattern_two)
        output_a = [next(iterator_a) for _ in range(10)]
        output_b = [next(iterator_b) for _ in range(10)]
        output_c = [next(iterator_c) for _ in range(10)]
        output_d = [next(iterator_d) for _ in range(10)]
        assert output_a != output_b
        assert output_a != output_c
        assert output_a != output_d
        assert output_b != output_c
        assert output_b != output_d
        assert output_c == output_d

    def test_interleaved(self):
        """
        Interleaving calls to seeded patterns is same as uninterleaved.
        """
        pattern = patterntools.Pseed(patterntools.Pwhite())
        iterator_a = iter(pattern)
        iterator_b = iter(pattern)
        iterator_c = iter(pattern)
        output_a, output_b = [], []
        for _ in range(10):
            output_a.append(next(iterator_a))
            output_b.append(next(iterator_b))
        output_c = [next(iterator_c) for _ in range(10)]
        assert output_a == output_b == output_c

    def test_seeds(self):
        """
        Different seed values yield different results, but still deterministic.
        """
        pattern_a = patterntools.Pseed(patterntools.Pwhite(), seed=0)
        pattern_b = patterntools.Pseed(patterntools.Pwhite(), seed=1)
        pattern_c = patterntools.Pseed(patterntools.Pwhite(), seed=2)
        iterator_a = iter(pattern_a)
        iterator_b = iter(pattern_b)
        iterator_c = iter(pattern_c)
        output_a = [next(iterator_a) for _ in range(10)]
        output_b = [next(iterator_b) for _ in range(10)]
        output_c = [next(iterator_c) for _ in range(10)]
        assert output_a != output_b
        assert output_b != output_c
        iterator_d = iter(pattern_a)
        iterator_e = iter(pattern_b)
        iterator_f = iter(pattern_c)
        output_d = [next(iterator_d) for _ in range(10)]
        output_e = [next(iterator_e) for _ in range(10)]
        output_f = [next(iterator_f) for _ in range(10)]
        assert output_d != output_e
        assert output_e != output_f
        assert output_a == output_d
        assert output_b == output_e
        assert output_c == output_f

    def test_nested(self):
        """
        The Pseed frame closest to the requesting frame determines which RNG
        is used during iteration.
        """
        pattern_one = patterntools.Pseed(patterntools.Pwhite(), seed=3)
        pattern_two = patterntools.Pwhite()
        pattern_two = patterntools.Pseed(pattern_two, seed=3)
        pattern_two = patterntools.Pseed(pattern_two, seed=2)
        pattern_two = patterntools.Pseed(pattern_two, seed=1)
        pattern_two = patterntools.Pseed(pattern_two, seed=0)
        iterator_one = iter(pattern_one)
        iterator_two = iter(pattern_two)
        output_one = [next(iterator_one) for _ in range(10)]
        output_two = [next(iterator_two) for _ in range(10)]
        assert output_one == output_two
