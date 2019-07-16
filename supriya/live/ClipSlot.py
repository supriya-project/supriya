class ClipSlot:
    def __init__(self, *, clip=None, parent=None):
        self._clip = clip
        self._parent = parent

    def fire(self):
        if not self._parent:
            raise RuntimeError("Parent cannot be null")
        self.parent.fire(self)
