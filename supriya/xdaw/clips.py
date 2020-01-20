from uuid import uuid4

from supriya.intervals import IntervalTree

from .bases import ApplicationObject


class Envelope:
    """
    An automation envelope, in a Clip or Timeline.
    """

    pass


class ClipObject(ApplicationObject):
    def __init__(self, *, name=None, uuid=None):
        ApplicationObject.__init__(self, name=name)
        self._uuid = uuid or uuid4()

    ### INITIALIZER ###

    def at(self, offset, start_delta=0.0, force_stop=False):
        pass

    ### PUBLIC PROPERTIES ###

    @property
    def uuid(self):
        return self._uuid


class Clip(ClipObject):

    ### INITIALIZER ###

    def __init__(
        self, *, duration=4 / 4, is_looping=True, name=None, notes=None, uuid=None
    ):
        ClipObject.__init__(self, name=name, uuid=uuid)
        self._duration = float(duration)
        self._is_looping = is_looping
        self._interval_tree = IntervalTree()
        self.add_notes(notes or [])

    ### SPECIAL METHODS ###

    def __iter__(self):
        return iter(self._interval_tree)

    def __len__(self):
        return len(self._interval_tree)

    def __str__(self):
        obj_name = type(self).__name__
        return "\n".join(
            [
                f"<{obj_name} {self.uuid}>",
                *(f"    {line}" for child in self for line in str(child).splitlines()),
            ]
        )

    ### PUBLIC METHODS ###

    def add_notes(self, notes):
        pass

    def at(self, offset, start_delta=0.0, force_stop=False):
        pass

    def remove_notes(self, notes):
        pass

    ### PUBLIC PROPERTIES ###

    @property
    def clip_start(self):
        return 0.0

    @property
    def clip_stop(self):
        return self._duration if self.is_looping else self._notes.stop_offset

    @property
    def duration(self):
        return self._duration

    @property
    def is_looping(self):
        return self._is_looping

    @property
    def is_playing(self):
        pass


class Slot(ApplicationObject):

    ### INITIALIZER ###

    def __init__(self, *, name=None, uuid=None):
        ApplicationObject.__init__(self, name=name)
        self._uuid = uuid or uuid4()

    ### SPECIAL METHODS ###

    def __str__(self):
        obj_name = type(self).__name__
        return "\n".join(
            [
                f"<{obj_name} {self.uuid}>",
                *(f"    {line}" for child in self for line in str(child).splitlines()),
            ]
        )

    ### PRIVATE METHODS ###

    def _set_clip(self, clip):
        pass

    ### PUBLIC METHODS ###

    def add_clip(self):
        self._set_clip(Clip())

    def duplicate_clip(self):
        pass

    def fire(self):
        if not self.application:
            return
        track = self.track
        if track is None:
            return
        track.fire(self)

    def move_clip(self, slot):
        slot._set_clip(self.clip)

    def remove_clip(self):
        self._set_clip(None)

    ### PUBLIC PROPERTIES ###

    @property
    def clip(self):
        return self[0]

    @property
    def track(self):
        from .tracks import Track

        for parent in self.parentage[1:]:
            if isinstance(parent, Track):
                return parent
        return None

    @property
    def uuid(self):
        return self._uuid


class Scene(ApplicationObject):

    ### INITIALIZER ###

    def __init__(self, *, name=None, uuid=None):
        ApplicationObject.__init__(self, name=name)
        self._uuid = uuid or uuid4()

    ### SPECIAL METHODS ###

    def __str__(self):
        obj_name = type(self).__name__
        return "\n".join(
            [
                f"<{obj_name} {self.uuid}>",
                *(f"    {line}" for child in self for line in str(child).splitlines()),
            ]
        )

    ### PUBLIC METHODS ###

    def delete(self):
        pass

    def duplicate(self):
        pass

    def fire(self):
        pass

    ### PUBLIC PROPERTIES ###

    @property
    def uuid(self):
        return self._uuid


class Timeline:
    pass
