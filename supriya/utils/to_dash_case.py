from supriya.utils import delimit_words, strip_diacritics


def to_dash_case(string):
    string = strip_diacritics(string)
    words = delimit_words(string)
    words = (_.lower() for _ in words)
    string = '-'.join(words)
    return string
