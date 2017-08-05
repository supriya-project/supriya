from supriya.utils import delimit_words, strip_diacritics


def to_snake_case(string):
    string = strip_diacritics(string)
    words = delimit_words(string)
    words = (_.lower() for _ in words)
    string = '_'.join(words)
    return string
