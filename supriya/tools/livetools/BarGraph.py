import urwid


class BarGraph(urwid.Widget):

    __metaclass__ = urwid.BarGraphMeta
    _sizing = frozenset([urwid.BOX])
    ignore_focus = False

    _horizontal_characters = (
        '\u2588',
        '\u258F',
        '\u258E',
        '\u258D',
        '\u258C',
        '\u258B',
        '\u258A',
        '\u2589',
        )

    _vertical_characters = (
        '\u2588',
        '\u2581',
        '\u2582',
        '\u2583',
        '\u2584',
        '\u2585',
        '\u2586',
        '\u2587',
        )

    def __init__(self, orientation='vertical'):
        self.set_data([])
        self.set_orientation(orientation)

    @staticmethod
    def _calculate_bar_sizes(maximum_size, bar_count):
        if bar_count >= maximum_size:
            return [1] * maximum_size
        bar_sizes = []
        grow = maximum_size
        remain = bar_count
        for bar in range(bar_count):
            bar_size = int(float(grow) / remain + 0.5)
            bar_sizes.append(bar_size)
            grow -= bar_size
            remain -= 1
        return bar_sizes

    @classmethod
    def _calculate_bar_text(cls, size, value, characters):
        div, mod = divmod(int(value * size * 8), 8)
        div_string = ('\u2588' * div)
        mod_string = characters[mod] if mod else ''
        space_string = ' ' * (size - div - (mod > 0))
        return '{}{}{}'.format(div_string, mod_string, space_string)

    def set_data(self, data, minimum=0.0, maximum=1.0):
        self._data = tuple(data)
        self._minimum = min(minimum, maximum)
        self._maximum = max(minimum, maximum)
        self._invalidate()

    def set_orientation(self, orientation):
        assert orientation in ('vertical', 'horizontal')
        self._orientation = orientation
        if orientation == 'vertical':
            self._characters = self._vertical_characters
        else:
            self._characters = self._horizontal_characters
        self._invalidate()

    def render(self, size, focus=False):
        columns, rows = size
        data, minimum, maximum = self._data, self._minimum, self._maximum
        spread = maximum - minimum
        if not data:
            data = [minimum]
        if self._orientation == 'vertical':
            dimension_a, dimension_b = columns, rows
        else:
            dimension_a, dimension_b = rows, columns
        bar_sizes = self._calculate_bar_sizes(dimension_a, len(data))
        strings = []
        for bar_size, value in zip(bar_sizes, data):
            value = float(value)
            value = (min(max(value, minimum), maximum) - minimum) / spread
            string = self._calculate_bar_text(
                dimension_b, value, self._characters)
            for _ in range(bar_size):
                strings.append(string)
        if self._orientation == 'vertical':
            strings = [''.join(_) for _ in zip(*strings)]
            strings.reverse()
        canvas_elements = []
        for string in strings:
            text_element = urwid.Text(string)
            canvas = text_element.render((columns,))
            canvas_elements.append((canvas, None, False))
        return urwid.CanvasCombine(canvas_elements)

    def selectable(self):
        return False
