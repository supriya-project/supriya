import collections
from supriya.tools.systemtools import Enumeration
from supriya.tools.miditools.LogicalControl import LogicalControl


class View(object):

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

    def __str__(self):
        parts = [type(self).__name__]
        for key in ('name', 'mode', 'visible'):
            value = str(getattr(self, key)).lower()
            parts.append('{}={}'.format(key, value))
        result = '<{}>'.format(' '.join(parts))
        result = [result]
        for child in self.children.values():
            result.extend('    ' + _ for _ in str(child).split('\n'))
        return '\n'.join(result)

    def add_child(self, child):
        self.children[child.name] = child
        child.parent = self

    def yield_visible_controls(self):
        if not self.visible:
            return
        for child in self.children.values():
            if isinstance(child, type(self)) and child.visible:
                yield from child.yield_visible_controls()
            elif isinstance(child, LogicalControl):
                yield child
