class Say(object):

    ### CLASS VARIABLES ###

    _voices = (
        'Alex', 'Alice', 'Alva', 'Amelie', 'Anna', 'Carmit', 'Damayanti',
        'Daniel', 'Diego', 'Ellen', 'Fiona', 'Fred', 'Ioana', 'Joana', 'Jorge',
        'Juan', 'Kanya', 'Karen', 'Kyoko', 'Laura', 'Lekha', 'Luca', 'Luciana',
        'Maged', 'Mariska', 'Mei-Jia', 'Melina', 'Milena', 'Moira', 'Monica',
        'Nora', 'Paulina', 'Samantha', 'Sara', 'Satu', 'Sin-ji', 'Tessa',
        'Thomas', 'Ting-Ting', 'Veena', 'Victoria', 'Xander', 'Yelda', 'Yuna',
        'Yuri', 'Zosia', 'Zuzana',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        text,
        bit_rate=None,
        channels=None,
        data_format=None,
        file_format=None,
        quality=None,
        voice=None,
        ):
        self._text = str(text)

        if channels is not None:
            channels = int(channels)
        self._channels = channels

        if data_format is not None:
            pass
        self._data_format = data_format

        if file_format is not None:
            pass
        self._file_format = file_format

        if quality is not None:
            quality = int(quality)
            assert 0 <= quality < 128
        self._quality = quality

        if voice is not None:
            voice = str(voice)
            assert voice in self._voices
        self._voice = voice
