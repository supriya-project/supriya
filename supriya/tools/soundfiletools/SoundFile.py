# -*- encoding: utf-8 -*-
import os
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class SoundFile(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_channel_count',
        '_file_path',
        '_frame_count',
        '_sample_rate',
        )

    ### INITIALIZER ###

    def __init__(self, file_path):
        import wavefile
        file_path = os.path.abspath(file_path)
        assert os.path.exists(file_path)
        self._file_path = file_path
        with wavefile.WaveReader(self.file_path) as reader:
            self._frame_count = reader.frames
            self._channel_count = reader.channels
            self._sample_rate = reader.samplerate

    ### PUBLIC METHODS ###

    def at_frame(self, frames):
        import wavefile
        assert 0 <= frames <= self.frame_count
        with wavefile.WaveReader(self.file_path) as reader:
            reader.seek(frames)
            iterator = reader.read_iter(size=1)
            frame = next(iterator)
            return frame.transpose().tolist()[0]

    def at_percent(self, percent):
        import wavefile
        assert 0 <= percent <= 1
        frames = int(self.frame_count * percent)
        with wavefile.WaveReader(self.file_path) as reader:
            reader.seek(frames)
            iterator = reader.read_iter(size=1)
            frame = next(iterator)
            return frame.transpose().tolist()[0]

    def at_second(self, second):
        import wavefile
        assert 0 <= second <= self.seconds
        frames = second * self.sample_rate
        with wavefile.WaveReader(self.file_path) as reader:
            reader.seek(frames)
            iterator = reader.read_iter(size=1)
            frame = next(iterator)
            return frame.transpose().tolist()[0]

    ### PUBLIC PROPERTIES ###

    @property
    def channel_count(self):
        return self._channel_count

    @property
    def seconds(self):
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
