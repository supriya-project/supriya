import urwid


class FocusColumns(urwid.Columns):

    signals = ['modified']

    def _get_focus_position(self):
        if not self.widget_list:
            raise IndexError("No focus_position, Columns is empty")
        return self.contents.focus

    def _set_focus_position(self, position):
        try:
            if position < 0 or position >= len(self.contents):
                raise IndexError
        except (TypeError, IndexError):
            raise IndexError("No Columns child widget at position %s" % (position,))
        self.contents.focus = position
        self._emit('modified')

    focus_position = property(_get_focus_position, _set_focus_position)
