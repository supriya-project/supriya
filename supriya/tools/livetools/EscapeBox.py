import urwid


class EscapeBox(urwid.LineBox):

    def __init__(self, original_widget, title=''):
        super().__init__(
            original_widget,
            title=title,
            tlcorner='╔',
            tline='═',
            lline='║',
            trcorner='╗',
            blcorner='╚',
            rline='║',
            bline='═',
            brcorner='╝',
            )
