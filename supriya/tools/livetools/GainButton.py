import urwid


class GainButton(urwid.Button):

    ### INITIALIZER ###

    def __init__(self, text):
        self._text = text
        self._gain = -96
        urwid.Button.__init__(self, self._build_label())

    ### PRIVATE METHODS ###

    def _build_label(self):
        return '{}: {:.2f}db'.format(self._text, float(self._gain))

    ### PUBLIC METHODS ###

    def keypress(self, size, key):
        key = super().keypress(size, key)
        if key in ('=', '+'):
            self.set_gain(self._gain + 3)
        elif key in ('-',):
            self.set_gain(self._gain - 3)
        return key

    def set_gain(self, gain):
        gain = min(gain, 0)
        gain = max(gain, -96)
        self._gain = gain
        self.set_label(self._build_label())
