# -*- encoding: utf-8 -*-
import random
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class RandomNumberGenerator(SupriyaObject):

    ### INITIALIZER ###

    def __init__(self, seed=1):
        self._seed = seed

    ### SPECIAL METHODS ###

    def __iter__(self):
        seed = self._seed
        while True:
            seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
            yield float(seed) / 0x7FFFFFFF

    ### PUBLIC METHODS ###

    @staticmethod
    def get_stdlib_rng():
        while True:
            yield random.random()

    ### PUBLIC PROPERTIES ###

    @property
    def seed(self):
        return self._seed
