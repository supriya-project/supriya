import urwid


class BoundGainButton(urwid.Button):

    ### INITIALIZER ###

    def __init__(self, text, read_source, write_source):
        self._text = text
        self._gain = -96.0
        self._read_source = read_source
        self._write_source = write_source
        urwid.Button.__init__(self, self._build_label())

    ### PRIVATE METHODS ###

    def _build_label(self):
        return '{}: {:.2f}db'.format(self.text, float(self.gain))

    ### PUBLIC METHODS ###

    def keypress(self, size, key):
        key = super().keypress(size, key)
        if key in ('=', '+'):
            self.set_gain(self.gain + 3.0)
        elif key in ('-',):
            self.set_gain(self.gain - 3.0)
        self.write_source(self.gain)
        return key

    def refresh(self):
        self.set_gain(self.read_source())

    def set_gain(self, gain):
        gain = min(gain, 0.0)
        gain = max(gain, -96.0)
        self._gain = gain
        self.set_label(self._build_label())

    ### PUBLIC PROPERTIES ###

    @property
    def gain(self):
        return self._gain

    @property
    def read_source(self):
        return self._read_source

    @property
    def text(self):
        return self._text

    @property
    def write_source(self):
        return self._write_source
