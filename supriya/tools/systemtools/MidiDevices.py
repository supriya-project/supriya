# -*- encoding: utf-8 -*-
import fnmatch
import os


class MidiDevices(object):

    ### SPECIAL METHODS ###

    def __getitem__(self, pattern):
        import supriya
        media_path = os.path.join(
            supriya.__path__[0],
            'mididevices',
            )
        result = []
        result = os.listdir(media_path)
        result = fnmatch.filter(result, pattern)
        result = [os.path.join(media_path, _) for _ in result]
        if len(result) == 1:
            return result[0]
        return result


MidiDevices = MidiDevices()