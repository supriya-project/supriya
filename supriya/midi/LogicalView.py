import collections
from supriya.midi.LogicalControl import LogicalControl


class LogicalView:

    ### INITIALIZER ###

    def __init__(self, name, device, is_mutex=False, visible=True):
        self.children = collections.OrderedDict()
        self.device = device
        self.is_mutex = bool(is_mutex)
        self.name = name
        self.parent = None
        self.visible = visible

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        return self.children[item]

    ### PRIVATE METHODS ###

    def _add_child(self, child):
        self.children[child.name] = child
        child.parent = self

    def _debug(self, only_visible=None):
        parts = [
            "V",
            "name={}".format(self.name),
            "is_mutex={}".format(str(self.is_mutex).lower()),
            "visible={}".format(str(self.visible).lower()),
        ]
        result = "<{}>".format(" ".join(parts))
        result = [result]
        for child in self.children.values():
            if only_visible and hasattr(child, "visible") and not child.visible:
                continue
            child_debug = child._debug(only_visible=only_visible)
            result.extend("    " + _ for _ in child_debug.split("\n"))
        return "\n".join(result)

    def _get_active_child(self):
        if not self.is_mutex:
            return
        for child in self.children.values():
            if child.value:
                return child

    def _yield_visible_controls(self):
        if not self.visible:
            return
        for child in self.children.values():
            if isinstance(child, type(self)) and child.visible:
                yield from child._yield_visible_controls()
            elif isinstance(child, LogicalControl):
                yield child
