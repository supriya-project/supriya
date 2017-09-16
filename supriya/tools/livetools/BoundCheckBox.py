import urwid


class BoundCheckBox(urwid.CheckBox):

    def __init__(self, label, read_source, write_source):
        self._read_source = read_source
        self._write_source = write_source
        urwid.CheckBox.__init__(self, label)

    ### PRIVATE METHODS ###

    def keypress(self, size, key):
        key = super().keypress(size, key)
        self.write_source(self.get_state())
        return key

    def refresh(self):
        self.set_state(self.read_source())

    ### PUBLIC PROPERTIES ###

    @property
    def read_source(self):
        return self._read_source

    @property
    def write_source(self):
        return self._write_source
