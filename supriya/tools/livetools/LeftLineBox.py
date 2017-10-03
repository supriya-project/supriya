import urwid


class LeftLineBox(urwid.WidgetDecoration, urwid.WidgetWrap):

    def __init__(
        self,
        original_widget,
        title='',
        bline='─',
        blcorner='└',
        brcorner='┘',
        lline='│',
        rline='│',
        tlcorner='┌',
        tline='─',
        trcorner='┐',
        ):
        tline, bline = urwid.Divider(tline), urwid.Divider(bline)
        lline, rline = urwid.SolidFill(lline), urwid.SolidFill(rline)
        tlcorner, trcorner = urwid.Text(tlcorner), urwid.Text(trcorner)
        blcorner, brcorner = urwid.Text(blcorner), urwid.Text(brcorner)
        self.title_widget = urwid.Text(self.format_title(title))
        self.tline_widget = urwid.Columns([
            (1, tline),
            ('flow', self.title_widget),
            tline,
        ])
        top = urwid.Columns([
            ('fixed', 1, tlcorner),
            self.tline_widget,
            ('fixed', 1, trcorner)
        ])
        middle_widget = original_widget
        middle = urwid.Columns([
            ('fixed', 1, lline),
            middle_widget,
            ('fixed', 1, rline),
        ], box_columns=[0, 2], focus_column=1)
        bottom = urwid.Columns([
            ('fixed', 1, blcorner), bline, ('fixed', 1, brcorner)
        ])
        pile = urwid.Pile([('flow', top), middle, ('flow', bottom)], focus_item=1)
        urwid.WidgetDecoration.__init__(self, original_widget)
        urwid.WidgetWrap.__init__(self, pile)

    def format_title(self, text):
        if len(text) > 0:
            return ' {} '.format(text)
        return ''

    def set_title(self, text):
        self.title_widget.set_text(self.format_title(text))
        self.tline_widget._invalidate()
