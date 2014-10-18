# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class SoundFile(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_file_path',
        )

    ### INITIALIZER ###

    def __init__(self, file_path):
        import wavefile
        file_path = os.path.abspath(file_path)
        assert os.path.exists(file_path)
        self._file_path = file_path
        reader = wavefile.WaveReader(self.file_path)
        self._frame_count = reader.frames
        self._channel_count = reader.channels
        self._sample_rate = reader.samplerate

    ### PUBLIC PROPERTIES ###

    @property
    def channel_count(self):
        return self._channel_count

    @property
    def duration_in_seconds(self):
        return float(self._frame_count) / float(self._sample_rate)

    @property
    def file_path(self):
        return self._file_path

    @property
    def frame_count(self):
        return self._frame_count

    @property
    def sample_rate(self):
        return self._sample_rate