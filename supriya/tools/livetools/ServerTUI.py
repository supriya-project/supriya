import urwid


class ServerTUI:

    ### INITIALIZER ###

    def __init__(self, server):
        self._server = server
        self._text_elements = {
            'actual_sample_rate': urwid.Text(''),
            'average_cpu_usage': urwid.Text(''),
            'group_count': urwid.Text(''),
            'peak_cpu_usage': urwid.Text(''),
            'synth_count': urwid.Text(''),
            'synthdef_count': urwid.Text(''),
            'target_sample_rate': urwid.Text(''),
            'ugen_count': urwid.Text(''),
        }
        self._header_box = urwid.LineBox(
            urwid.Padding(
                urwid.Columns([
                    self._text_elements['actual_sample_rate'],
                    self._text_elements['target_sample_rate'],
                    self._text_elements['average_cpu_usage'],
                    self._text_elements['peak_cpu_usage'],
                    ],
                    dividechars=2,
                    ),
                left=1,
                right=1,
                ),
            title='Server Status',
            )
        self._footer_box = urwid.LineBox(
            urwid.Padding(
                urwid.Columns([
                    self._text_elements['group_count'],
                    self._text_elements['synth_count'],
                    self._text_elements['ugen_count'],
                    self._text_elements['synthdef_count'],
                    ],
                    dividechars=2,
                    ),
                left=1,
                right=1,
                ),
            title='Server Status',
            )
        self.refresh()

    ### PUBLIC METHODS ###

    def refresh(self):
        status = self.server.status
        if status is None or not self.server.is_running:
            status = self.dummy_status
        else:
            status = status.to_dict()['server_status']
        templates = self.templates
        for key, text_element in self.text_elements.items():
            value = status[key]
            template = templates[key]
            text_element.set_text(template.format(value))

    ### PUBLIC PROPERTIES ###

    @property
    def dummy_status(self):
        return {
            'actual_sample_rate': 'N/A',
            'average_cpu_usage': 'N/A',
            'group_count': 0,
            'peak_cpu_usage': 'N/A',
            'synth_count': 0,
            'synthdef_count': 0,
            'target_sample_rate': 'N/A',
            'ugen_count': 0,
            }

    @property
    def footer_box(self):
        return self._footer_box

    @property
    def header_box(self):
        return self._header_box

    @property
    def server(self):
        return self._server

    @property
    def templates(self):
        return {
            'actual_sample_rate': 'Actual SR: {}',
            'average_cpu_usage': 'Average CPU: {}',
            'group_count': 'Groups: {}',
            'peak_cpu_usage': 'Peak CPU: {}',
            'synth_count': 'Synths: {}',
            'synthdef_count': 'SynthDefs: {}',
            'target_sample_rate': 'Target SR: {}',
            'ugen_count': 'Ugens: {}',
            }

    @property
    def text_elements(self):
        return self._text_elements
