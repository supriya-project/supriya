# -*- encoding: utf-8 -*-
import time
import uuid
from abjad.tools import systemtools
from supriya.tools import patterntools


class TestCase(systemtools.TestCase):

    class Event(object):

        def __init__(self, manifest, delta=None, save_execution_time=False):
            self.count = 0
            self.delta = delta
            self.manifest = manifest
            self.save_execution_time = save_execution_time

        def __call__(self, execution_time, scheduled_time):
            self.count += 1
            if self.save_execution_time:
                self.manifest.append((execution_time, scheduled_time))
            else:
                self.manifest.append(scheduled_time)
            if self.count == 4:
                return
            if self.delta:
                return self.delta
            return 0.1 * self.count

    def test_01(self):
        """
        Incremental deltas.
        """
        manifest = []
        event = self.Event(manifest)
        clock = patterntools.Clock()
        now = clock.schedule(event)
        time.sleep(1.)
        assert [round(_ - now, 6) for _ in manifest] == [0., 0.1, 0.3, 0.6]

    def test_02(self):
        """
        Constant deltas.
        """
        manifest = []
        event = self.Event(manifest, delta=0.25)
        clock = patterntools.Clock()
        now = clock.schedule(event)
        time.sleep(1.)
        assert [round(_ - now, 6) for _ in manifest] == [0., 0.25, 0.5, 0.75]

    def test_03(self):
        """
        Relative schedule with delta.
        """
        manifest = []
        event = self.Event(manifest)
        clock = patterntools.Clock()
        now = clock.schedule(event, 0.1)
        time.sleep(1.)
        assert [round(_ - now, 6) for _ in manifest] == [0.1, 0.2, 0.4, 0.7]

    def test_04(self):
        """
        Absolute scheduling.
        """
        manifest = []
        event = self.Event(manifest)
        clock = patterntools.Clock()
        now = time.time()
        clock.schedule(event, now + 0.25, absolute=True)
        time.sleep(1.)
        assert [round(_ - now, 6) for _ in manifest] == [0.25, 0.35, 0.55, 0.85]

    def test_05(self):
        """
        Interleaved (preempting) events.
        """
        manifest = []
        event_a = self.Event(manifest, delta=0.25)
        event_b = self.Event(manifest, delta=0.1)
        clock = patterntools.Clock()
        now = clock.schedule(event_a)
        clock.schedule(event_b, now + 0.1, absolute=True)
        time.sleep(1.)
        assert [round(_ - now, 6) for _ in manifest] == [0.0, 0.1, 0.2, 0.25, 0.3, 0.4, 0.5, 0.75]

    def test_06(self):
        """
        Resetting the clock.
        """
        manifest = []
        event = self.Event(manifest, delta=0.25)
        clock = patterntools.Clock()
        now = clock.schedule(event)
        time.sleep(0.4)
        clock.reset()
        assert [round(_ - now, 6) for _ in manifest] == [0., 0.25]

    def test_07(self):
        """
        Canceling by callable reference.
        """
        manifest = []
        event = self.Event(manifest, delta=0.25)
        clock = patterntools.Clock()
        now = clock.schedule(event)
        time.sleep(0.4)
        clock.cancel(event)
        assert [round(_ - now, 6) for _ in manifest] == [0., 0.25]

    def test_08(self):
        """
        Canceling by registry key.
        """
        manifest = []
        registry_key = uuid.uuid4()
        event = self.Event(manifest, delta=0.25)
        clock = patterntools.Clock()
        now = clock.schedule(event, registry_key=registry_key)
        time.sleep(0.4)
        clock.cancel(registry_key)
        assert [round(_ - now, 6) for _ in manifest] == [0., 0.25]

    def test_09(self):
        """
        If scheduled by registry key, must cancel by registry key.
        """
        manifest = []
        registry_key = uuid.uuid4()
        event = self.Event(manifest, delta=0.25)
        clock = patterntools.Clock()
        now = clock.schedule(event, registry_key=registry_key)
        time.sleep(0.4)
        clock.cancel(event)
        clock.cancel(9000)
        time.sleep(0.6)
        assert [round(_ - now, 6) for _ in manifest] == [0., 0.25, 0.5, 0.75]

    def test_10(self):
        """
        Negative relative scheduling.
        """
        manifest = []
        event = self.Event(manifest, delta=0.25, save_execution_time=True)
        clock = patterntools.Clock()
        now = clock.schedule(event, -0.1)
        time.sleep(1)
        assert [(round(x - now, 6), round(y - now, 3)) for x, y in manifest] == [
            (0.0, -0.1), (0.25, 0.25), (0.5, 0.5), (0.75, 0.75)]

    def test_11(self):
        """
        Negative absolute scheduling.
        """
        manifest = []
        event = self.Event(manifest, delta=0.25, save_execution_time=True)
        clock = patterntools.Clock()
        now = time.time()
        now = clock.schedule(event, now - 0.1, absolute=True)
        time.sleep(1)
        assert [(round(x - now, 6), round(y - now, 3)) for x, y in manifest] == [
            (0.0, -0.1), (0.25, 0.25), (0.5, 0.5), (0.75, 0.75)]

    def test_12(self):
        """
        Simultaneities.
        """
        manifest = []
        event_a = self.Event(manifest)
        event_b = self.Event(manifest)
        clock = patterntools.Clock()
        now = clock.schedule(event_a)
        now = clock.schedule(event_b)
        time.sleep(1.)
        assert [abs(round(_ - now, 2)) for _ in manifest] == [
            0.0, 0.0, 0.1, 0.1, 0.3, 0.3, 0.6, 0.6]

    def test_13(self):
        """
        Constant deltas, small and smaller.
        """
        manifest = []
        event = self.Event(manifest, delta=0.01, save_execution_time=True)
        clock = patterntools.Clock()
        now = clock.schedule(event)
        time.sleep(0.1)
        assert [(round(x - now, 6), round(y - now, 6)) for x, y in manifest] == [
            (0.0, 0.0), (0.01, 0.01), (0.02, 0.02), (0.03, 0.03)
            ]
        manifest = []
        event = self.Event(manifest, delta=0.001, save_execution_time=True)
        clock = patterntools.Clock()
        now = clock.schedule(event)
        time.sleep(0.1)
        assert [(round(x - now, 6), round(y - now, 6)) for x, y in manifest] == [
            (0.0, 0.0), (0.001, 0.001), (0.002, 0.002), (0.003, 0.003)
            ]
