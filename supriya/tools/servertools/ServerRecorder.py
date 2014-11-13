# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class ServerRecorder(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_server',
        )

    ### INITIALIZER ###

    def __init__(self, server):
        self._server = server

    ### PUBLIC METHODS ###

    def get_file_name(self):
        pass

    def pause(self):
        pass

    def prepare(self, path=None):
        pass

    def start(self, path=None):
        pass

    def stop(self):
        pass

    def unpause(self):
        pass

    ### PUBLIC PROPERTIES ###

    @property
    def record_node(self):
        pass

    @property
    def channel_count(self):
        pass

    @property
    def sample_format(self):
        pass

    @property
    def header_format(self):
        pass

    @property
    def current_channel_count(self):
        pass

    @property
    def current_sample_format(self):
        pass

    @property
    def current_header_format(self):
        pass