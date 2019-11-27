from .bases import ApplicationObject


class Envelope:
    """
    An automation envelope, in a Clip or Timeline.
    """

    pass


class Clip(ApplicationObject):
    pass


class Scene(ApplicationObject):
    def delete(self):
        pass

    def duplicate(self):
        pass

    def fire(self):
        pass


class Slot(ApplicationObject):
    def add_clip(self):
        pass

    def duplicate_clip(self):
        pass

    def fire(self):
        pass

    def move_clip(self, slot):
        pass

    def remove_clip(self):
        pass


class Timeline:
    pass
