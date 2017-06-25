import collections
from supriya.tools.systemtools import Enumeration
from supriya.tools.miditools.LogicalControl import LogicalControl


class LogicalView:

    class Mode(Enumeration):
        NON_MUTEX = 0
        MUTEX = 1

    def __init__(
        self,
        name,
        mode='non_mutex',
        visible=True,
        ):
        self.children = collections.OrderedDict()
        self.mode = self.Mode.from_expr(mode)
        self.name = name
        self.parent = None
        self.visible = visible

    def __getitem__(self, item):
        return self.children[item]

    def add_child(self, child):
        self.children[child.name] = child
        child.parent = self

    def debug(self, only_visible=None):
        parts = [
            'V',
            'name={}'.format(self.name),
            'mode={}'.format(self.mode.name.lower()),
            'visible={}'.format(str(self.visible).lower()),
            ]
        result = '<{}>'.format(' '.join(parts))
        result = [result]
        for child in self.children.values():
            if (
                only_visible and
                hasattr(child, 'visible') and
                not child.visible
                ):
                continue
            child_debug = child.debug(only_visible=only_visible)
            result.extend('    ' + _ for _ in child_debug.split('\n'))
        return '\n'.join(result)

    def yield_visible_controls(self):
        if not self.visible:
            return
        for child in self.children.values():
            if isinstance(child, type(self)) and child.visible:
                yield from child.yield_visible_controls()
            elif isinstance(child, LogicalControl):
                yield child
