import time
import uuid
import supriya.patterns


class Event:

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


def test_01():
    """
    Incremental deltas.
    """
    manifest = []
    event = Event(manifest)
    clock = supriya.patterns.Clock()
    now = clock.schedule(event)
    time.sleep(1.)
    assert [round(_ - now, 6) for _ in manifest] == [0., 0.1, 0.3, 0.6]


def test_02():
    """
    Constant deltas.
    """
    manifest = []
    event = Event(manifest, delta=0.25)
    clock = supriya.patterns.Clock()
    now = clock.schedule(event)
    time.sleep(1.)
    assert [round(_ - now, 6) for _ in manifest] == [0., 0.25, 0.5, 0.75]


def test_03():
    """
    Relative schedule with delta.
    """
    manifest = []
    event = Event(manifest)
    clock = supriya.patterns.Clock()
    now = clock.schedule(event, 0.1)
    time.sleep(1.)
    assert [round(_ - now, 6) for _ in manifest] == [0.1, 0.2, 0.4, 0.7]


def test_04():
    """
    Absolute scheduling.
    """
    manifest = []
    event = Event(manifest)
    clock = supriya.patterns.Clock()
    now = time.time()
    clock.schedule(event, now + 0.25, absolute=True)
    time.sleep(1.)
    assert [round(_ - now, 6) for _ in manifest] == [0.25, 0.35, 0.55, 0.85]


def test_05():
    """
    Interleaved (preempting) events.
    """
    manifest = []
    event_a = Event(manifest, delta=0.25)
    event_b = Event(manifest, delta=0.1)
    clock = supriya.patterns.Clock()
    now = clock.schedule(event_a)
    clock.schedule(event_b, now + 0.1, absolute=True)
    time.sleep(1.)
    assert [round(_ - now, 6) for _ in manifest] == [0.0, 0.1, 0.2, 0.25, 0.3, 0.4, 0.5, 0.75]


def test_06():
    """
    Resetting the clock.
    """
    manifest = []
    event = Event(manifest, delta=0.25)
    clock = supriya.patterns.Clock()
    now = clock.schedule(event)
    time.sleep(0.4)
    clock.reset()
    assert [round(_ - now, 6) for _ in manifest] == [0., 0.25]


def test_07():
    """
    Canceling by callable reference.
    """
    manifest = []
    event = Event(manifest, delta=0.25)
    clock = supriya.patterns.Clock()
    now = clock.schedule(event)
    time.sleep(0.4)
    clock.cancel(event)
    assert [round(_ - now, 6) for _ in manifest] == [0., 0.25]


def test_08():
    """
    Canceling by registry key.
    """
    manifest = []
    registry_key = uuid.uuid4()
    event = Event(manifest, delta=0.25)
    clock = supriya.patterns.Clock()
    now = clock.schedule(event, registry_key=registry_key)
    time.sleep(0.4)
    clock.cancel(registry_key)
    assert [round(_ - now, 6) for _ in manifest] == [0., 0.25]


def test_09():
    """
    If scheduled by registry key, must cancel by registry key.
    """
    manifest = []
    registry_key = uuid.uuid4()
    event = Event(manifest, delta=0.25)
    clock = supriya.patterns.Clock()
    now = clock.schedule(event, registry_key=registry_key)
    time.sleep(0.4)
    clock.cancel(event)
    clock.cancel(9000)
    time.sleep(0.6)
    assert [round(_ - now, 6) for _ in manifest] == [0., 0.25, 0.5, 0.75]


def test_10():
    """
    Negative relative scheduling.
    """
    manifest = []
    event = Event(manifest, delta=0.25, save_execution_time=True)
    clock = supriya.patterns.Clock()
    now = clock.schedule(event, -0.1)
    time.sleep(1)
    assert [(round(x - now, 6), round(y - now, 3)) for x, y in manifest] == [
        (0.0, -0.1), (0.25, 0.25), (0.5, 0.5), (0.75, 0.75)]


def test_11():
    """
    Negative absolute scheduling.
    """
    manifest = []
    event = Event(manifest, delta=0.25, save_execution_time=True)
    clock = supriya.patterns.Clock()
    now = time.time()
    now = clock.schedule(event, now - 0.1, absolute=True)
    time.sleep(1)
    assert [(round(x - now, 6), round(y - now, 3)) for x, y in manifest] == [
        (0.0, -0.1), (0.25, 0.25), (0.5, 0.5), (0.75, 0.75)]


def test_12():
    """
    Simultaneities.
    """
    manifest = []
    event_a = Event(manifest)
    event_b = Event(manifest)
    clock = supriya.patterns.Clock()
    now = clock.schedule(event_a)
    now = clock.schedule(event_b)
    time.sleep(1.)
    assert [abs(round(_ - now, 2)) for _ in manifest] == [
        0.0, 0.0, 0.1, 0.1, 0.3, 0.3, 0.6, 0.6]


def test_13():
    """
    Constant deltas, small and smaller.
    """
    manifest = []
    event = Event(manifest, delta=0.01, save_execution_time=True)
    clock = supriya.patterns.Clock()
    now = clock.schedule(event)
    time.sleep(0.1)
    assert [(round(x - now, 6), round(y - now, 6)) for x, y in manifest] == [
        (0.0, 0.0), (0.01, 0.01), (0.02, 0.02), (0.03, 0.03)
        ]
    manifest = []
    event = Event(manifest, delta=0.001, save_execution_time=True)
    clock = supriya.patterns.Clock()
    now = clock.schedule(event)
    time.sleep(0.1)
    assert [(round(x - now, 6), round(y - now, 6)) for x, y in manifest] == [
        (0.0, 0.0), (0.001, 0.001), (0.002, 0.002), (0.003, 0.003)
        ]
